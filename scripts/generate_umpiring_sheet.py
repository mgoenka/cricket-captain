"""Generate a custom umpiring score sheet for a CricBay-style T20 match.

Takes the standard CricBay umpiring PDF and overlays a custom Playing XI section
at the bottom with up to 20 named roster slots and 10 blank fill-in slots.

Usage:
  python3 generate_umpiring_sheet.py \\
    --source /path/to/cricbay-Umpiring.pdf \\
    --output /path/to/output.pdf \\
    --roster /path/to/roster.txt \\
    --team-name "Alpha Lions"

`roster.txt` is a plain text file with one player per line, up to 20 names.
Convention:
  - Line 1: Captain (will be marked with "(C)")
  - Line 2: Vice Captain (will be marked with "(VC)")
  - Line 3: Manager (will be marked with "(M)")
  - Lines 4-18: regular roster (alphabetical or any order you want)
  - Lines 19-20: secondary / non-primary players (will be marked with "(S)")

The annotations can also be supplied inline (e.g., "Mohit Goenka (C)") and the
script will use them directly without re-annotating.
"""

from __future__ import annotations

import argparse
import os

import fitz

PAGE_W = 612
PAGE_H = 792

# CricBay logo blue (sampled from the original CricBay PDF logo)
DEFAULT_TEAM_COLOR = (32 / 255, 80 / 255, 243 / 255)

# Bounds of the original Playing XI section to cover
COVER_Y0 = 642
COVER_Y1 = 745.5

FONT_REG = "helv"
FONT_BOLD = "hebo"


def load_roster(path: str) -> list[str]:
    """Read up to 20 player names from a roster file."""
    with open(path) as f:
        names = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if not names:
        raise ValueError(f"No player names found in {path}")
    if len(names) > 20:
        print(f"Warning: roster has {len(names)} names, only the first 20 will be used.")
        names = names[:20]
    return names


def annotate_role(names: list[str]) -> list[str]:
    """Add (C), (VC), (M), (S) annotations if not already present.

    Convention:
      - index 0 -> (C)
      - index 1 -> (VC)
      - index 2 -> (M)
      - last two (indices 18, 19) -> (S) (only if you have 20 players)
    """
    annotated = []
    n = len(names)
    for i, name in enumerate(names):
        # If user already wrote "(C)", "(VC)", etc., leave it alone
        if any(tag in name for tag in ["(C)", "(VC)", "(M)", "(S)"]):
            annotated.append(name)
            continue

        if i == 0:
            annotated.append(f"{name} (C)")
        elif i == 1:
            annotated.append(f"{name} (VC)")
        elif i == 2:
            annotated.append(f"{name} (M)")
        elif n == 20 and i >= 18:
            annotated.append(f"{name} (S)")
        else:
            annotated.append(name)
    return annotated


def overlay_playing_xi(page: fitz.Page, players: list[str], team_name: str, team_color: tuple) -> None:
    cover = fitz.Rect(0, COVER_Y0, PAGE_W, COVER_Y1)
    page.draw_rect(cover, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

    # Section header: "Playing XI for {team_name} team" with team_name bold + team_color
    header_y = COVER_Y0 + 8
    header_fs = 9
    font_reg = fitz.Font(fontname=FONT_REG)
    font_bold = fitz.Font(fontname=FONT_BOLD)

    text1 = "Playing XI for "
    text2 = team_name
    text3 = " team"
    x = 18
    page.insert_text((x, header_y), text1, fontname=FONT_REG, fontsize=header_fs, color=(0, 0, 0))
    w1 = font_reg.text_length(text1, fontsize=header_fs)
    page.insert_text(
        (x + w1, header_y), text2, fontname=FONT_BOLD, fontsize=header_fs, color=team_color
    )
    w2 = font_bold.text_length(text2, fontsize=header_fs)
    page.insert_text(
        (x + w1 + w2, header_y), text3, fontname=FONT_REG, fontsize=header_fs, color=(0, 0, 0)
    )

    # 4-column slot grid: 1-10 / 11-20 / 21-25 / 26-30
    table_top = header_y + 3
    table_bottom = COVER_Y1
    n_rows = 10
    row_h = (table_bottom - table_top) / n_rows
    col_w = (PAGE_W - 36) / 4
    num_fs = 9
    font_num = fitz.Font(fontname=FONT_REG)

    dot_x_in_col = 16
    name_indent_in_col = 20

    slots = []
    for slot in range(1, 11):
        slots.append((slot, 0, slot - 1))
    for slot in range(11, 21):
        slots.append((slot, 1, slot - 11))
    for slot in range(21, 26):
        slots.append((slot, 2, (slot - 21) * 2))
    for slot in range(26, 31):
        slots.append((slot, 3, (slot - 26) * 2))

    for slot, col, row in slots:
        col_x = 18 + col * col_w
        baseline_y = table_top + row * row_h + row_h - 2

        # Number, right-aligned at the dot
        num_str = f"{slot}."
        num_w = font_num.text_length(num_str, fontsize=num_fs)
        num_x = col_x + dot_x_in_col - num_w
        page.insert_text(
            (num_x, baseline_y), num_str, fontname=FONT_REG, fontsize=num_fs, color=(0, 0, 0)
        )

        name_x = col_x + name_indent_in_col
        if slot <= len(players):
            page.insert_text(
                (name_x, baseline_y),
                players[slot - 1],
                fontname=FONT_REG,
                fontsize=num_fs,
                color=(0, 0, 0),
            )
        else:
            page.draw_line(
                fitz.Point(name_x, baseline_y + 1),
                fitz.Point(col_x + col_w - 6, baseline_y + 1),
                color=(0, 0, 0),
                width=0.5,
            )


def generate(source: str, output: str, players: list[str], team_name: str, team_color: tuple) -> None:
    doc = fitz.open(source)
    page = doc[0]
    overlay_playing_xi(page, players, team_name, team_color)
    doc.save(output)
    doc.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate custom umpiring score sheet")
    ap.add_argument("--source", required=True, help="Original CricBay umpiring PDF")
    ap.add_argument("--output", required=True, help="Output PDF path")
    ap.add_argument(
        "--roster",
        required=True,
        help="Text file with player names, one per line (up to 20)",
    )
    ap.add_argument(
        "--team-name", default="My Team", help='Team name to highlight (default: "My Team")'
    )
    ap.add_argument(
        "--color",
        default="2050F3",
        help="Hex color for team name (default: CricBay blue 2050F3)",
    )
    args = ap.parse_args()

    names = load_roster(args.roster)
    names = annotate_role(names)

    hex_color = args.color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    team_color = (r / 255, g / 255, b / 255)

    generate(args.source, args.output, names, args.team_name, team_color)
    print(f"Generated: {args.output}")


if __name__ == "__main__":
    main()
