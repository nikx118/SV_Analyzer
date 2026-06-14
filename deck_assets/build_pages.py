from common import HEAD, TAIL, HEADER_BANNER

# ── Screen 1: Agent recording view ──────────────────────────────────────────
screen1 = HEAD + HEADER_BANNER + """
<div class="tabs">
  <div class="tab active">🎙️ Sales Agent Dashboard</div>
  <div class="tab">📊 Developer Dashboard</div>
</div>
<h3 class="section-title">Record Your Site Visit</h3>
<p class="section-sub">Record a summary of your site visit conversation immediately after the meeting. The AI will analyze your performance across 5 coaching pillars.</p>

<div style="display:flex; gap:24px; margin-top:18px">
  <div style="flex:1">
    <div style="color:#e8eaf6; font-size:0.85rem; margin-bottom:6px; font-weight:600">Your Name</div>
    <div class="stTextInput" style="background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:10px 14px; color:#6b7280">e.g. Priya Sharma</div>
  </div>
  <div style="flex:1">
    <div style="color:#e8eaf6; font-size:0.85rem; margin-bottom:6px; font-weight:600">Lead / Customer Name</div>
    <div class="stTextInput" style="background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.15); border-radius:10px; padding:10px 14px; color:#6b7280">e.g. Rajesh Kapoor</div>
  </div>
</div>

<div class="recording-hint" style="margin-top:18px">🔴 Tip: Speak clearly and include the key parts of your conversation — the property pitch, any objections raised, and how you responded.</div>

<div style="margin-top:6px; color:#e8eaf6; font-size:0.9rem; font-weight:600">🎙️ Record Site Visit Conversation (WAV)</div>
<div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:18px; margin-top:10px; display:flex; align-items:center; gap:14px">
  <div style="font-size:1.4rem">🎙️</div>
  <div style="flex:1; height:2px; background:repeating-linear-gradient(90deg, rgba(255,255,255,0.25) 0 4px, transparent 4px 10px)"></div>
  <div style="color:#9ca3af; font-size:0.85rem">00:00</div>
</div>

<div style="text-align:center; padding:60px 20px; opacity:0.55">
  <div style="font-size:3rem">🎙️</div>
  <div style="font-size:1rem; color:#9ca3af; margin-top:12px">Click the microphone above to start recording your site visit</div>
</div>
""" + TAIL

# ── Screen 2: Developer Dashboard - KPIs ────────────────────────────────────
def kpi(value, label, big=False):
    fs = "1.1rem" if big else None
    style = f' style="font-size:{fs}; padding-top:6px"' if fs else ""
    return f'<div class="kpi-card"><div class="kpi-value"{style}>{value}</div><div class="kpi-label">{label}</div></div>'

screen2 = HEAD + HEADER_BANNER + """
<div class="tabs">
  <div class="tab">🎙️ Sales Agent Dashboard</div>
  <div class="tab active">📊 Developer Dashboard</div>
</div>
<h3 class="section-title">Developer Intelligence Dashboard</h3>
<p class="section-sub">Aggregated insights across all site visits — track agent performance and surface product-level customer concerns.</p>

<div class="section-header" style="margin-top:24px">📈 Key Metrics</div>
<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:18px; margin-top:14px">
""" + kpi("6", "Total Site Visits") + kpi("6.8/10", "Avg Overall Score") + kpi("6.5/10", "Avg Objection Handling") + kpi("Pricing / Budget", "Top Customer Concern", big=True) + """
</div>
""" + TAIL

# ── Screen 3: Pillar chart + leaderboard ────────────────────────────────────
def bar(label, val, color):
    pct = val / 10 * 100
    return f"""<div class="bar-row">
      <div class="bar-label">{label}</div>
      <div class="bar-track">
        <div class="bar-fill" style="width:{pct}%; background:{color}"></div>
      </div>
      <div class="bar-val">{val}/10</div>
    </div>"""

def lb_row(rank, name, visits, score, color):
    return f"""<div class="leaderboard-row">
      <span class="leaderboard-rank">{rank}</span>
      <span class="leaderboard-name">{name}</span>
      <span class="leaderboard-visits" style="margin-right:12px">{visits} visits</span>
      <span class="leaderboard-score" style="color:{color}">{score}</span>
    </div>"""

screen3 = HEAD + HEADER_BANNER + """
<div class="tabs">
  <div class="tab">🎙️ Sales Agent Dashboard</div>
  <div class="tab active">📊 Developer Dashboard</div>
</div>
<div style="display:flex; gap:32px; margin-top:10px">
  <div style="flex:3">
    <div class="section-header">📊 Average Pillar Scores</div>
    <div style="margin-top:18px">
""" + bar("Rapport Building", 7.0, "linear-gradient(90deg, #34d399, #059669)") \
    + bar("Objection Handling", 6.5, "linear-gradient(90deg, #fbbf24, #d97706)") \
    + bar("Product Knowledge", 6.5, "linear-gradient(90deg, #fbbf24, #d97706)") \
    + bar("Product Information", 6.5, "linear-gradient(90deg, #fbbf24, #d97706)") \
    + bar("Tonality &amp; Pitch", 7.3, "linear-gradient(90deg, #34d399, #059669)") + """
      <div class="axis"><span>0</span><span>2</span><span>4</span><span>6</span><span>8</span><span>10</span></div>
    </div>
  </div>
  <div style="flex:2">
    <div class="section-header">🏆 Agent Leaderboard</div>
    <div style="margin-top:18px">
""" + lb_row("🥇", "Priya Sharma", 2, "8.8", "#34d399") \
    + lb_row("🥈", "Sneha Kulkarni", 1, "8.8", "#34d399") \
    + lb_row("🥉", "Vikram Joshi", 1, "8.2", "#34d399") \
    + lb_row("#4", "Arjun Mehta", 2, "3.0", "#f87171") + """
    </div>
  </div>
</div>
""" + TAIL

# ── Screen 4: VoC AI synthesis ──────────────────────────────────────────────
def theme_card(severity, count, title, desc, quote, css_class, color):
    return f"""<div class="theme-card {css_class}">
      <span class="severity-badge" style="background:rgba(255,255,255,0.1);color:{color}">{severity} Priority · {count} mentions</span>
      <div class="theme-title">{title}</div>
      <div class="theme-desc">{desc}</div>
      <div class="theme-quote">"{quote}"</div>
    </div>"""

screen4 = HEAD + HEADER_BANNER + """
<div class="tabs">
  <div class="tab">🎙️ Sales Agent Dashboard</div>
  <div class="tab active">📊 Developer Dashboard</div>
</div>
<div class="section-header">🗣️ Voice of Customer — Product Insights</div>
<p class="section-sub">Based on objections collected across 17 customer interactions — synthesized by Gemini AI.</p>

<div class="feedback-box" style="margin:16px 0">
  <div class="label">📋 Executive Summary</div>
  <p>The overall customer sentiment indicates significant concerns regarding the property's pricing and perceived value, the extended possession timelines, and the lack of clear data to support its investment potential.</p>
</div>

<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:18px; margin-top:8px">
""" + theme_card("High", 5, "Price &amp; Value Proposition",
                 "Customers perceive the property's price as high relative to competitors or their budget, and question the justification for the cost, including payment terms and the opportunity cost of capital.",
                 "Price at ₹2.8 crore feels steep compared to competitors", "high", "#FF4B4B") \
    + theme_card("High", 3, "Possession &amp; Availability Timeline",
                 "Customers express dissatisfaction with the long wait for possession, indicating a need for earlier occupancy or ready-to-move options.",
                 "Possession date Q4 2026 is too late — need apartment by March 2026", "high", "#FF4B4B") \
    + theme_card("Medium", 2, "Investment Potential &amp; Certainty",
                 "Customers are looking for stronger assurances and data regarding the property's future financial performance, specifically rental yield and capital appreciation.",
                 "Skeptical about appreciation projections without data", "medium", "#FFA500") + """
</div>
""" + TAIL

# ── Screen 5: Agent scorecard detail (visit record) ─────────────────────────
def score_row(icon, label, val):
    color = "#34d399" if val >= 7 else "#fbbf24" if val >= 5 else "#f87171"
    return f"""<div style="display:flex;justify-content:space-between;margin-bottom:10px">
      <span style="color:#9ca3af;font-size:0.88rem">{icon} {label}</span>
      <span style="color:{color};font-weight:700">{val}/10</span>
    </div>"""

transcript = ("Agent: Good morning Mr. and Mrs. Kapoor! Welcome to Sunrise Residences. I'm so glad you could make it "
"today. How was the drive in from Koramangala? Customer: The traffic was terrible actually, almost 45 minutes. "
"Agent: Oh I completely understand, the traffic in Bangalore can be brutal. That's actually one of the reasons our "
"residents love this location — the upcoming metro station is just 500 metres away. Your daily commute is going "
"to transform once it opens. Customer: Oh really? When does the metro come? Agent: The Purple Line Phase 2 is "
"expected to be operational by Q1 2027... Customer: The view is stunning. But honestly, ₹2.8 crore is quite steep "
"for us. We've been looking at Prestige Lakeside too and they're offering better payment plans. Agent: I completely "
"hear you on the price point. Prestige Lakeside doesn't include the complimentary service apartment that comes "
"with every unit here — that's a ₹45 lakh asset at no extra cost...")

screen5 = HEAD + HEADER_BANNER + """
<div class="tabs">
  <div class="tab">🎙️ Sales Agent Dashboard</div>
  <div class="tab active">📊 Developer Dashboard</div>
</div>
<div class="section-header">📋 Site Visit Record — Priya Sharma → Rajesh &amp; Meena Kapoor &nbsp;|&nbsp; Score: 8.6/10</div>

<div style="display:flex; gap:28px; margin-top:14px">
  <div style="flex:2">
    <div style="font-weight:700; color:#e8eaf6; margin-bottom:8px">Transcript:</div>
    <div style="color:#c4b5fd; font-size:0.9rem; line-height:1.7; max-height:280px; overflow:hidden">""" + transcript + """</div>
    <div class="feedback-box" style="margin-top:16px">
      <div class="label">💡 Coaching</div>
      <p>Excellent rapport and objection handling — next time also mention the smart home automation to reinforce the premium value proposition.</p>
    </div>
  </div>
  <div style="flex:1">
""" + score_row("🎤", "Tonality &amp; Pitch", 9) \
    + score_row("🏠", "Product Information", 8) \
    + score_row("📚", "Product Knowledge", 8) \
    + score_row("🛡️", "Objection Handling", 9) \
    + score_row("🤝", "Rapport Building", 9) + """
    <div style="margin-top:16px; font-weight:700; color:#e8eaf6; margin-bottom:8px">Customer Objections:</div>
    <span class="pill-red">⚡ Price at ₹2.8 crore feels steep</span><br>
    <span class="pill-red" style="margin-top:6px">⚡ Prestige Lakeside better payment flexibility</span>
  </div>
</div>
""" + TAIL

for name, html in [("screen1", screen1), ("screen2", screen2), ("screen3", screen3), ("screen4", screen4), ("screen5", screen5)]:
    with open(f"{name}.html", "w", encoding="utf-8") as f:
        f.write(html)
print("done")
