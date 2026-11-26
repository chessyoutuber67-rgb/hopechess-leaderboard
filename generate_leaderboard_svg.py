
import json
from pathlib import Path
from xml.sax.saxutils import escape

INPUT_FILE = Path("leaderboard.json")
OUTPUT_FILE = Path("leaderboard.svg")

# Exact 1:3 portrait layout
WIDTH = 500
HEIGHT = 1500

GOLD = "#e6c879"
WHITE = "#f3f0df"
GREEN = "#192b21"
MUTED = "#b8c8b9"
BACKGROUND = "#0b1511"
GREEN_TEXT = "#9ed39f"


def safe(value):
    return escape(str(value))


def text(x, y, value, size=25, color=WHITE,
         weight="normal", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" '
        f'font-size="{size}" '
        f'fill="{color}" '
        f'font-weight="{weight}" '
        f'text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif">'
        f'{safe(value)}</text>'
    )


def card(y, height):
    return (
        f'<rect x="15" y="{y}" width="470" height="{height}" '
        f'rx="16" fill="{GREEN}" '
        f'stroke="#526c50" stroke-width="2"/>'
    )


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',

        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>',

        # HEADER
        text(250, 55, "HOPECHESS", 42, GOLD, "bold", "middle"),
        text(250, 98, "WEEKLY CLIMBERS", 27, WHITE, "bold", "middle"),
        text(250, 130, "THINK. PLAY. CONQUER.", 18, MUTED, "normal", "middle"),
    ]

    # WEEKLY CLIMBERS
    modes = [
        ("rapid", "RAPID", 165),
        ("blitz", "BLITZ", 440),
        ("bullet", "BULLET", 715),
    ]

    for mode, label, top in modes:
        parts.append(card(top, 260))

        parts.append(
            text(35, top + 43, label, 32, GOLD, "bold")
        )

        climbers = data.get("weekly_climbers", {}).get(mode, [])

        if not climbers:
            parts.append(
                text(35, top + 130, "Collecting history...",
                     22, MUTED)
            )
        else:
            for index, player in enumerate(climbers[:3]):
                y = top + 95 + index * 65

                username = player.get("username", "Unknown")
                change = player.get("change", 0)
                rating = player.get("rating", "N/A")

                parts.append(
                    text(35, y, f"{index + 1}. {username}",
                         24, WHITE, "bold")
                )

                parts.append(
                    text(35, y + 27,
                         f"+{change} rating points  |  {rating}",
                         18, GREEN_TEXT, "bold")
                )

    # CHAMPIONS' HALL
    champion_top = 995

    parts.append(card(champion_top, 385))

    parts.append(
        text(250, champion_top + 55,
             "CHAMPIONS' HALL", 29, GOLD, "bold", "middle")
    )

    rankings = data.get("rankings", {})

    champion_modes = [
        ("rapid", "RAPID"),
        ("blitz", "BLITZ"),
        ("bullet", "BULLET"),
    ]

    for index, (mode, label) in enumerate(champion_modes):
        y = champion_top + 120 + index * 85

        players = rankings.get(mode, [])

        if players:
            champion = players[0]
            username = champion.get("username", "Unknown")
            rating = champion.get("rating", "N/A")

            parts.append(
                text(35, y, label, 23, GOLD, "bold")
            )

            parts.append(
                text(35, y + 29, username, 22, WHITE, "bold")
            )

            parts.append(
                text(35, y + 54, f"Rating: {rating}",
                     18, GREEN_TEXT)
            )
        else:
            parts.append(
                text(35, y, f"{label}: No data", 22, MUTED)
            )

    # FOOTER
    parts.append(
        text(250, 1440, "HOPECHESS", 25, GOLD, "bold", "middle")
    )

    parts.append(
        text(250, 1475, "THINK. PLAY. CONQUER.",
             18, MUTED, "normal", "middle")
    )

    parts.append("</svg>")

    OUTPUT_FILE.write_text(
        "\n".join(parts),
        encoding="utf-8"
    )

    print("HOPECHESS 1:3 LEADERBOARD GENERATED!")


if __name__ == "__main__":
    main()
