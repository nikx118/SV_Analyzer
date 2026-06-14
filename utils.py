# utils.py — Gemini API helpers, data management, and aggregation logic

import json
import os
import re
import time
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

from config import AUDIO_ANALYSIS_PROMPT, VOC_AGGREGATION_PROMPT

# ── Environment & API Setup ────────────────────────────────────────────────────
load_dotenv()

_api_key = os.getenv("GOOGLE_API_KEY")
if _api_key:
    genai.configure(api_key=_api_key)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
MOCK_DATA_PATH = BASE_DIR / "mock_data.json"
LIVE_DATA_PATH = BASE_DIR / "data.json"

# ── Gemini Model ───────────────────────────────────────────────────────────────
GEMINI_MODEL = "gemini-2.5-flash"


def _get_model():
    """Return a configured Gemini GenerativeModel instance."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. Please add it to your .env file."
        )
    return genai.GenerativeModel(GEMINI_MODEL)


# ── Audio Analysis ─────────────────────────────────────────────────────────────

def analyze_audio(audio_bytes: bytes, mime_type: str = "audio/wav") -> dict:
    """
    Send audio bytes to Gemini 1.5 Pro for site visit analysis.
    Returns a parsed dict with keys: transcript, scores, overall_score,
    agent_feedback, customer_objections, customer_positives.
    """
    model = _get_model()

    audio_part = {
        "mime_type": mime_type,
        "data": audio_bytes,
    }

    response = model.generate_content(
        [AUDIO_ANALYSIS_PROMPT, audio_part],
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=4096,
        ),
    )

    raw_text = response.text.strip()
    return _parse_json_response(raw_text)


def _parse_json_response(raw_text: str) -> dict:
    """
    Robustly parse a JSON response from Gemini.
    Strips markdown code fences if present.
    """
    # Strip markdown code fences
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.MULTILINE)
    cleaned = re.sub(r"```\s*$", "", cleaned, flags=re.MULTILINE).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract the first JSON object from the text
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            raise ValueError(f"Could not parse JSON from Gemini response:\n{raw_text}")

    # Ensure overall_score is computed if missing
    if "overall_score" not in data and "scores" in data:
        scores = data["scores"]
        data["overall_score"] = round(sum(scores.values()) / len(scores), 1)

    return data


# ── VoC Aggregation ────────────────────────────────────────────────────────────

def aggregate_voc(all_visits: list[dict]) -> dict:
    """
    Collects all customer_objections from visits and asks Gemini
    to identify the top 3 recurring product-level themes.
    """
    model = _get_model()

    all_objections = []
    for visit in all_visits:
        objections = visit.get("customer_objections", [])
        all_objections.extend(objections)

    if not all_objections:
        return {
            "themes": [],
            "summary": "No customer objections recorded yet.",
        }

    objections_text = "\n".join(f"- {obj}" for obj in all_objections)
    prompt = VOC_AGGREGATION_PROMPT.format(objections_text=objections_text)

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            max_output_tokens=4096,
        ),
    )

    return _parse_json_response(response.text.strip())


# ── Data Persistence ───────────────────────────────────────────────────────────

def load_mock_data() -> list[dict]:
    """Load the pre-generated mock site visit analyses."""
    if MOCK_DATA_PATH.exists():
        with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def load_live_data() -> list[dict]:
    """Load live recorded analyses from data.json."""
    if LIVE_DATA_PATH.exists():
        with open(LIVE_DATA_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def load_all_data() -> list[dict]:
    """Merge mock data and live data, sorted by timestamp descending."""
    mock = load_mock_data()
    live = load_live_data()
    combined = live + mock  # live data first
    return combined


def save_analysis(analysis: dict, agent_name: str, lead_name: str) -> None:
    """Append a new analysis to data.json with metadata."""
    from datetime import datetime

    analysis["id"] = f"live_{int(time.time())}"
    analysis["agent_name"] = agent_name or "Unknown Agent"
    analysis["lead_name"] = lead_name or "Unknown Lead"
    analysis["timestamp"] = datetime.now().isoformat()

    live_data = load_live_data()
    live_data.append(analysis)

    with open(LIVE_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(live_data, f, indent=2, ensure_ascii=False)


# ── Aggregate Statistics ───────────────────────────────────────────────────────

def compute_aggregate_stats(all_visits: list[dict]) -> dict:
    """
    Compute aggregate statistics across all visits.
    Returns avg scores per pillar, overall avg, top concern, agent leaderboard.
    """
    if not all_visits:
        return {}

    pillar_keys = [
        "tonality_pitch",
        "product_information",
        "product_knowledge",
        "objection_handling",
        "rapport_building",
    ]

    pillar_totals = {k: 0.0 for k in pillar_keys}
    pillar_counts = {k: 0 for k in pillar_keys}
    overall_scores = []

    # Per-agent aggregation
    agent_stats: dict[str, dict] = {}

    for visit in all_visits:
        scores = visit.get("scores", {})
        for k in pillar_keys:
            if k in scores:
                pillar_totals[k] += scores[k]
                pillar_counts[k] += 1

        overall = visit.get("overall_score")
        if overall is not None:
            overall_scores.append(overall)

        # Agent leaderboard
        agent = visit.get("agent_name", "Unknown")
        if agent not in agent_stats:
            agent_stats[agent] = {"scores": [], "visits": 0}
        if overall is not None:
            agent_stats[agent]["scores"].append(overall)
        agent_stats[agent]["visits"] += 1

    avg_pillars = {
        k: round(pillar_totals[k] / pillar_counts[k], 1) if pillar_counts[k] > 0 else 0
        for k in pillar_keys
    }

    overall_avg = round(sum(overall_scores) / len(overall_scores), 1) if overall_scores else 0.0

    # Find the lowest scoring pillar (top concern area)
    weakest_pillar = min(avg_pillars, key=avg_pillars.get) if avg_pillars else None

    # Agent leaderboard
    leaderboard = []
    for agent, data in agent_stats.items():
        avg = round(sum(data["scores"]) / len(data["scores"]), 1) if data["scores"] else 0
        leaderboard.append(
            {
                "agent_name": agent,
                "avg_score": avg,
                "visits": data["visits"],
            }
        )
    leaderboard.sort(key=lambda x: x["avg_score"], reverse=True)

    # Most common objection keyword (simple heuristic)
    all_objections = []
    for visit in all_visits:
        all_objections.extend(visit.get("customer_objections", []))

    top_concern = _extract_top_concern(all_objections)

    return {
        "total_visits": len(all_visits),
        "overall_avg": overall_avg,
        "avg_pillars": avg_pillars,
        "leaderboard": leaderboard,
        "top_concern": top_concern,
        "all_objections_count": len(all_objections),
    }


def _extract_top_concern(objections: list[str]) -> str:
    """Simple keyword frequency analysis to find the top concern."""
    keywords = {
        "price": ["price", "crore", "expensive", "cost", "steep", "₹", "budget"],
        "possession": ["possession", "2026", "delay", "timeline", "date", "wait"],
        "competitor": ["brigade", "prestige", "sobha", "competitor", "other project"],
        "location": ["traffic", "commute", "far", "connectivity", "distance"],
        "knowledge": ["don't know", "didn't know", "confirm", "check", "unsure"],
    }
    counts = {k: 0 for k in keywords}
    for objection in objections:
        obj_lower = objection.lower()
        for category, words in keywords.items():
            if any(w in obj_lower for w in words):
                counts[category] += 1

    if not any(counts.values()):
        return "General Concerns"

    top = max(counts, key=counts.get)
    labels = {
        "price": "Pricing / Budget",
        "possession": "Possession Timeline",
        "competitor": "Competitor Comparisons",
        "location": "Location / Commute",
        "knowledge": "Agent Product Knowledge",
    }
    return labels.get(top, "General Concerns")
