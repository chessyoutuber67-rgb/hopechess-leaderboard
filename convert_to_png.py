
from pathlib import Path
import cairosvg

SVG_FILE = Path("leaderboard.svg")
PNG_FILE = Path("leaderboard.png")

if not SVG_FILE.exists():
    raise FileNotFoundError("leaderboard.svg not found!")

cairosvg.svg2png(
    url=str(SVG_FILE),
    write_to=str(PNG_FILE),
    output_width=900
)

print("HOPECHESS PNG GENERATED!")
print("Saved:", PNG_FILE)
