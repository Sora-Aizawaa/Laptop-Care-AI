import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import LoadingDiagnosis from "../components/LoadingDiagnosis";

describe("LoadingDiagnosis", () => {
  it("renders the main loading heading", () => {
    render(<LoadingDiagnosis />);
    expect(screen.getByText(/analyzing your laptop problem/i)).toBeInTheDocument();
  });

  it("renders a rotating status message", () => {
    render(<LoadingDiagnosis />);
    expect(screen.getByText(/understanding symptoms/i)).toBeInTheDocument();
  });
});
