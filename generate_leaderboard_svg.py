
import json
from pathlib import Path
from xml.sax.saxutils import escape

INPUT_FILE = Path("leaderboard.json")
OUTPUT_FILE = Path("leaderboard.svg")

WIDTH = 700
HEIGHT = 1840

GOLD = "#e6c879"
WHITE = "#f3f0df"
GREEN = "#192b21"
MUTED = "#b8c8b9"


def safe(value):
    return escape(str(value))


def text(x, y, value, size=30, color=WHITE, weight="normal"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" '
        f'fill="{color}" font-weight="{weight}" '
        f'font-family="Arial, Helvetica, sans-serif">'
        f'{safe(value)}</text>'
    )


def card(y, height):
    return (
        f'<rect x="20" y="{y}" width="660" height="{height}" '
        f'rx="18" fill="{GREEN}" stroke="#526c50" stroke-width="2"/>'
    )


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#0b1511"/>',

        text(40, 65, "HOPECHESS", 48, GOLD, "bold"),
        text(40, 110, "WEEKLY RATING CLIMBERS", 29, WHITE, "bold"),
        text(40, 150, "THINK. PLAY. CONQUER.", 19, MUTED),
    ]

    modes = [
        ("rapid", "RAPID", 190),
        ("blitz", "BLITZ", 610),
        ("bullet", "BULLET", 1030),
    ]

    # WEEKLY RATING CLIMBERS
    for mode, label, top in modes:
        parts.append(card(top, 390))
        parts.append(text(45, top + 55, label, 38, GOLD, "bold"))

        climbers = data.get("weekly_climbers", {}).get(mode, [])

        if not climbers:
            parts.append(
                text(45, top + 140, "Collecting 7-day history...", 24, MUTED)
            )
        else:
            for index, player in enumerate(climbers[:5]):
                y = top + 125 + index * 48
                username = player.get("username", "Unknown")
                change = player.get("change", 0)
                rating = player.get("rating", "N/A")

                parts.append(
                    text(45, y, f"{index + 1}. {username}", 25, WHITE, "bold")
                )
                parts.append(
                    text(
                        45, y + 30,
                        f"+{change} rating points | Now: {rating}",
                        20, "#9ed39f"
                    )
                )

    # CURRENT CLUB CHAMPIONS
    champion_top = 1450
    parts.append(card(champion_top, 340))
    parts.append(
        text(45, champion_top + 60, "CURRENT CLUB CHAMPIONS",
             32, GOLD, "bold")
    )

    rankings = data.get("rankings", {})

    champion_modes = [
        ("rapid", "RAPID"),
        ("blitz", "BLITZ"),
        ("bullet", "BULLET"),
    ]

    for index, (mode, label) in enumerate(champion_modes):
        y = champion_top + 140 + index * 75
        players = rankings.get(mode, [])

        parts.append(text(45, y, label, 25, GOLD, "bold"))

        if players:
            champion = players[0]
            username = champion.get("username", "Unknown")
            rating = champion.get("rating", "N/A")

            parts.append(
                text(220, y, username, 25, WHITE, "bold")
            )
            parts.append(
                text(220, y + 30, f"Rating: {rating}", 20, MUTED)
            )
        else:
            parts.append(
                text(220, y, "No rating data yet", 22, MUTED)
            )

    parts.append(
        text(40, 1820, "HOPECHESS • THINK. PLAY. CONQUER.",
             19, GOLD, "bold")
    )

    parts.append("</svg>")

    OUTPUT_FILE.write_text("\n".join(parts), encoding="utf-8")
    print("HOPECHESS SVG GENERATED!")


if __name__ == "__main__":
    main()

