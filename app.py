# app.py — Site Visit Analyzer — Main Streamlit Application

import json
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import PROPERTY_CONTEXT, SCORE_ICONS, SCORE_LABELS, SEVERITY_COLORS
from utils import (
    aggregate_voc,
    analyze_audio,
    compute_aggregate_stats,
    load_all_data,
    save_analysis,
)

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Site Visit Analyzer",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
        color: #e8eaf6;
    }

    /* Header banner */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }
    .main-header h1 {
        color: white;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        margin: 4px 0 0 0;
        font-size: 0.95rem;
    }
    .property-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.8rem;
        color: white;
        margin-top: 8px;
    }

    /* Score cards */
    .score-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 12px;
    }
    .score-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
    }
    .score-icon { font-size: 1.8rem; margin-bottom: 6px; }
    .score-label { font-size: 0.75rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
    .score-value { font-size: 2.2rem; font-weight: 800; margin: 4px 0; }
    .score-bar {
        height: 6px;
        border-radius: 3px;
        margin-top: 8px;
        background: rgba(255,255,255,0.1);
        overflow: hidden;
    }
    .score-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }

    /* Overall score badge */
    .overall-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        padding: 20px 40px;
        text-align: center;
        display: inline-block;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }
    .overall-badge .score-num { font-size: 3.5rem; font-weight: 800; color: white; }
    .overall-badge .score-max { font-size: 1.2rem; color: rgba(255,255,255,0.7); }
    .overall-badge .score-lbl { font-size: 0.85rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 1px; }

    /* Feedback box */
    .feedback-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border: 1px solid rgba(102, 126, 234, 0.4);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 16px 0;
    }
    .feedback-box .label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #667eea; font-weight: 700; margin-bottom: 6px; }
    .feedback-box p { color: #e8eaf6; font-size: 0.95rem; line-height: 1.6; margin: 0; }

    /* Objection / Positive pills */
    .pill-red {
        display: inline-block;
        background: rgba(255, 75, 75, 0.15);
        border: 1px solid rgba(255, 75, 75, 0.3);
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.82rem;
        color: #ff8a80;
    }
    .pill-green {
        display: inline-block;
        background: rgba(0, 196, 154, 0.15);
        border: 1px solid rgba(0, 196, 154, 0.3);
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.82rem;
        color: #69f0ae;
    }

    /* KPI metric cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .kpi-card .kpi-value { font-size: 2.4rem; font-weight: 800; color: #a78bfa; }
    .kpi-card .kpi-label { font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

    /* Theme cards (VoC) */
    .theme-card {
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 12px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    .theme-card.high {
        background: rgba(255, 75, 75, 0.1);
        border-color: #FF4B4B;
    }
    .theme-card.medium {
        background: rgba(255, 165, 0, 0.1);
        border-color: #FFA500;
    }
    .theme-card.low {
        background: rgba(0, 196, 154, 0.1);
        border-color: #00C49A;
    }
    .theme-title { font-size: 1rem; font-weight: 700; color: #e8eaf6; margin-bottom: 4px; }
    .theme-desc { font-size: 0.85rem; color: #9ca3af; margin-bottom: 8px; }
    .theme-quote { font-size: 0.82rem; color: #c4b5fd; font-style: italic; }
    .severity-badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 2px 10px;
        border-radius: 10px;
        margin-bottom: 8px;
    }

    /* Agent leaderboard */
    .leaderboard-row {
        display: flex;
        align-items: center;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 8px;
        justify-content: space-between;
    }
    .leaderboard-rank { font-size: 1.1rem; font-weight: 800; color: #a78bfa; min-width: 30px; }
    .leaderboard-name { font-size: 0.95rem; font-weight: 600; color: #e8eaf6; flex: 1; margin-left: 12px; }
    .leaderboard-visits { font-size: 0.8rem; color: #9ca3af; }
    .leaderboard-score { font-size: 1.3rem; font-weight: 800; color: #34d399; }

    /* Visit log */
    .visit-log-item {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 8px;
    }

    /* Streamlit overrides */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    div[data-testid="stTabs"] button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: #e8eaf6 !important;
        font-family: 'Inter', sans-serif;
    }
    .stExpander {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #a78bfa !important;
        font-family: 'Inter', sans-serif;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.1); }

    /* Section headers */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e8eaf6;
        margin: 24px 0 14px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0.15), transparent);
        margin-left: 12px;
    }

    /* Recording indicator */
    .recording-hint {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid rgba(255, 75, 75, 0.3);
        border-radius: 10px;
        padding: 12px 18px;
        font-size: 0.88rem;
        color: #ff8a80;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helper Functions ───────────────────────────────────────────────────────────

def score_color(score: float) -> str:
    if score >= 7:
        return "#34d399"
    elif score >= 5:
        return "#fbbf24"
    else:
        return "#f87171"


def score_gradient(score: float) -> str:
    if score >= 7:
        return "linear-gradient(90deg, #34d399, #059669)"
    elif score >= 5:
        return "linear-gradient(90deg, #fbbf24, #d97706)"
    else:
        return "linear-gradient(90deg, #f87171, #dc2626)"


def render_score_card(icon: str, label: str, score: float):
    color = score_color(score)
    gradient = score_gradient(score)
    width_pct = int(score * 10)
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-icon">{icon}</div>
            <div class="score-label">{label}</div>
            <div class="score-value" style="color:{color}">{score}</div>
            <div class="score-bar">
                <div class="score-fill" style="width:{width_pct}%;background:{gradient}"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overall_badge(score: float):
    emoji = "🏆" if score >= 8 else "✅" if score >= 6 else "⚠️"
    st.markdown(
        f"""
        <div style="text-align:center; margin: 20px 0;">
            <div class="overall-badge">
                <div class="score-lbl">Overall Score</div>
                <div>
                    <span class="score-num">{score}</span>
                    <span class="score-max">/10</span>
                </div>
                <div style="font-size:1.5rem">{emoji}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agent_results(result: dict):
    scores = result.get("scores", {})
    overall = result.get("overall_score", 0)

    # Overall badge
    render_overall_badge(overall)

    # Score cards in a 5-column grid
    st.markdown('<div class="section-header">📊 Performance Pillars</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    pillar_keys = [
        "tonality_pitch",
        "product_information",
        "product_knowledge",
        "objection_handling",
        "rapport_building",
    ]
    for col, key in zip(cols, pillar_keys):
        with col:
            render_score_card(
                SCORE_ICONS.get(key, "📌"),
                SCORE_LABELS.get(key, key),
                scores.get(key, 0),
            )

    # Coaching feedback
    feedback = result.get("agent_feedback", "")
    if feedback:
        st.markdown('<div class="section-header">💡 Coaching Insight</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="feedback-box">
                <div class="label">🎯 Action for Next Visit</div>
                <p>{feedback}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Objections and Positives side by side
    col_obj, col_pos = st.columns(2)

    with col_obj:
        st.markdown('<div class="section-header">🚨 Customer Objections</div>', unsafe_allow_html=True)
        objections = result.get("customer_objections", [])
        if objections:
            pills = "".join(f'<span class="pill-red">⚡ {o}</span>' for o in objections)
            st.markdown(f'<div style="line-height:2">{pills}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#6b7280">No objections detected.</p>', unsafe_allow_html=True)

    with col_pos:
        st.markdown('<div class="section-header">✅ Customer Positives</div>', unsafe_allow_html=True)
        positives = result.get("customer_positives", [])
        if positives:
            pills = "".join(f'<span class="pill-green">✓ {p}</span>' for p in positives)
            st.markdown(f'<div style="line-height:2">{pills}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#6b7280">No positives captured.</p>', unsafe_allow_html=True)

    # Transcript
    transcript = result.get("transcript", "")
    if transcript:
        st.markdown('<div class="section-header">📝 Transcript</div>', unsafe_allow_html=True)
        with st.expander("View Full Transcript", expanded=False):
            st.write(transcript)


# ── Main App ───────────────────────────────────────────────────────────────────

def main():
    # Header
    st.markdown(
        f"""
        <div class="main-header">
            <h1>🏡 Site Visit Analyzer</h1>
            <p>AI-powered real estate sales coaching & Voice of Customer intelligence</p>
            <span class="property-badge">📍 {PROPERTY_CONTEXT["name"]} · {PROPERTY_CONTEXT["location"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["🎙️  Sales Agent Dashboard", "📊  Developer Dashboard"])

    # ── TAB 1: AGENT VIEW ──────────────────────────────────────────────────────
    with tab1:
        st.markdown(
            """
            <div style="margin-bottom:20px">
                <h3 style="color:#e8eaf6;font-weight:700;margin-bottom:4px">Record Your Site Visit</h3>
                <p style="color:#9ca3af;font-size:0.9rem">
                    Record a summary of your site visit conversation immediately after the meeting.
                    The AI will analyze your performance across 5 coaching pillars.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Agent and Lead name inputs
        col_a, col_b = st.columns(2)
        with col_a:
            agent_name = st.text_input("Your Name", placeholder="e.g. Priya Sharma", key="agent_name")
        with col_b:
            lead_name = st.text_input("Lead / Customer Name", placeholder="e.g. Rajesh Kapoor", key="lead_name")

        st.markdown(
            '<div class="recording-hint">🔴 Tip: Speak clearly and include the key parts of your conversation — the property pitch, any objections raised, and how you responded.</div>',
            unsafe_allow_html=True,
        )

        audio_value = st.audio_input("🎙️ Record Site Visit Conversation (WAV)")

        if audio_value is not None:
            st.markdown("---")
            with st.spinner("🤖 Gemini is analyzing your site visit... (this may take 15–30 seconds)"):
                try:
                    audio_bytes = audio_value.read()
                    result = analyze_audio(audio_bytes, mime_type="audio/wav")
                    st.session_state["latest_result"] = result
                    st.session_state["latest_agent"] = agent_name
                    st.session_state["latest_lead"] = lead_name
                    st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.info("Please check your GOOGLE_API_KEY in the .env file and try again.")
                    result = None

            if result:
                render_agent_results(result)

                st.markdown("---")
                col_save, col_spacer = st.columns([1, 3])
                with col_save:
                    if st.button("💾 Save Analysis to Dashboard", use_container_width=True):
                        save_analysis(
                            result,
                            agent_name=agent_name,
                            lead_name=lead_name,
                        )
                        st.success(f"✅ Saved! This visit will now appear in the Developer Dashboard.")
                        st.balloons()

        elif "latest_result" in st.session_state:
            # Show the last result from this session even after re-run
            st.info("ℹ️ Showing your last analysis from this session. Record again to analyze a new visit.")
            render_agent_results(st.session_state["latest_result"])

        else:
            # Empty state
            st.markdown(
                """
                <div style="text-align:center;padding:60px 20px;opacity:0.5">
                    <div style="font-size:3rem">🎙️</div>
                    <div style="font-size:1rem;color:#9ca3af;margin-top:12px">
                        Click the microphone above to start recording your site visit
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── TAB 2: DEVELOPER VIEW ──────────────────────────────────────────────────
    with tab2:
        all_visits = load_all_data()
        stats = compute_aggregate_stats(all_visits)

        st.markdown(
            """
            <div style="margin-bottom:20px">
                <h3 style="color:#e8eaf6;font-weight:700;margin-bottom:4px">Developer Intelligence Dashboard</h3>
                <p style="color:#9ca3af;font-size:0.9rem">
                    Aggregated insights across all site visits — track agent performance and surface product-level customer concerns.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not all_visits:
            st.warning("No visit data found. Record and save a site visit in the Agent tab first.")
            return

        # ── KPI Row ──
        st.markdown('<div class="section-header">📈 Key Metrics</div>', unsafe_allow_html=True)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-value">{stats["total_visits"]}</div><div class="kpi-label">Total Site Visits</div></div>',
                unsafe_allow_html=True,
            )
        with kpi2:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-value">{stats["overall_avg"]}/10</div><div class="kpi-label">Avg Overall Score</div></div>',
                unsafe_allow_html=True,
            )
        with kpi3:
            avg_obj = stats["avg_pillars"].get("objection_handling", 0)
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-value">{avg_obj}/10</div><div class="kpi-label">Avg Objection Handling</div></div>',
                unsafe_allow_html=True,
            )
        with kpi4:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-value" style="font-size:1.1rem;padding-top:6px">{stats["top_concern"]}</div><div class="kpi-label">Top Customer Concern</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Score Breakdown & Agent Leaderboard side by side ──
        col_chart, col_board = st.columns([3, 2])

        with col_chart:
            st.markdown('<div class="section-header">📊 Average Pillar Scores</div>', unsafe_allow_html=True)
            avg_pillars = stats["avg_pillars"]
            labels = [SCORE_LABELS[k] for k in avg_pillars]
            values = [avg_pillars[k] for k in avg_pillars]
            colors = [score_color(v) for v in values]

            fig = go.Figure(
                go.Bar(
                    x=values,
                    y=labels,
                    orientation="h",
                    marker=dict(
                        color=colors,
                        line=dict(color="rgba(255,255,255,0.1)", width=1),
                    ),
                    text=[f"{v}/10" for v in values],
                    textposition="outside",
                    textfont=dict(color="white", size=13, family="Inter"),
                )
            )
            fig.update_layout(
                xaxis=dict(range=[0, 10.5], showgrid=True, gridcolor="rgba(255,255,255,0.08)", color="white"),
                yaxis=dict(color="white", tickfont=dict(size=12, family="Inter")),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=60, t=10, b=10),
                height=280,
                font=dict(family="Inter", color="white"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_board:
            st.markdown('<div class="section-header">🏆 Agent Leaderboard</div>', unsafe_allow_html=True)
            rank_emojis = ["🥇", "🥈", "🥉"]
            for i, agent in enumerate(stats["leaderboard"]):
                rank = rank_emojis[i] if i < 3 else f"#{i+1}"
                color = score_color(agent["avg_score"])
                st.markdown(
                    f"""
                    <div class="leaderboard-row">
                        <span class="leaderboard-rank">{rank}</span>
                        <span class="leaderboard-name">{agent["agent_name"]}</span>
                        <span class="leaderboard-visits" style="margin-right:12px">{agent["visits"]} visits</span>
                        <span class="leaderboard-score" style="color:{color}">{agent["avg_score"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── VoC Synthesis ──
        st.markdown('<div class="section-header">🗣️ Voice of Customer — Product Insights</div>', unsafe_allow_html=True)
        st.markdown(
            f'<p style="color:#9ca3af;font-size:0.88rem">Based on objections collected across {stats["all_objections_count"]} customer interactions. Click below to synthesize with AI.</p>',
            unsafe_allow_html=True,
        )

        voc_col, _ = st.columns([1, 3])
        with voc_col:
            synthesize_btn = st.button("🤖 Synthesize Customer Objections with AI", use_container_width=True)

        if synthesize_btn or "voc_result" in st.session_state:
            if synthesize_btn:
                with st.spinner("🧠 Gemini is analyzing customer objections across all visits..."):
                    try:
                        voc_result = aggregate_voc(all_visits)
                        st.session_state["voc_result"] = voc_result
                    except Exception as e:
                        st.error(f"❌ VoC synthesis failed: {str(e)}")
                        voc_result = None
            else:
                voc_result = st.session_state.get("voc_result")

            if voc_result:
                summary = voc_result.get("summary", "")
                if summary:
                    st.markdown(
                        f"""
                        <div class="feedback-box" style="margin-bottom:16px">
                            <div class="label">📋 Executive Summary</div>
                            <p>{summary}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                themes = voc_result.get("themes", [])
                theme_cols = st.columns(min(len(themes), 3))
                for i, theme in enumerate(themes[:3]):
                    sev = theme.get("severity", "Medium")
                    sev_color = SEVERITY_COLORS.get(sev, "#FFA500")
                    with theme_cols[i]:
                        st.markdown(
                            f"""
                            <div class="theme-card {sev.lower()}">
                                <span class="severity-badge" style="background:rgba(255,255,255,0.1);color:{sev_color}">
                                    {sev} Priority · {theme.get("count", "?")} mentions
                                </span>
                                <div class="theme-title">{theme.get("title", "")}</div>
                                <div class="theme-desc">{theme.get("description", "")}</div>
                                <div class="theme-quote">"{theme.get("example_quote", "")}"</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Visit Log ──
        st.markdown('<div class="section-header">📋 All Site Visit Records</div>', unsafe_allow_html=True)

        for visit in all_visits:
            ts = visit.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts)
                formatted_ts = dt.strftime("%d %b %Y, %I:%M %p")
            except Exception:
                formatted_ts = ts

            overall = visit.get("overall_score", "–")
            overall_color = score_color(overall) if isinstance(overall, (int, float)) else "#9ca3af"
            is_live = visit.get("id", "").startswith("live_")
            badge = '<span style="font-size:0.7rem;background:rgba(102,126,234,0.3);border-radius:6px;padding:2px 8px;color:#a78bfa;margin-left:8px">LIVE</span>' if is_live else ""

            with st.expander(
                f"{visit.get('agent_name', 'Agent')} → {visit.get('lead_name', 'Lead')}   |   {formatted_ts}   |   Score: {overall}/10"
            ):
                r_col1, r_col2 = st.columns([2, 1])
                with r_col1:
                    transcript = visit.get("transcript", "No transcript available.")
                    st.markdown(f"**Transcript:**\n\n{transcript}")
                    feedback = visit.get("agent_feedback", "")
                    if feedback:
                        st.markdown(
                            f'<div class="feedback-box"><div class="label">💡 Coaching</div><p>{feedback}</p></div>',
                            unsafe_allow_html=True,
                        )
                with r_col2:
                    scores = visit.get("scores", {})
                    for key, label in SCORE_LABELS.items():
                        score_val = scores.get(key, 0)
                        c = score_color(score_val)
                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;margin-bottom:6px">'
                            f'<span style="color:#9ca3af;font-size:0.82rem">{SCORE_ICONS.get(key,"")} {label}</span>'
                            f'<span style="color:{c};font-weight:700">{score_val}/10</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    objections = visit.get("customer_objections", [])
                    if objections:
                        st.markdown("**Customer Objections:**")
                        for obj in objections:
                            st.markdown(f'<span class="pill-red">⚡ {obj}</span>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
