# config.py — Property context and AI prompt configuration

PROPERTY_CONTEXT = {
    "name": "Sunrise Residences",
    "type": "Luxury Residential Apartments",
    "location": "Whitefield, Bangalore",
    "price_range": "₹2.5 Cr – ₹3.2 Cr",
    "size": "2,800 – 3,500 sq.ft (4 BHK)",
    "possession": "Q4 2026",
    "developer": "Sunrise Properties Pvt. Ltd.",
    "usps": [
        "Rooftop infinity pool with panoramic city views",
        "3-acre landscaped garden and jogging track",
        "German modular kitchen with Hettich fittings",
        "Complimentary 2 BHK service apartment on purchase",
        "500 metres from upcoming Purple Line Metro station (Whitefield Phase 2)",
        "RERA registered — RERA No. PRM/KA/RERA/2024/SR-001",
        "Vastu-compliant floor plans",
        "24/7 concierge and smart home automation",
    ],
    "competitor_projects": ["Brigade Orchards", "Prestige Lakeside Habitat", "Sobha Dream Acres"],
    "target_buyer": "IT professionals, NRIs, HNI investors",
}

AUDIO_ANALYSIS_PROMPT = f"""
You are an expert Real Estate Sales Manager evaluating a recorded site visit conversation for '{PROPERTY_CONTEXT["name"]}' — a {PROPERTY_CONTEXT["type"]} in {PROPERTY_CONTEXT["location"]}.

Property Context:
- Price: {PROPERTY_CONTEXT["price_range"]}
- Possession: {PROPERTY_CONTEXT["possession"]}
- Key USPs the agent SHOULD have covered: {", ".join(PROPERTY_CONTEXT["usps"][:5])}

Listen carefully to the audio recording and:
1. Generate a concise transcript of the conversation (max 300 words).
2. Evaluate the SALES AGENT's performance (NOT the customer) on each of the following pillars, scored 1–10:
   - **tonality_pitch**: Was the agent confident, warm, and engaging? Or rushed/monotone?
   - **product_information**: Did the agent cover the key USPs of the property?
   - **product_knowledge**: Did the agent answer questions accurately without hesitation?
   - **objection_handling**: How well did the agent handle customer concerns (pricing, possession, comparisons)?
   - **rapport_building**: Did the agent establish a personal connection with the customer?
3. Calculate an overall_score (average of the 5 pillars, rounded to 1 decimal).
4. Write one specific, actionable piece of coaching feedback for the agent.
5. Extract what the CUSTOMER said they liked and disliked about the property (NOT the agent — about the property itself).

IMPORTANT: Return ONLY a valid JSON object. No markdown, no code fences, no explanation.

JSON format:
{{
  "transcript": "...",
  "scores": {{
    "tonality_pitch": <1-10>,
    "product_information": <1-10>,
    "product_knowledge": <1-10>,
    "objection_handling": <1-10>,
    "rapport_building": <1-10>
  }},
  "overall_score": <float>,
  "agent_feedback": "One specific, actionable sentence.",
  "customer_objections": ["objection 1", "objection 2"],
  "customer_positives": ["positive 1", "positive 2"]
}}
"""

VOC_AGGREGATION_PROMPT = """
You are a real estate product manager analyzing customer feedback from multiple site visits.
Below is a list of customer objections collected from all recent site visits.

Your task: Identify the top 3 recurring themes or concerns that customers have about the PROPERTY (not the agents).
For each theme, provide:
- A short theme title
- A brief description
- An example quote from the objections
- A severity level: "High" | "Medium" | "Low"

IMPORTANT: Return ONLY a valid JSON object. No markdown, no code fences.

JSON format:
{{
  "themes": [
    {{
      "title": "...",
      "description": "...",
      "example_quote": "...",
      "severity": "High|Medium|Low",
      "count": <number of mentions>
    }}
  ],
  "summary": "One sentence executive summary of the overall customer sentiment."
}}

Customer objections to analyze:
{objections_text}
"""

SCORE_LABELS = {
    "tonality_pitch": "Tonality & Pitch",
    "product_information": "Product Information",
    "product_knowledge": "Product Knowledge",
    "objection_handling": "Objection Handling",
    "rapport_building": "Rapport Building",
}

SCORE_ICONS = {
    "tonality_pitch": "🎤",
    "product_information": "🏠",
    "product_knowledge": "📚",
    "objection_handling": "🛡️",
    "rapport_building": "🤝",
}

SEVERITY_COLORS = {
    "High": "#FF4B4B",
    "Medium": "#FFA500",
    "Low": "#00C49A",
}
