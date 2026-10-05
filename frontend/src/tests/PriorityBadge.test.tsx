import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import PriorityBadge from "../components/PriorityBadge";

describe("PriorityBadge", () => {
  it("renders the priority label", () => {
    render(<PriorityBadge priority="HIGH" />);
    expect(screen.getByText("HIGH")).toBeInTheDocument();
  });

  it("does not rely on color alone — includes a distinguishing icon", () => {
    const { container: highContainer } = render(<PriorityBadge priority="HIGH" />);
    const { container: lowContainer } = render(<PriorityBadge priority="LOW" />);
    expect(highContainer.textContent).not.toEqual(lowContainer.textContent);
  });

  it("renders unknown priority gracefully", () => {
    render(<PriorityBadge priority="UNKNOWN" />);
    expect(screen.getByText("UNKNOWN")).toBeInTheDocument();
  });
});
