
import json
import urllib.request

CLUB_URL = "https://api.chess.com/pub/club/hopechess/members"

request = urllib.request.Request(
    CLUB_URL,
    headers={
        "User-Agent": "HOPECHESS-Leaderboard/1.0",
        "Accept": "application/json",
    },
)

with urllib.request.urlopen(request, timeout=20) as response:
    data = json.loads(response.read().decode("utf-8"))

members = {}

for category in ("weekly", "monthly", "all_time"):
    entries = data.get(category, [])
    print(f"{category}: {len(entries)} members")

    for member in entries:
        username = member.get("username")
        if username:
            members[username.lower()] = username

print("\nUnique members found:", len(members))
print("\nMember usernames:")

for username in sorted(members.values(), key=str.lower):
    print("-", username)
