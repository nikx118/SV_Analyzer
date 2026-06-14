# SiteVisit AI — Product Requirements Document

**Status:** Prototype (post-hackathon MVP)
**Owner:** Nikhil/Shehzaad/Jahanvi/BYTEBattle

## 1. Problem
Real estate site visits generate rich conversational data (agent pitch quality, customer
objections, product feedback) that is currently lost. Sales managers have no objective way to
coach agents, and developers have no aggregated signal on why leads don't convert.

## 2. Objective
Turn a voice recording of a site visit into (a) instant AI coaching for the agent and (b)
aggregated Voice-of-Customer (VoC) insights for the developer/project team.

## 3. Target Personas
| Persona | Need |
|---|---|
| **Sales Agent** | "How did I perform? What should I do differently with this lead?" |
| **Developer / Sales Manager** | "Across all visits, why are customers hesitating — price, location, agent knowledge?" |

## 4. Core Features (MVP Scope)
1. **Audio Capture** — one-click in-browser recording of a site-visit summary.
2. **Multimodal AI Analysis** (Gemini) — listens to the raw audio (not just text) and scores the
   agent on 5 pillars:
   - Tonality & Pitch
   - Product Information coverage
   - Product Knowledge
   - Objection Handling
   - Rapport Building
3. **Agent Coaching View** — overall score, pillar breakdown, transcript, one actionable coaching
   tip, customer objections & positives.
4. **Developer Dashboard** — aggregated KPIs (avg scores, top concern), agent leaderboard, and
   AI-synthesized VoC themes across all visits.
5. **Persistence** — live recordings saved alongside seeded mock data to simulate a historical
   dataset.

## 5. Out of Scope (for prototype)
- User authentication / multi-tenant orgs
- Real database (using local JSON)
- Multi-property / multi-project support
- Mobile app (browser-based only)
- CRM integration

## 6. Tech Stack
- **Frontend:** Streamlit
- **AI Engine:** Google Gemini (`gemini-2.5-flash`), multimodal audio input
- **Storage:** Local JSON (`mock_data.json` + `data.json`)

## 7. Success Metrics (next phase)
- % of site visits with a recorded analysis
- Agent score improvement over time (coaching loop closes)
- Reduction in top VoC objection category quarter-over-quarter

## 8. Risks
- LLM scoring consistency/bias — needs periodic calibration against human reviewers
- Audio quality in field conditions (background noise) may affect transcript accuracy
- Model deprecations (Gemini model IDs change over time — pin and monitor)
