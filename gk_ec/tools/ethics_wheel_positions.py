#!/usr/bin/env python3
"""Calculate ethics wheel positions for a 5-axis (10-division) layout.

Vanilla geometry (4 axes, 8 divisions):
  - Container: 230x230, icon positions are top-left corner of 29x29 sprites
  - Inner ring (regular): effective radius ~45px from visual center
  - Outer ring (fanatic): effective radius ~80px from visual center
  - Gap: ~35px
  - Gestalt at visual center of wheel

With 5 axes we need wider inner radius to maintain button spacing.
"""

import math

# --- Configuration ---

ICON_SIZE = 29  # Ethics icons are 29x29 px
ICON_OFFSET = ICON_SIZE // 2  # 14px — subtract from center to get top-left

# Radii (vanilla: inner=45, outer=80, gap=35)
INNER_RADIUS = 55   # Wider than vanilla 45 to fit 10 divisions
OUTER_RADIUS = 90   # inner + 35 gap (same as vanilla)

# Container size — visual center will be at (W//2, H//2)
# Positions need enough room for outer ring + half icon size
# Minimum: 2 * (OUTER_RADIUS + ICON_OFFSET) = 2 * 104 = 208
CONTAINER_W = 240
CONTAINER_H = 240
CENTER_X = CONTAINER_W // 2
CENTER_Y = CONTAINER_H // 2

# Axes ordered clockwise from top (first ethic is top-half, second is bottom-half)
# Vanilla order: mil, xph, egal, mat | pac, xpl, auth, spirit
# New axis (ind/col) inserted between mil and xph
AXES = [
    ("militarist",   "pacifist"),
    ("individualist",   "collectivist"),       # NEW — inserted between mil and xph
    ("xenophobe",    "xenophile"),
    ("egalitarian",  "authoritarian"),
    ("materialist",  "spiritualist"),
]

# Starting angle: 90° = top of wheel (screen Y is inverted)
START_ANGLE_DEG = 90

# --- Calculation ---

N_AXES = len(AXES)
N_DIVISIONS = N_AXES * 2
ANGLE_STEP = 360.0 / N_DIVISIONS

def center_pos(radius, angle_deg):
    """Get visual center position for a given radius and angle."""
    a = math.radians(angle_deg)
    x = CENTER_X + radius * math.cos(a)
    y = CENTER_Y - radius * math.sin(a)  # Screen Y is inverted
    return (x, y)

def topleft_pos(radius, angle_deg):
    """Get top-left corner position (for GUI) from visual center."""
    cx, cy = center_pos(radius, angle_deg)
    return (round(cx - ICON_OFFSET), round(cy - ICON_OFFSET))

print(f"Container: {CONTAINER_W}x{CONTAINER_H}, Center: ({CENTER_X}, {CENTER_Y})")
print(f"Inner: {INNER_RADIUS}px, Outer: {OUTER_RADIUS}px, Gap: {OUTER_RADIUS - INNER_RADIUS}px")
print(f"Divisions: {N_DIVISIONS}, Step: {ANGLE_STEP}°, Icon: {ICON_SIZE}x{ICON_SIZE}")

inner_spacing = 2 * INNER_RADIUS * math.sin(math.radians(ANGLE_STEP / 2))
print(f"Inner ring spacing: {inner_spacing:.1f}px (min ~{ICON_SIZE}px for non-overlap)")
print()

# --- Position Table ---

print("=" * 60)
print("POSITIONS (top-left corner, for GUI)")
print("=" * 60)

for i, (neg_ethic, pos_ethic) in enumerate(AXES):
    angle_neg = START_ANGLE_DEG - i * ANGLE_STEP
    angle_pos = angle_neg - 180

    print(f"\n### AXIS {i}: {neg_ethic.upper()} ↔ {pos_ethic.upper()} ###")
    for label, r, a in [
        (f"fanatic_{neg_ethic}", OUTER_RADIUS, angle_neg),
        (neg_ethic, INNER_RADIUS, angle_neg),
        (pos_ethic, INNER_RADIUS, angle_pos),
        (f"fanatic_{pos_ethic}", OUTER_RADIUS, angle_pos),
    ]:
        p = topleft_pos(r, a)
        print(f"  {label:32s} x={p[0]:4d}  y={p[1]:4d}")

gestalt_tl = (CENTER_X - ICON_OFFSET, CENTER_Y - ICON_OFFSET)
print(f"\n### GESTALT ###")
print(f"  {'gestalt_consciousness':32s} x={gestalt_tl[0]:4d}  y={gestalt_tl[1]:4d}")

# --- GUI Snippet ---

print()
print("=" * 60)
print("GUI SNIPPET")
print("=" * 60)

for i, (neg_ethic, pos_ethic) in enumerate(AXES):
    angle_neg = START_ANGLE_DEG - i * ANGLE_STEP
    angle_pos = angle_neg - 180

    print(f"\n\t\t### AXIS {i}: {neg_ethic.upper()} \u2194 {pos_ethic.upper()} ###")
    for name, sprite_name, r, a in [
        (f"ethic_fanatic_{neg_ethic}", f"GFX_ethics_fanatic_{neg_ethic}", OUTER_RADIUS, angle_neg),
        (f"ethic_{neg_ethic}", f"GFX_ethics_{neg_ethic}", INNER_RADIUS, angle_neg),
        (f"ethic_{pos_ethic}", f"GFX_ethics_{pos_ethic}", INNER_RADIUS, angle_pos),
        (f"ethic_fanatic_{pos_ethic}", f"GFX_ethics_fanatic_{pos_ethic}", OUTER_RADIUS, angle_pos),
    ]:
        p = topleft_pos(r, a)
        print(f"""
\t\tbuttonType = {{
\t\t\tname = "{name}"
\t\t\tspriteType = "{sprite_name}"
\t\t\tposition = {{ x = {p[0]} y = {p[1]} }}
\t\t\tclicksound = interface
\t\t}}""")

print(f"""
\t\t### GESTALT ###

\t\tbuttonType = {{
\t\t\tname = "ethic_gestalt_consciousness"
\t\t\tspriteType = "GFX_ethics_gestalt_consciousness"
\t\t\tposition = {{ x = {gestalt_tl[0]} y = {gestalt_tl[1]} }}
\t\t\tclicksound = interface
\t\t}}""")
