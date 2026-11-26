
import json
import urllib.request
import urllib.error
import time

CLUB_URL = "https://api.chess.com/pub/club/hopechess/members"

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
        print("Rapid:", player["rapid"] or "N/A")
        print("Blitz:", player["blitz"] or "N/A")
        print("Bullet:", player["bullet"] or "N/A")

    except (urllib.error.URLError, ValueError, KeyError) as error:
        print(f"\nCould not retrieve {username}: {error}")

    time.sleep(0.5)

print("\n" + "=" * 55)
print("Players retrieved:", len(results))
