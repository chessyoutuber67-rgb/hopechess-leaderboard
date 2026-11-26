
import json
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone
from pathlib import Path

CLUB_URL = "https://api.chess.com/pub/club/hopechess/members"
HISTORY_FILE = Path("rating_history.json")


def get_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "HOPECHESS-Leaderboard/1.0",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


# Load previous rating history
if HISTORY_FILE.exists():
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)
else:
    history = {}

# Get club members
club = get_json(CLUB_URL)

members = {}

for category in ("weekly", "monthly", "all_time"):
    for member in club.get(category, []):
        username = member.get("username")
        if username:
            members[username.lower()] = username

print("HOPECHESS RATING LEADERBOARD")
print("=" * 55)

results = []

for username in sorted(members.values(), key=str.lower):
    try:
        stats = get_json(
            f"https://api.chess.com/pub/player/{username}/stats"
        )

        player = {"username": username}

        for mode in ("rapid", "blitz", "bullet"):
            rating = (
                stats.get(f"chess_{mode}", {})
                .get("last", {})
                .get("rating")
            )
            player[mode] = rating

        results.append(player)

        print(f"\n{username}")
        print("Rapid:", player["rapid"] if player["rapid"] is not None else "N/A")
        print("Blitz:", player["blitz"] if player["blitz"] is not None else "N/A")
        print("Bullet:", player["bullet"] if player["bullet"] is not None else "N/A")

    except (urllib.error.URLError, ValueError, KeyError) as error:
        print(f"\nCould not retrieve {username}: {error}")

    time.sleep(0.5)

# Save a new historical snapshot
if results:
    timestamp = datetime.now(timezone.utc).isoformat()

    for player in results:
        username = player["username"].lower()

        if username not in history:
            history[username] = []

        history[username].append({
            "timestamp": timestamp,
            "rapid": player["rapid"],
            "blitz": player["blitz"],
            "bullet": player["bullet"]
        })

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    print("\nRating history successfully saved!")

print("\n" + "=" * 55)
print("Players retrieved:", len(results))

