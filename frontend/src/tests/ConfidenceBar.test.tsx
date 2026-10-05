import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import ConfidenceBar from "../components/ConfidenceBar";

describe("ConfidenceBar", () => {
  it("renders the confidence percentage", () => {
    render(<ConfidenceBar confidence={0.91} />);
    expect(screen.getByText("91%")).toBeInTheDocument();
  });

  it("rounds the percentage correctly", () => {
    render(<ConfidenceBar confidence={0.556} />);
    expect(screen.getByText("56%")).toBeInTheDocument();
  });

  it("clamps values above 1", () => {
    render(<ConfidenceBar confidence={1.5} />);
    expect(screen.getByText("150%")).toBeInTheDocument();
  });
});
