
import json
from pathlib import Path
from xml.sax.saxutils import escape

INPUT_FILE = Path("leaderboard.json")
OUTPUT_FILE = Path("leaderboard.svg")

WIDTH = 900
HEIGHT = 1120

GOLD = "#e6c879"
WHITE = "#f3f0df"
GREEN = "#192b21"
MUTED = "#b8c8b9"


def safe(value):
    return escape(str(value))


def text(x, y, value, size=24, color=WHITE, weight="normal",
         anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" '
        f'fill="{color}" font-weight="{weight}" '
        f'text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif">'
        f'{safe(value)}</text>'
    )


def card(x, y, width, height):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="16" fill="{GREEN}" stroke="#526c50" stroke-width="2"/>'
    )


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("leaderboard.json not found!")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" '
        f'rx="22" fill="#0b1511"/>',

        text(450, 65, "HOPECHESS", 42, GOLD, "bold", "middle"),
        text(450, 105, "WEEKLY RATING CLIMBERS", 22,
             WHITE, "bold", "middle"),
        text(450, 140, "THINK. PLAY. CONQUER.", 15,
             MUTED, "normal", "middle"),
    ]

    modes = [
        ("rapid", "♟ RAPID", 180),
        ("blitz", "⚡ BLITZ", 460),
        ("bullet", "🔥 BULLET", 740),
    ]

    for mode, label, top in modes:
        parts.append(card(35, top, 830, 255))
        parts.append(text(65, top + 45, label, 27, GOLD, "bold"))

        climbers = data.get("weekly_climbers", {}).get(mode, [])

        if not climbers:
            parts.append(
                text(65, top + 105, "Collecting 7-day rating history...",
                     20, MUTED)
            )
            parts.append(
                text(65, top + 145, "Results will appear here soon.",
                     17, MUTED)
            )
        else:
            for index, player in enumerate(climbers[:3]):
                y = top + 100 + index * 48
                username = player.get("username", "Unknown")
                change = player.get("change", 0)
                rating = player.get("rating", "N/A")

                parts.append(
                    text(65, y, f"{index + 1}. {username}",
                         20, WHITE, "bold")
                )
                parts.append(
                    text(835, y, f"+{change}  |  {rating}",
                         19, "#9ed39f", "bold", "end")
                )

    parts.append(
        text(450, 1045, "CURRENT CLUB CHAMPIONS",
             25, GOLD, "bold", "middle")
    )

    champions = [
        ("rapid", "RAPID"),
        ("blitz", "BLITZ"),
        ("bullet", "BULLET"),
    ]

    for index, (mode, label) in enumerate(champions):
        ranking = data.get("rankings", {}).get(mode, [])
        y = 1080 + index * 0

        if ranking:
            champion = ranking[0]
            name = champion.get("username", "Unknown")
            rating = champion.get("rating", "N/A")
            parts.append(
                text(65 + index * 275, y, f"{label}: {name} ({rating})",
                     15, WHITE)
            )
        else:
            parts.append(
                text(65 + index * 275, y, f"{label}: No data",
                     15, MUTED)
            )

    parts.append("</svg>")

    OUTPUT_FILE.write_text("\n".join(parts), encoding="utf-8")

    print("HOPECHESS SVG GENERATED!")
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
