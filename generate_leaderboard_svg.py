
import json
from pathlib import Path
from xml.sax.saxutils import escape

INPUT_FILE = Path("leaderboard.json")
OUTPUT_FILE = Path("leaderboard.svg")

WIDTH = 900
HEIGHT = 1200

GOLD = "#e6c879"
WHITE = "#f3f0df"
GREEN = "#192b21"
MUTED = "#b8c8b9"
BACKGROUND = "#0b1511"
GREEN_TEXT = "#9ed39f"


def safe(value):
    return escape(str(value))


def text(x, y, value, size=28, color=WHITE,
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
        f'<rect x="25" y="{y}" width="850" height="{height}" '
        f'rx="18" fill="{GREEN}" '
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

        text(450, 65, "HOPECHESS", 52, GOLD, "bold", "middle"),
        text(450, 110, "WEEKLY RATING CLIMBERS", 30, WHITE, "bold", "middle"),
        text(450, 145, "THINK. PLAY. CONQUER.", 20, MUTED, "normal", "middle"),
    ]

    # WEEKLY CLIMBERS
    modes = [
        ("rapid", "RAPID", 170),
        ("blitz", "BLITZ", 380),
        ("bullet", "BULLET", 590),
    ]

    for mode, label, top in modes:
        parts.append(card(top, 195))

        parts.append(
            text(55, top + 48, label, 34, GOLD, "bold")
        )

        climbers = data.get("weekly_climbers", {}).get(mode, [])

        if not climbers:
            parts.append(
                text(55, top + 115, "Collecting 7-day history...",
                     26, MUTED)
            )
        else:
            for index, player in enumerate(climbers[:3]):
                y = top + 100 + index * 45

                username = player.get("username", "Unknown")
                change = player.get("change", 0)
                rating = player.get("rating", "N/A")

                parts.append(
                    text(55, y, f"{index + 1}. {username}",
                         25, WHITE, "bold")
                )

                parts.append(
                    text(840, y, f"+{change}  |  {rating}",
                         24, GREEN_TEXT, "bold", "end")
                )

    # CURRENT CHAMPIONS
    champion_top = 810

    parts.append(card(champion_top, 300))

    parts.append(
        text(450, champion_top + 55,
             "CHAMPIONS' HALL", 36, GOLD, "bold", "middle")
    )

    rankings = data.get("rankings", {})

    champion_modes = [
        ("rapid", "RAPID"),
        ("blitz", "BLITZ"),
        ("bullet", "BULLET"),
    ]

    for index, (mode, label) in enumerate(champion_modes):
        y = champion_top + 125 + index * 65

        players = rankings.get(mode, [])

        if players:
            champion = players[0]
            username = champion.get("username", "Unknown")
            rating = champion.get("rating", "N/A")

            parts.append(
                text(65, y, label, 27, GOLD, "bold")
            )

            parts.append(
                text(840, y, f"{username}  |  {rating}",
                     25, WHITE, "bold", "end")
            )
        else:
            parts.append(
                text(65, y, f"{label}: No champion data",
                     25, MUTED)
            )

    # FOOTER
    parts.append(
        text(450, 1160, "HOPECHESS  •  THINK. PLAY. CONQUER.",
             22, GOLD, "bold", "middle")
    )

    parts.append("</svg>")

    OUTPUT_FILE.write_text(
        "\n".join(parts),
        encoding="utf-8"
    )

    print("HOPECHESS SVG GENERATED!")


if __name__ == "__main__":
    main()
