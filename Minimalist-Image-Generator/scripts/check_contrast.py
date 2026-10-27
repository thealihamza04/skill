#!/usr/bin/env python3
"""WCAG contrast ratio checker for two hex colors.

Usage: python3 check_contrast.py <fg_hex> <bg_hex>
Example: python3 check_contrast.py "#8a8f98" "#08090a"

Prints the contrast ratio and whether it passes common thresholds
(4.5:1 for body/caption text, 3:1 for large headlines/shapes).
"""

import sys


def _linearize(channel):
    c = channel / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"expected a 6-digit hex color, got {hex_color!r}")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = _linearize(r), _linearize(g), _linearize(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex_a, hex_b):
    l1, l2 = relative_luminance(hex_a), relative_luminance(hex_b)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    fg, bg = sys.argv[1], sys.argv[2]
    ratio = contrast_ratio(fg, bg)

    print(f"{fg} on {bg}: {ratio:.2f}:1")
    print(f"  body/caption text (needs 4.5:1): {'PASS' if ratio >= 4.5 else 'FAIL'}")
    print(f"  large headline/shape (needs 3:1): {'PASS' if ratio >= 3 else 'FAIL'}")


if __name__ == "__main__":
    main()
