# 🏡 Site Visit Analyzer

**AI-powered sales coaching & Voice-of-Customer intelligence for real estate site visits.**

Real estate site visits generate rich conversational data — the agent's pitch, the customer's
objections, on-the-spot feedback — that is normally lost the moment the visit ends. Site Visit
Analyzer turns a short voice recording of a site visit into:

- **Instant AI coaching** for the sales agent (transcript, pillar scores, and a concrete tip)
- **Aggregated Voice-of-Customer (VoC) insights** for the developer / sales manager team

It is a Streamlit prototype built around Google Gemini's multimodal (audio) analysis.

## How It Works

1. **Record** — the agent records a short spoken summary of the visit, right in the browser.
2. **AI Analysis** — Gemini listens to the raw audio (tone, pacing, content — not just a transcript)
   and scores the visit across 5 coaching pillars.
3. **Instant Coaching** — the agent sees their overall score, a pillar breakdown, the transcript,
   and one actionable coaching tip.
4. **Aggregated VoC** — the developer dashboard aggregates objections across every visit and uses
   Gemini to synthesize recurring customer themes, ranked by priority.

## Core Features

1. **Audio Capture** — one-click in-browser recording of a site-visit summary (WAV).
2. **Multimodal AI Analysis** — Gemini scores each visit on:
   - Tonality & Pitch
   - Product Information coverage
   - Product Knowledge
   - Objection Handling
   - Rapport Building
3. **Agent Coaching View** — overall score, pillar breakdown, transcript, coaching tip, and
   extracted customer objections & positives.
4. **Developer Dashboard** — aggregated KPIs, agent leaderboard, and AI-synthesized VoC themes
   across all visits.
5. **Persistence** — live recordings are saved alongside seeded mock data to simulate a
   historical dataset.

## Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Engine:** Google Gemini (`gemini-2.5-flash`), multimodal audio input
- **Storage:** Local JSON (`mock_data.json` + `data.json`)

## Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your Gemini API key
cp .env.example .env
# then edit .env and set GOOGLE_API_KEY=<your key>

# 3. Run the app
streamlit run app.py
```

## Project Structure

```
app.py            # Streamlit UI — Sales Agent & Developer dashboards
config.py         # Property context, prompts, score labels/icons
utils.py          # Gemini helpers, JSON parsing, data persistence & aggregation
mock_data.json    # Seeded mock site-visit analyses
data.json         # Live recorded analyses (generated at runtime)
PRD.md            # Product requirements document
```

## Pilot Property

📍 **Sunrise Residences**, Whitefield, Bangalore

## Team — BYTEBattle

- **Nikhil**
- **Shehzaad**
- **Jahanvi**

---
*Prototype built for a hackathon. See [PRD.md](PRD.md) for the full product requirements.*
