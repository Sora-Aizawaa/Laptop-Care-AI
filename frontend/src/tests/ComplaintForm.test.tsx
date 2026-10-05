import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import ComplaintForm from "../components/ComplaintForm";

describe("ComplaintForm", () => {
  it("renders the heading and textarea", () => {
    render(<ComplaintForm onSubmit={vi.fn()} onStartGuided={vi.fn()} />);
    expect(screen.getByText(/how can we help/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/my laptop becomes very hot/i)).toBeInTheDocument();
  });

  it("shows a validation message when submitting empty text", async () => {
    const user = userEvent.setup();
    render(<ComplaintForm onSubmit={vi.fn()} onStartGuided={vi.fn()} />);
    await user.click(screen.getByRole("button", { name: /analyze problem/i }));
    expect(screen.getByText(/please describe what is happening/i)).toBeInTheDocument();
  });

  it("calls onSubmit with the entered text", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<ComplaintForm onSubmit={onSubmit} onStartGuided={vi.fn()} />);
    await user.type(screen.getByPlaceholderText(/my laptop becomes very hot/i), "Laptop panas");
    await user.click(screen.getByRole("button", { name: /analyze problem/i }));
    expect(onSubmit).toHaveBeenCalledWith("Laptop panas");
  });

  it("calls onStartGuided when the guided link is clicked", async () => {
    const user = userEvent.setup();
    const onStartGuided = vi.fn();
    render(<ComplaintForm onSubmit={vi.fn()} onStartGuided={onStartGuided} />);
    await user.click(screen.getByText(/start guided troubleshooting/i));
    expect(onStartGuided).toHaveBeenCalled();
  });

  it("disables the textarea and button while disabled prop is true", () => {
    render(<ComplaintForm onSubmit={vi.fn()} onStartGuided={vi.fn()} disabled />);
    expect(screen.getByPlaceholderText(/my laptop becomes very hot/i)).toBeDisabled();
    expect(screen.getByRole("button", { name: /analyze problem/i })).toBeDisabled();
  });
});
