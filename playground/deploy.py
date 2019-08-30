import requests

def upload_zip():
    out = []
    r = s.get("https://terminal.c1games.com/api/game/algo")
    leaderboard = json.loads(r.text)

    for algo in leaderboard["data"]["algos"]:
        out.append({
            "id": algo["id"],
            "name": algo["name"],
            "rating": algo["rating"]
        })
    return out