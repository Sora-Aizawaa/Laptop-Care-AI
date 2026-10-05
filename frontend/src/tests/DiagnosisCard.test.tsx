import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import DiagnosisCard from "../components/DiagnosisCard";
import type { DiagnosisResponse } from "../types/diagnosis";

const baseResult: DiagnosisResponse = {
  diagnosis_id: 1,
  diagnosis: {
    problem: "Overheating",
    category: "Hardware",
    confidence: 0.91,
    is_low_confidence: false,
  },
  priority: "HIGH",
  estimated_time: "1-2 hours",
  possible_causes: ["Dust accumulation", "Degraded thermal paste"],
  reasoning: ["High temperature reported", "Automatic shutdown reported"],
  troubleshooting_steps: [],
  safety_warning: "Stop using the laptop and seek professional inspection.",
  follow_up_questions: [],
  top_predictions: { overheating: 0.91, wifi_problem: 0.03 },
};

describe("DiagnosisCard", () => {
  it("renders the problem name and confidence", () => {
    render(<DiagnosisCard result={baseResult} />);
    expect(screen.getByText("Overheating")).toBeInTheDocument();
    expect(screen.getByText("91%")).toBeInTheDocument();
  });

  it("renders reasoning (explainability)", () => {
    render(<DiagnosisCard result={baseResult} />);
    expect(screen.getByText(/high temperature reported/i)).toBeInTheDocument();
  });

  it("renders the safety warning when present", () => {
    render(<DiagnosisCard result={baseResult} />);
    expect(screen.getByText(/safety notice/i)).toBeInTheDocument();
  });

  it("hides technician predictions by default", () => {
    render(<DiagnosisCard result={baseResult} />);
    expect(screen.queryByText(/technician view/i)).not.toBeInTheDocument();
  });

  it("shows technician predictions when technicianMode is true", () => {
    render(<DiagnosisCard result={baseResult} technicianMode />);
    expect(screen.getByText(/technician view/i)).toBeInTheDocument();
  });
});
