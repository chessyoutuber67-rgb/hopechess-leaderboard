
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

HISTORY_FILE = Path("rating_history.json")
OUTPUT_FILE = Path("leaderboard.json")

MODES = ("rapid", "blitz", "bullet")


def parse_timestamp(value):
    if not value:
        return None

    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))

        if result.tzinfo is None:
            result = result.replace(tzinfo=timezone.utc)

        return result
    except (ValueError, TypeError):
        return None


def main():
    if not HISTORY_FILE.exists():
        raise FileNotFoundError("rating_history.json not found!")

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    players = []
    weekly_candidates = {mode: [] for mode in MODES}

    for username, snapshots in history.items():
        if not snapshots:
            continue

        snapshots = sorted(
            snapshots,
            key=lambda s: parse_timestamp(s.get("timestamp"))
            or datetime.min.replace(tzinfo=timezone.utc)
        )

        current = snapshots[-1]
        current_time = parse_timestamp(current.get("timestamp"))
        previous = snapshots[-2] if len(snapshots) >= 2 else None

        player = {
            "username": username,
            "timestamp": current.get("timestamp")
        }

        weekly_baseline = None

        if current_time:
            cutoff = current_time - timedelta(days=7)

            for snapshot in snapshots:
                snapshot_time = parse_timestamp(snapshot.get("timestamp"))

                if snapshot_time and snapshot_time <= cutoff:
                    weekly_baseline = snapshot

        for mode in MODES:
            rating = current.get(mode)
            old_rating = previous.get(mode) if previous else None

            player[mode] = rating

            if (
                isinstance(rating, (int, float))
                and not isinstance(rating, bool)
                and isinstance(old_rating, (int, float))
                and not isinstance(old_rating, bool)
            ):
                player[f"{mode}_change"] = rating - old_rating
            else:
                player[f"{mode}_change"] = None

            baseline_rating = (
                weekly_baseline.get(mode)
                if weekly_baseline else None
            )

            if (
                isinstance(rating, (int, float))
                and not isinstance(rating, bool)
                and isinstance(baseline_rating, (int, float))
                and not isinstance(baseline_rating, bool)
            ):
                weekly_change = rating - baseline_rating
            else:
                weekly_change = None

            player[f"{mode}_weekly_change"] = weekly_change

            if weekly_change is not None and weekly_change > 0:
                weekly_candidates[mode].append({
                    "username": username,
                    "rating": rating,
                    "change": weekly_change,
                    "from_timestamp": weekly_baseline.get("timestamp"),
                    "to_timestamp": current.get("timestamp")
                })

        players.append(player)

    leaderboard = {
        "updated_at": max(
            (p["timestamp"] or "" for p in players),
            default=None
        ),
        "total_players": len(players),
        "players": players,
        "rankings": {},
        "biggest_improver": {},
        "weekly_climbers": {}
    }

    for mode in MODES:
        ranked = [
            p for p in players
            if isinstance(p[mode], (int, float))
            and not isinstance(p[mode], bool)
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
            and not isinstance(p[f"{mode}_change"], bool)
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

        weekly = weekly_candidates[mode]
        weekly.sort(key=lambda p: p["change"], reverse=True)

        leaderboard["weekly_climbers"][mode] = [
            {
                "rank": index + 1,
                **player
            }
            for index, player in enumerate(weekly)
        ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(leaderboard, file, indent=4)

    print("HOPECHESS LEADERBOARD GENERATED!")
    print("Players:", len(players))

    for mode in MODES:
        print(f"\n{mode.upper()} TOP 3 RATINGS:")

        for player in leaderboard["rankings"][mode][:3]:
            print(
                player["rank"],
                player["username"],
                player["rating"],
                "Change:",
                player["change"]
            )

        print(f"\n{mode.upper()} WEEKLY CLIMBERS:")

        for player in leaderboard["weekly_climbers"][mode][:3]:
            print(
                player["rank"],
                player["username"],
                "+",
                player["change"]
            )

        if not leaderboard["weekly_climbers"][mode]:
            print("No weekly climbers yet. Collecting history...")


if __name__ == "__main__":
    main()

