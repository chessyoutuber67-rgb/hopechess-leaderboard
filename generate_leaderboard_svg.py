
import json
from pathlib import Path
from xml.sax.saxutils import escape

INPUT_FILE = Path("leaderboard.json")
OUTPUT_FILE = Path("leaderboard.svg")

# Narrower and taller layout
WIDTH = 500
HEIGHT = 1650

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

        text(250, 65, "HOPECHESS", 42, GOLD, "bold", "middle"),
        text(250, 110, "WEEKLY CLIMBERS", 27, WHITE, "bold", "middle"),
        text(250, 145, "THINK. PLAY. CONQUER.", 18, MUTED, "normal", "middle"),
    ]

    # WEEKLY CLIMBERS
    modes = [
        ("rapid", "RAPID", 180),
        ("blitz", "BLITZ", 480),
        ("bullet", "BULLET", 780),
    ]

    for mode, label, top in modes:
        parts.append(card(top, 275))

        parts.append(
            text(35, top + 48, label, 32, GOLD, "bold")
        )

        climbers = data.get("weekly_climbers", {}).get(mode, [])

        if not climbers:
            parts.append(
                text(35, top + 120, "Collecting history...",
                     22, MUTED)
            )
        else:
            for index, player in enumerate(climbers[:3]):
                y = top + 105 + index * 75

                username = player.get("username", "Unknown")
                change = player.get("change", 0)
                rating = player.get("rating", "N/A")

                parts.append(
                    text(35, y, f"{index + 1}. {username}",
                         24, WHITE, "bold")
                )

                parts.append(
                    text(35, y + 32,
                         f"+{change} rating points  |  {rating}",
                         19, GREEN_TEXT, "bold")
                )

    # CHAMPIONS' HALL
    champion_top = 1090

    parts.append(card(champion_top, 400))

    parts.append(
        text(250, champion_top + 60,
             "CHAMPIONS' HALL", 29, GOLD, "bold", "middle")
    )

    rankings = data.get("rankings", {})

    champion_modes = [
        ("rapid", "RAPID"),
        ("blitz", "BLITZ"),
        ("bullet", "BULLET"),
    ]

    for index, (mode, label) in enumerate(champion_modes):
        y = champion_top + 145 + index * 85

        players = rankings.get(mode, [])

        if players:
            champion = players[0]
            username = champion.get("username", "Unknown")
            rating = champion.get("rating", "N/A")

            parts.append(
                text(35, y, label, 24, GOLD, "bold")
            )

            parts.append(
                text(35, y + 35, username, 23, WHITE, "bold")
            )

            parts.append(
                text(35, y + 62, f"Rating: {rating}",
                     19, GREEN_TEXT)
            )
        else:
            parts.append(
                text(35, y, f"{label}: No data", 22, MUTED)
            )

    # FOOTER
    parts.append(
        text(250, 1540, "HOPECHESS", 25, GOLD, "bold", "middle")
    )

    parts.append(
        text(250, 1575, "THINK. PLAY. CONQUER.",
             18, MUTED, "normal", "middle")
    )

    parts.append("</svg>")

    OUTPUT_FILE.write_text(
        "\n".join(parts),
        encoding="utf-8"
    )

    print("HOPECHESS NARROW LEADERBOARD GENERATED!")


if __name__ == "__main__":
    main()
