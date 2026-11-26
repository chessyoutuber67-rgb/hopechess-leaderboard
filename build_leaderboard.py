
import json
from pathlib import Path

HISTORY_FILE = Path("rating_history.json")
OUTPUT_FILE = Path("leaderboard.json")

MODES = ("rapid", "blitz", "bullet")


def main():
    if not HISTORY_FILE.exists():
        raise FileNotFoundError("rating_history.json not found!")

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    players = []

    for username, snapshots in history.items():
        if not snapshots:
            continue

        current = snapshots[-1]
        previous = snapshots[-2] if len(snapshots) >= 2 else None

        player = {
            "username": username,
            "timestamp": current.get("timestamp")
        }

        for mode in MODES:
            rating = current.get(mode)
            old_rating = previous.get(mode) if previous else None

            player[mode] = rating

            if isinstance(rating, (int, float)) and isinstance(old_rating, (int, float)):
                player[f"{mode}_change"] = rating - old_rating
            else:
                player[f"{mode}_change"] = None

        players.append(player)

    leaderboard = {
        "updated_at": max(
            (p["timestamp"] or "" for p in players),
            default=None
        ),
        "total_players": len(players),
        "players": players,
        "rankings": {},
        "biggest_improver": {}
    }

    for mode in MODES:
        ranked = [
            p for p in players
            if isinstance(p[mode], (int, float))
        ]

        ranked.sort(key=lambda p: p[mode], reverse=True)

        leaderboard["rankings"][mode] = [
            {
                "rank": index + 1,
                "username": player["username"],
                "rating": player[mode],
                "change": player[f"{mode}_change"]
            }
            for index, player in enumerate(ranked)
        ]

        improvers = [
            p for p in players
            if isinstance(p[f"{mode}_change"], (int, float))
        ]

        improvers.sort(
            key=lambda p: p[f"{mode}_change"],
            reverse=True
        )

        if improvers:
            best = improvers[0]
            leaderboard["biggest_improver"][mode] = {
                "username": best["username"],
                "change": best[f"{mode}_change"]
            }
        else:
            leaderboard["biggest_improver"][mode] = None

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(leaderboard, file, indent=4)

    print("HOPECHESS LEADERBOARD GENERATED!")
    print("Players:", len(players))

    for mode in MODES:
        print(f"\n{mode.upper()} TOP 3:")

        for player in leaderboard["rankings"][mode][:3]:
            print(
                player["rank"],
                player["username"],
                player["rating"],
                "Change:",
                player["change"]
            )


if __name__ == "__main__":
    main()
