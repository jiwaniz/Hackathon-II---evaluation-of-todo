/**
 * Tests for utility functions.
 *
 * Reference: T151 - Run all frontend tests
 */

import { cn, formatDate, truncate } from "../../lib/utils";

describe("cn utility", () => {
  it("merges class names correctly", () => {
    expect(cn("a", "b")).toBe("a b");
  });

  it("handles conditional classes", () => {
    expect(cn("base", false && "hidden", true && "visible")).toBe("base visible");
  });

  it("handles undefined and null", () => {
    expect(cn("base", undefined, null)).toBe("base");
  });

  it("merges Tailwind classes correctly", () => {
    expect(cn("p-4", "p-2")).toBe("p-2");
  });
});

describe("formatDate utility", () => {
  it("formats date string correctly", () => {
    const date = "2024-01-15T10:30:00Z";
    const formatted = formatDate(date);
    expect(formatted).toContain("2024");
  });

  it("handles Date object", () => {
    const date = new Date("2024-06-20T15:45:00Z");
    const formatted = formatDate(date);
    expect(formatted).toBeTruthy();
  });
});

describe("truncate utility", () => {
  it("truncates long text", () => {
    const text = "This is a very long string that should be truncated";
    const result = truncate(text, 20);
    expect(result).toHaveLength(20);
    expect(result.endsWith("...")).toBe(true);
  });

  it("does not truncate short text", () => {
    const text = "Short text";
    expect(truncate(text, 20)).toBe("Short text");
  });

  it("handles exact length", () => {
    const text = "Exactly twenty chars";
    expect(truncate(text, 20)).toBe("Exactly twenty chars");
  });
});
