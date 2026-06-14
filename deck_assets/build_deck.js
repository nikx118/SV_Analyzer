const path = require("path");
const pptxgen = require("pptxgenjs");

const DIR = __dirname;
const img = (name) => path.join(DIR, name);

// ── Palette (derived from the live app's dark purple UI) ───────────────────
const BG = "15131F";       // deep purple-navy background
const CARD = "211D33";     // card / frame background
const VIOLET = "7C3AED";   // primary gradient color (header banner)
const PINK = "EC4899";     // secondary gradient color (header banner)
const RED = "FF4B4B";      // sharp accent (Streamlit red, active tab)
const TEXT = "F4F3FA";     // primary text
const MUTED = "A0A3BD";    // secondary / muted text
const GREEN = "34D399";    // good score
const AMBER = "FBBF24";    // medium score

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "BYTEBattle";
pres.title = "Site Visit Analyzer";

const FULL_W = 13.333;
const FULL_H = 7.5;

// ── Helpers ──────────────────────────────────────────────────────────────

function freshShadow() {
  return { type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.35 };
}

function addBackground(slide, color = BG) {
  slide.background = { color };
}

// Repeating motif: rounded violet badge with an emoji/icon, used before every section title
function addBadge(slide, emoji, x, y) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w: 0.62, h: 0.62, rectRadius: 0.14,
    fill: { color: VIOLET },
  });
  slide.addText(emoji, {
    x, y, w: 0.62, h: 0.62, align: "center", valign: "middle", fontSize: 24, margin: 0,
  });
}

function addTitle(slide, emoji, title, subtitle) {
  addBadge(slide, emoji, 0.6, 0.55);
  slide.addText(title, {
    x: 1.35, y: 0.48, w: 10.0, h: 0.55, fontSize: 28, bold: true, color: TEXT,
    fontFace: "Calibri", margin: 0, valign: "middle",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 1.35, y: 1.05, w: 11.3, h: 0.4, fontSize: 14, color: MUTED,
      fontFace: "Calibri", margin: 0,
    });
  }
}

function addPageTag(slide, text) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 11.55, y: 0.6, w: 1.55, h: 0.4, rectRadius: 0.2, fill: { color: CARD },
  });
  slide.addText(text, {
    x: 11.55, y: 0.6, w: 1.55, h: 0.4, align: "center", valign: "middle",
    fontSize: 11, color: MUTED, bold: true, margin: 0,
  });
}

function addFooter(slide, pageNum) {
  slide.addText("Site Visit Analyzer  ·  BYTEBattle", {
    x: 0.6, y: 7.05, w: 8, h: 0.3, fontSize: 9, color: MUTED, margin: 0,
  });
  slide.addText(String(pageNum), {
    x: 12.6, y: 7.05, w: 0.5, h: 0.3, fontSize: 9, color: MUTED, align: "right", margin: 0,
  });
}

// Screenshot placed inside a rounded "device frame" card, returns card bounds
function addScreenshot(slide, file, imgW, imgH, x, y) {
  const pad = 0.18;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: x - pad, y: y - pad, w: imgW + pad * 2, h: imgH + pad * 2, rectRadius: 0.08,
    fill: { color: CARD }, shadow: freshShadow(),
  });
  slide.addImage({ path: img(file), x, y, w: imgW, h: imgH });
}

// Standard feature-screenshot slide
function addFeatureSlide(opts) {
  const { pageNum, badge, featureTag, title, bullets, file, imgW, imgH, imageOnRight } = opts;
  const slide = pres.addSlide();
  addBackground(slide);
  addTitle(slide, badge, title);
  addPageTag(slide, featureTag);

  const contentY = 1.85;
  const contentH = 5.0;
  const cardW = imgW + 0.36;
  const cardH = imgH + 0.36;
  const cardY = contentY + (contentH - cardH) / 2;

  let imgX, textX, textW;
  if (imageOnRight) {
    imgX = FULL_W - 0.6 - cardW + 0.18;
    textX = 0.6;
    textW = imgX - 0.18 - 0.5 - textX;
  } else {
    imgX = 0.6 + 0.18;
    textX = imgX - 0.18 + cardW + 0.5;
    textW = FULL_W - 0.6 - textX;
  }

  addScreenshot(slide, file, imgW, imgH, imgX, cardY + 0.18);

  const bulletItems = bullets.map((b, i) => ({
    text: b, options: { bullet: { code: "2022", color: VIOLET }, color: TEXT, fontSize: 14.5, breakLine: i < bullets.length - 1, paraSpaceAfter: 12 },
  }));
  slide.addText(bulletItems, { x: textX, y: contentY + 0.3, w: textW, h: contentH - 0.6, valign: "middle", fontFace: "Calibri" });

  addFooter(slide, pageNum);
  return slide;
}

// ════════════════════════════════════════════════════════════════════════
// SLIDE 1 — Title
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);

  // Decorative corner circles (motif echo of the app's gradient header)
  slide.addShape(pres.shapes.OVAL, { x: 9.6, y: -2.2, w: 6.5, h: 6.5, fill: { color: VIOLET, transparency: 78 } });
  slide.addShape(pres.shapes.OVAL, { x: -2.5, y: 4.3, w: 5.5, h: 5.5, fill: { color: PINK, transparency: 85 } });

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.9, y: 2.55, w: 1.0, h: 1.0, rectRadius: 0.22, fill: { color: VIOLET },
  });
  slide.addText("🏡", { x: 0.9, y: 2.55, w: 1.0, h: 1.0, align: "center", valign: "middle", fontSize: 38, margin: 0 });

  slide.addText("Site Visit Analyzer", {
    x: 2.15, y: 2.45, w: 10.3, h: 1.0, fontSize: 46, bold: true, color: TEXT, fontFace: "Calibri", margin: 0, valign: "middle",
  });
  slide.addText("AI-powered sales coaching & Voice-of-Customer intelligence for real estate", {
    x: 2.15, y: 3.45, w: 10.0, h: 0.5, fontSize: 18, color: MUTED, fontFace: "Calibri", margin: 0,
  });

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 2.15, y: 4.25, w: 4.7, h: 0.5, rectRadius: 0.25, fill: { color: CARD },
  });
  slide.addText("📍  Pilot: Sunrise Residences · Whitefield, Bangalore", {
    x: 2.15, y: 4.25, w: 4.7, h: 0.5, align: "center", valign: "middle", fontSize: 13, color: TEXT, margin: 0,
  });

  slide.addText("Prototype  ·  Team BYTEBattle", {
    x: 0.9, y: 6.9, w: 6, h: 0.4, fontSize: 12, color: MUTED, margin: 0,
  });
}

// ════════════════════════════════════════════════════════════════════════
// SLIDE 2 — The Problem
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);
  addTitle(slide, "⚠️", "Every site visit is a goldmine of data — and today it's all lost");
  addPageTag(slide, "The Problem");

  const items = [
    { icon: "🎙️", title: "Conversations vanish", desc: "Agent pitches, customer objections, and on-the-spot feedback are never captured after the visit ends." },
    { icon: "🧑‍🏫", title: "No objective coaching", desc: "Sales managers can't tell why a deal was won or lost, or which agents need help with which skills." },
    { icon: "📊", title: "No aggregated signal", desc: "Developers have no structured view of why leads hesitate — price, timelines, trust, or location." },
  ];

  const colW = 3.85;
  const gap = 0.35;
  const startX = 0.6;
  items.forEach((it, i) => {
    const x = startX + i * (colW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 2.0, w: colW, h: 3.9, rectRadius: 0.1, fill: { color: CARD }, shadow: freshShadow(),
    });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x + 0.35, y: 2.4, w: 0.8, h: 0.8, rectRadius: 0.18, fill: { color: VIOLET },
    });
    slide.addText(it.icon, { x: x + 0.35, y: 2.4, w: 0.8, h: 0.8, align: "center", valign: "middle", fontSize: 30, margin: 0 });
    slide.addText(it.title, {
      x: x + 0.35, y: 3.4, w: colW - 0.7, h: 0.7, fontSize: 18, bold: true, color: TEXT, margin: 0, fontFace: "Calibri",
    });
    slide.addText(it.desc, {
      x: x + 0.35, y: 4.1, w: colW - 0.7, h: 1.6, fontSize: 13.5, color: MUTED, margin: 0, fontFace: "Calibri", valign: "top",
    });
  });

  slide.addText([
    { text: "The result: ", options: { bold: true, color: TEXT } },
    { text: "decisions about coaching, pricing, and product positioning are made on gut feel instead of evidence.", options: { color: MUTED } },
  ], { x: 0.6, y: 6.15, w: 12.1, h: 0.6, fontSize: 14, fontFace: "Calibri", margin: 0 });

  addFooter(slide, 2);
}

// ════════════════════════════════════════════════════════════════════════
// SLIDE 3 — How It Works
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);
  addTitle(slide, "✨", "From a 2-minute voice note to coaching + market intelligence");
  addPageTag(slide, "How It Works");

  const steps = [
    { n: "1", icon: "🎙️", title: "Record", desc: "Agent records a short voice summary right after the site visit, in-browser." },
    { n: "2", icon: "🤖", title: "AI Analysis", desc: "Gemini 2.5 listens to the raw audio — tone, content, and objections — not just a transcript." },
    { n: "3", icon: "📈", title: "Instant Coaching", desc: "Agent gets a 5-pillar scorecard, transcript, and one actionable coaching tip." },
    { n: "4", icon: "🗣️", title: "Aggregated VoC", desc: "Developers see synthesized customer themes across every visit, ranked by priority." },
  ];

  const colW = 2.85;
  const gap = 0.28;
  const startX = 0.6;
  const y = 2.3;
  steps.forEach((s, i) => {
    const x = startX + i * (colW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w: colW, h: 4.1, rectRadius: 0.1, fill: { color: CARD }, shadow: freshShadow(),
    });
    slide.addShape(pres.shapes.OVAL, { x: x + colW / 2 - 0.45, y: y + 0.35, w: 0.9, h: 0.9, fill: { color: VIOLET } });
    slide.addText(s.icon, { x: x + colW / 2 - 0.45, y: y + 0.35, w: 0.9, h: 0.9, align: "center", valign: "middle", fontSize: 32, margin: 0 });
    slide.addShape(pres.shapes.OVAL, { x: x + colW - 0.55, y: y + 0.15, w: 0.42, h: 0.42, fill: { color: RED } });
    slide.addText(s.n, { x: x + colW - 0.55, y: y + 0.15, w: 0.42, h: 0.42, align: "center", valign: "middle", fontSize: 14, bold: true, color: TEXT, margin: 0 });
    slide.addText(s.title, {
      x, y: y + 1.45, w: colW, h: 0.5, align: "center", fontSize: 18, bold: true, color: TEXT, margin: 0, fontFace: "Calibri",
    });
    slide.addText(s.desc, {
      x: x + 0.25, y: y + 2.0, w: colW - 0.5, h: 1.9, align: "center", fontSize: 13, color: MUTED, margin: 0, fontFace: "Calibri",
    });
    if (i < steps.length - 1) {
      slide.addText("›", { x: x + colW, y: y + 1.6, w: gap, h: 0.6, align: "center", fontSize: 28, bold: true, color: VIOLET, margin: 0 });
    }
  });

  addFooter(slide, 3);
}

// ════════════════════════════════════════════════════════════════════════
// SLIDE 4 — Target Personas
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);
  addTitle(slide, "🎯", "Built for two audiences, in one product");
  addPageTag(slide, "Who It's For");

  const personas = [
    {
      icon: "🧑‍💼", title: "Sales Agent", color: VIOLET,
      quote: "“How did I perform? What should I do differently with this lead?”",
      bullets: ["Instant, judgment-free scorecard after every visit", "One concrete coaching tip to apply on the next call", "Tracks personal performance over time on the leaderboard"],
    },
    {
      icon: "🏗️", title: "Developer / Sales Manager", color: PINK,
      quote: "“Across all visits, why are customers hesitating — price, location, or agent knowledge?”",
      bullets: ["Team-wide KPIs and pillar performance at a glance", "Agent leaderboard to identify coaching priorities", "AI-synthesized Voice-of-Customer themes for product decisions"],
    },
  ];

  const colW = 5.85;
  const gap = 0.6;
  const startX = 0.6;
  personas.forEach((p, i) => {
    const x = startX + i * (colW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 1.95, w: colW, h: 4.95, rectRadius: 0.12, fill: { color: CARD }, shadow: freshShadow(),
    });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x + 0.4, y: 2.35, w: 0.9, h: 0.9, rectRadius: 0.2, fill: { color: p.color },
    });
    slide.addText(p.icon, { x: x + 0.4, y: 2.35, w: 0.9, h: 0.9, align: "center", valign: "middle", fontSize: 34, margin: 0 });
    slide.addText(p.title, {
      x: x + 1.5, y: 2.35, w: colW - 1.9, h: 0.9, valign: "middle", fontSize: 22, bold: true, color: TEXT, margin: 0, fontFace: "Calibri",
    });
    slide.addText(p.quote, {
      x: x + 0.4, y: 3.45, w: colW - 0.8, h: 0.95, italic: true, fontSize: 14, color: MUTED, margin: 0, fontFace: "Calibri",
    });
    const bulletItems = p.bullets.map((b, j) => ({
      text: b, options: { bullet: { code: "2022", color: p.color }, color: TEXT, fontSize: 14, breakLine: j < p.bullets.length - 1, paraSpaceAfter: 10 },
    }));
    slide.addText(bulletItems, { x: x + 0.4, y: 4.55, w: colW - 0.8, h: 2.2, fontFace: "Calibri" });
  });

  addFooter(slide, 4);
}

// ════════════════════════════════════════════════════════════════════════
// SLIDES 5–9 — Features with real product screenshots
// ════════════════════════════════════════════════════════════════════════

addFeatureSlide({
  pageNum: 5, badge: "🎙️", featureTag: "Feature 1 / 5",
  title: "One-click audio capture, right in the browser",
  bullets: [
    "Agent records a short spoken summary immediately after the visit — no app install, no extra hardware.",
    "Captures agent name and lead name alongside the recording for clean tracking.",
    "Built-in guidance prompts the agent to mention the pitch, objections raised, and how they were handled.",
  ],
  file: "screen1.png", imgW: 7.0, imgH: 3.5, imageOnRight: true,
});

addFeatureSlide({
  pageNum: 6, badge: "📈", featureTag: "Feature 2 / 5",
  title: "Multimodal AI scoring across 5 coaching pillars",
  bullets: [
    "Google Gemini listens to the raw audio — tone, pacing, and confidence — not just a text transcript.",
    "Scores every visit on Tonality & Pitch, Product Information, Product Knowledge, Objection Handling, and Rapport Building.",
    "Returns a full transcript, an overall score, and one specific, actionable coaching tip.",
    "Automatically extracts customer objections and positive signals from the conversation.",
  ],
  file: "screen5.png", imgW: 6.6, imgH: 3.7125, imageOnRight: false,
});

addFeatureSlide({
  pageNum: 7, badge: "📊", featureTag: "Feature 3 / 5",
  title: "Developer dashboard with real-time team KPIs",
  bullets: [
    "Aggregates every recorded visit into a single live view for sales managers and developers.",
    "Tracks total site visits, average overall score, and average objection-handling performance.",
    "Surfaces the single biggest customer concern across the whole pipeline — automatically.",
  ],
  file: "screen2.png", imgW: 7.5, imgH: 2.696, imageOnRight: true,
});

addFeatureSlide({
  pageNum: 8, badge: "🏆", featureTag: "Feature 4 / 5",
  title: "Pillar performance breakdown & agent leaderboard",
  bullets: [
    "Visualizes the team's average score on each of the 5 coaching pillars to spot systemic strengths and gaps.",
    "Ranks agents by overall score, turning every recording into a friendly performance leaderboard.",
    "Helps managers target coaching where it matters most — e.g. objection handling vs. rapport.",
  ],
  file: "screen3.png", imgW: 7.0, imgH: 3.5, imageOnRight: false,
});

addFeatureSlide({
  pageNum: 9, badge: "🗣️", featureTag: "Feature 5 / 5",
  title: "AI-synthesized Voice of Customer, ranked by priority",
  bullets: [
    "Gemini reads every customer objection collected across all visits and groups them into recurring themes.",
    "Each theme gets a priority level, a mention count, a description, and a real supporting quote.",
    "An executive summary gives product and leadership teams a one-paragraph read on customer sentiment.",
  ],
  file: "screen4.png", imgW: 6.6, imgH: 3.7125, imageOnRight: true,
});

// ════════════════════════════════════════════════════════════════════════
// SLIDE 10 — Tech Stack
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);
  addTitle(slide, "🛠️", "A lean stack, built to move from prototype to pilot fast");
  addPageTag(slide, "Tech Stack");

  const stack = [
    { icon: "🖥️", title: "Frontend", desc: "Streamlit — a fast, Python-native UI for both the Agent and Developer dashboards." },
    { icon: "🤖", title: "AI Engine", desc: "Google Gemini 2.5 Flash — multimodal model that analyzes audio directly for transcript + scoring." },
    { icon: "💾", title: "Storage", desc: "Local JSON files for live and mock data — simple, transparent, and easy to swap for a real database." },
  ];

  const colW = 3.85;
  const gap = 0.35;
  const startX = 0.6;
  stack.forEach((s, i) => {
    const x = startX + i * (colW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 2.0, w: colW, h: 3.0, rectRadius: 0.1, fill: { color: CARD }, shadow: freshShadow(),
    });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x + 0.35, y: 2.35, w: 0.8, h: 0.8, rectRadius: 0.18, fill: { color: VIOLET },
    });
    slide.addText(s.icon, { x: x + 0.35, y: 2.35, w: 0.8, h: 0.8, align: "center", valign: "middle", fontSize: 30, margin: 0 });
    slide.addText(s.title, {
      x: x + 0.35, y: 3.35, w: colW - 0.7, h: 0.5, fontSize: 18, bold: true, color: TEXT, margin: 0, fontFace: "Calibri",
    });
    slide.addText(s.desc, {
      x: x + 0.35, y: 3.9, w: colW - 0.7, h: 1.0, fontSize: 13.5, color: MUTED, margin: 0, fontFace: "Calibri",
    });
  });

  slide.addText("Why it matters: every layer is replaceable without a rewrite — swap JSON for Postgres, or add a CRM integration, without touching the AI pipeline.", {
    x: 0.6, y: 5.4, w: 12.1, h: 0.8, fontSize: 14, color: MUTED, italic: true, margin: 0, fontFace: "Calibri",
  });

  addFooter(slide, 10);
}

// ════════════════════════════════════════════════════════════════════════
// SLIDE 11 — Success Metrics & Roadmap
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);
  addTitle(slide, "🚀", "Measuring impact, and what comes next");
  addPageTag(slide, "What's Next");

  // Left: Success metrics
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.6, y: 1.95, w: 5.95, h: 4.95, rectRadius: 0.12, fill: { color: CARD }, shadow: freshShadow(),
  });
  slide.addText("📏  Success Metrics", {
    x: 1.0, y: 2.25, w: 5.2, h: 0.5, fontSize: 18, bold: true, color: TEXT, margin: 0, fontFace: "Calibri",
  });
  const metrics = [
    "% of site visits with a recorded analysis",
    "Agent score improvement over time — does the coaching loop close?",
    "Reduction in the top VoC objection category, quarter over quarter",
  ];
  slide.addText(metrics.map((m, i) => ({
    text: m, options: { bullet: { code: "2022", color: VIOLET }, color: TEXT, fontSize: 14.5, breakLine: i < metrics.length - 1, paraSpaceAfter: 14 },
  })), { x: 1.0, y: 2.95, w: 5.2, h: 3.6, fontFace: "Calibri" });

  // Right: Roadmap
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 6.78, y: 1.95, w: 5.95, h: 4.95, rectRadius: 0.12, fill: { color: CARD }, shadow: freshShadow(),
  });
  slide.addText("🗺️  Roadmap", {
    x: 7.18, y: 2.25, w: 5.2, h: 0.5, fontSize: 18, bold: true, color: TEXT, margin: 0, fontFace: "Calibri",
  });
  const roadmap = [
    "Move from local JSON to a shared database for multi-agent, multi-property use",
    "Multi-property / multi-project support for developers with several launches",
    "CRM integration to push coaching scores and VoC themes into existing workflows",
    "Mobile-friendly recording flow for agents in the field",
  ];
  slide.addText(roadmap.map((m, i) => ({
    text: m, options: { bullet: { code: "2022", color: PINK }, color: TEXT, fontSize: 14.5, breakLine: i < roadmap.length - 1, paraSpaceAfter: 12 },
  })), { x: 7.18, y: 2.95, w: 5.2, h: 3.6, fontFace: "Calibri" });

  addFooter(slide, 11);
}

// ════════════════════════════════════════════════════════════════════════
// SLIDE 12 — Thank You / CTA
// ════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  addBackground(slide);

  slide.addShape(pres.shapes.OVAL, { x: -2.5, y: -2.5, w: 6.5, h: 6.5, fill: { color: VIOLET, transparency: 78 } });
  slide.addShape(pres.shapes.OVAL, { x: 9.8, y: 4.0, w: 5.5, h: 5.5, fill: { color: PINK, transparency: 85 } });

  slide.addText("Let's turn every site visit\ninto a coaching + insight engine", {
    x: 0.9, y: 2.3, w: 11.5, h: 1.8, fontSize: 38, bold: true, color: TEXT, fontFace: "Calibri", margin: 0, lineSpacingMultiple: 1.15,
  });
  slide.addText("Site Visit Analyzer  ·  Prototype  ·  Team BYTEBattle", {
    x: 0.9, y: 4.3, w: 11.5, h: 0.5, fontSize: 16, color: MUTED, fontFace: "Calibri", margin: 0,
  });

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.9, y: 5.1, w: 5.3, h: 0.55, rectRadius: 0.27, fill: { color: CARD },
  });
  slide.addText("📍  Pilot: Sunrise Residences · Whitefield, Bangalore", {
    x: 0.9, y: 5.1, w: 5.3, h: 0.55, align: "center", valign: "middle", fontSize: 13, color: TEXT, margin: 0,
  });
}

pres.writeFile({ fileName: path.join(DIR, "Site_Visit_Analyzer_Sales_Deck.pptx") }).then(() => {
  console.log("done");
});
