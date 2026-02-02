/**
 * Tests for PriorityBadge component.
 *
 * Reference: T151 - Run all frontend tests
 */

import { render, screen } from "@testing-library/react";
import { PriorityBadge } from "@/components/ui/PriorityBadge";

describe("PriorityBadge", () => {
  it("renders high priority with correct styling", () => {
    render(<PriorityBadge priority="high" />);
    const badge = screen.getByText("High");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass("bg-red-100", "text-red-800");
  });

  it("renders medium priority with correct styling", () => {
    render(<PriorityBadge priority="medium" />);
    const badge = screen.getByText("Medium");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass("bg-yellow-100", "text-yellow-800");
  });

  it("renders low priority with correct styling", () => {
    render(<PriorityBadge priority="low" />);
    const badge = screen.getByText("Low");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass("bg-green-100", "text-green-800");
  });

  it("applies additional className when provided", () => {
    render(<PriorityBadge priority="high" className="custom-class" />);
    const badge = screen.getByText("High");
    expect(badge).toHaveClass("custom-class");
  });
});
