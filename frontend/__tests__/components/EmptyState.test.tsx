/**
 * Tests for EmptyState component.
 *
 * Reference: T151 - Run all frontend tests
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { EmptyState } from "@/components/ui/EmptyState";

describe("EmptyState", () => {
  it("renders title and description", () => {
    render(
      <EmptyState title="No tasks yet" description="Create your first task." />
    );
    expect(screen.getByText("No tasks yet")).toBeInTheDocument();
    expect(screen.getByText("Create your first task.")).toBeInTheDocument();
  });

  it("renders custom icon when provided", () => {
    render(
      <EmptyState
        title="Empty"
        description="Nothing here"
        icon={<svg data-testid="custom-icon" />}
      />
    );
    expect(screen.getByTestId("custom-icon")).toBeInTheDocument();
  });

  it("renders action button when provided", () => {
    const handleClick = jest.fn();
    render(
      <EmptyState
        title="No items"
        description="Add something"
        action={{ label: "Add Item", onClick: handleClick }}
      />
    );
    const button = screen.getByText("Add Item");
    expect(button).toBeInTheDocument();
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("does not render action button when not provided", () => {
    render(<EmptyState title="Empty" description="Nothing here" />);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
});
