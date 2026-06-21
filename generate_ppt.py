const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "PortfolioAI – Week 1 Report";

// ─── COLOR PALETTE ─────────────────────────────────────────────
const C = {
  navy: "0D1B2A",
  navyMid: "1A2F47",
  blue: "2E86C1",
  ice: "A9CCE3",
  white: "FFFFFF",
  gold: "F4C842",
  grey: "7F8C8D",
  lightbg: "EAF2FB",
  darktext: "1A2F47",
};

const FOOTER_Y = 5.1;

// ─── FOOTER ───────────────────────────────────────────────────
function addFooter(slide, presenter, id) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: FOOTER_Y,
    w: 10,
    h: 0.525,
    fill: { color: C.navyMid },
    line: { color: C.navyMid },
  });

  slide.addText(
    `Presented by: ${presenter} · ${id}`,
    {
      x: 0.4,
      y: FOOTER_Y + 0.05,
      w: 5.5,
      h: 0.42,
      fontSize: 10,
      color: C.ice,
    }
  );

  slide.addText(
    "PortfolioAI · AI Project · CUST · June 2026",
    {
      x: 4.5,
      y: FOOTER_Y + 0.05,
      w: 5.1,
      h: 0.42,
      fontSize: 9,
      color: C.grey,
      align: "right",
    }
  );
}

// ─── TITLE HELPER ─────────────────────────────────────────────
function slideTitle(slide, num, label, subtitle) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5,
    y: 0.38,
    w: 0.45,
    h: 0.45,
    fill: { color: C.blue },
  });

  slide.addText(`0${num}`, {
    x: 0.5,
    y: 0.38,
    w: 0.45,
    h: 0.45,
    fontSize: 13,
    bold: true,
    color: C.white,
    align: "center",
  });

  slide.addText(label, {
    x: 1.1,
    y: 0.35,
    w: 8.5,
    h: 0.5,
    fontSize: 22,
    bold: true,
    color: C.navy,
  });

  if (subtitle) {
    slide.addText(subtitle, {
      x: 1.1,
      y: 0.83,
      w: 8.5,
      h: 0.32,
      fontSize: 12,
      color: C.blue,
      italic: true,
    });
  }
}

// ─────────────────────────────────────────────────────────────
// SLIDE 1 — TITLE
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 0,
    w: 0.18,
    h: 5.625,
    fill: { color: C.blue },
  });

  s.addText("WEEK 1 DELIVERABLE", {
    x: 8.1,
    y: 0.25,
    w: 1.6,
    h: 0.38,
    fontSize: 9,
    bold: true,
    color: C.white,
    align: "center",
  });

  s.addText("PortfolioAI", {
    x: 0.5,
    y: 0.85,
    w: 9,
    h: 1.1,
    fontSize: 56,
    bold: true,
    color: C.white,
  });

  s.addText(
    "AI-Based Long-Term Investment Advisory\n& Portfolio Optimization System",
    {
      x: 0.5,
      y: 1.9,
      w: 9,
      h: 0.9,
      fontSize: 18,
      color: C.ice,
    }
  );

  const students = [
    { name: "Muhammad Omer", id: "BCS233066", role: "Data Engineer" },
    { name: "Saeed Ur Rehman", id: "BCS233057", role: "UI & Visualization" },
    { name: "Azan Zafar", id: "BCS231065", role: "AI Optimization" },
  ];

  students.forEach((st, i) => {
    const x = 0.5 + i * 3.1;

    s.addShape(pres.shapes.RECTANGLE, {
      x,
      y: 4.2,
      w: 2.85,
      h: 1.05,
      fill: { color: C.navyMid },
    });

    s.addText(st.name, {
      x: x + 0.1,
      y: 4.45,
      w: 2.7,
      h: 0.3,
      fontSize: 12,
      color: C.white,
      bold: true,
    });

    s.addText(`${st.id} · ${st.role}`, {
      x: x + 0.1,
      y: 4.8,
      w: 2.7,
      h: 0.25,
      fontSize: 9,
      color: C.ice,
    });
  });
}

// ─────────────────────────────────────────────────────────────
// SLIDE 2 — PROBLEM
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightbg };

  slideTitle(s, 1, "Problem Definition", "What are we building?");

  s.addText(
    "Individual investors lack access to intelligent portfolio advisory tools.",
    {
      x: 0.5,
      y: 1.5,
      w: 4.5,
      fontSize: 11,
      color: C.darktext,
    }
  );

  const objectives = [
    "Model investment decisions as AI optimization",
    "Heuristic scoring system",
    "Hill Climbing & Simulated Annealing",
    "Explainable recommendations",
  ];

  objectives.forEach((o, i) => {
    s.addText(`• ${o}`, {
      x: 5.5,
      y: 1.5 + i * 0.5,
      w: 4,
      fontSize: 11,
      color: C.darktext,
    });
  });

  addFooter(s, "Muhammad Omer", "BCS233066");
}

// ─────────────────────────────────────────────────────────────
// SLIDE 3 — DATASET
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightbg };

  slideTitle(s, 2, "Dataset Collection", "Financial Data Sources");

  const sources = ["Yahoo Finance", "PSX Data", "Annual Reports"];

  sources.forEach((src, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5 + i * 3,
      y: 1.5,
      w: 2.8,
      h: 1.2,
      fill: { color: C.white },
    });

    s.addText(src, {
      x: 0.6 + i * 3,
      y: 1.8,
      w: 2.5,
      fontSize: 12,
      color: C.darktext,
    });
  });

  addFooter(s, "Muhammad Omer", "BCS233066");
}

// ─────────────────────────────────────────────────────────────
// SLIDE 4 — FEATURES
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightbg };

  slideTitle(s, 3, "Stock Features", "AI Input Variables");

  const features = [
    "Growth Rate",
    "Volatility",
    "Dividend Yield",
    "Sector",
  ];

  features.forEach((f, i) => {
    s.addText(`• ${f}`, {
      x: 0.5,
      y: 1.5 + i * 0.5,
      fontSize: 12,
      color: C.darktext,
    });
  });

  addFooter(s, "Muhammad Omer", "BCS233066");
}

// ─────────────────────────────────────────────────────────────
// SLIDE 5 — HEURISTIC
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  slideTitle(s, 4, "Heuristic Scoring", "AI Decision System");

  const weights = [
    "Growth 30%",
    "Risk 20%",
    "Dividend 15%",
    "Momentum 15%",
  ];

  weights.forEach((w, i) => {
    s.addText(`• ${w}`, {
      x: 0.5,
      y: 1.5 + i * 0.5,
      fontSize: 12,
      color: C.ice,
    });
  });

  addFooter(s, "Saeed Ur Rehman", "BCS233057");
}

// ─────────────────────────────────────────────────────────────
// SLIDE 6 — UI
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightbg };

  slideTitle(s, 5, "UI Design", "Streamlit Dashboard");

  const pages = ["Profile", "Recommendations", "Optimizer", "Dashboard"];

  pages.forEach((p, i) => {
    s.addText(`${i + 1}. ${p}`, {
      x: 0.5,
      y: 1.5 + i * 0.5,
      fontSize: 12,
      color: C.darktext,
    });
  });

  addFooter(s, "Saeed Ur Rehman", "BCS233057");
}

// ─────────────────────────────────────────────────────────────
// SLIDE 7 — MOCKUP
// ─────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.lightbg };

  slideTitle(s, 6, "UI Mockups", "Application Preview");

  const screens = [
    "Investor Profile",
    "Recommendations",
    "Optimizer",
    "Dashboard",
  ];

  screens.forEach((sc, i) => {
    const x = i % 2 === 0 ? 0.5 : 5.2;
    const y = i < 2 ? 1.5 : 3.2;

    s.addShape(pres.shapes.RECTANGLE, {
      x,
      y,
      w: 4,
      h: 1.5,
      fill: { color: C.navyMid },
    });

    s.addText(sc, {
      x,
      y: y + 0.5,
      w: 4,
      fontSize: 12,
      color: C.white,
      align: "center",
    });
  });

  addFooter(s, "Saeed Ur Rehman", "BCS233057");
}

// ─────────────────────────────────────────────────────────────
// EXPORT PPT
// ─────────────────────────────────────────────────────────────
pres.writeFile("PortfolioAI_Week1_Report.pptx");
console.log("PPT Generated Successfully!");