from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import os
from dotenv import load_dotenv
import jwt
import json
import secrets

from custom_map import CustomMap
from location import Location
from leaderboards_entry import Entry

app = Flask(__name__, static_url_path="/geoguessr/static")
load_dotenv()

api = os.getenv("API")


score = 0
round_counter = 1

gothic1_map = CustomMap(
    "gothic1",
    "./static/maps/g1.png",
    620,
    490,
    7,
)
gothic2_map = CustomMap("gothic2", "./static/maps/g2.png", 2000, 2000, 7)


def get_random_location(map_pool="gothic1"):
    loc1 = Location(
        "./static/locations/1.jpg", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc2 = Location(
        "./static/locations/2.png", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc3 = Location(
        "./static/locations/3.png", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc4 = Location(
        "./static/locations/4.png", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc5 = Location(
        "./static/locations/5.png", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc6 = Location(
        "./static/locations/6.png", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    gothic1 = [loc1, loc2, loc3, loc4, loc5, loc6]
    gothic2 = [loc1, loc2, loc3, loc4, loc5, loc6]
    gothic3 = [loc1, loc2, loc3, loc4, loc5, loc6]
    archolos = [loc1, loc2, loc3, loc4, loc5, loc6]
    mixed = [loc1, loc2, loc3, loc4, loc5, loc6]

    chosen = []
    if map_pool == "Gothic1":
        chosen = gothic1
    elif map_pool == "Gothic2":
        chosen = gothic2
    elif map_pool == "Gothic3":
        chosen = gothic3
    elif map_pool == "Archolos":
        chosen = archolos
    else:
        chosen = mixed
    return random.choice(chosen)


@app.route("/geoguessr/")
def home():
    global score, round_counter
    round_counter = 1
    score = 0
    access_token = request.cookies.get("access_token")
    if not access_token:
        return render_template(
            "gothic.html",
            message="It looks like you're not logged in, so your score won't be saved to the leaderboards. Log in or create an account to start saving your scores and competing with others.",
        )
    return render_template("gothic.html")


@app.route("/geoguessr/start_game", methods=["POST"])
def start_game():
    global score, round_counter, map_pool
    round_counter = 1
    score = 0
    data = request.get_json()
    map_pool = data["selectedGamePool"]
    return jsonify({"message": "Success"})


@app.route("/geoguessr/update_score_and_round", methods=["POST"])
def update_score_and_round():
    global score, round_counter
    data = request.get_json()
    score += data["score"]
    round_counter += 1
    if round_counter == 6:
        access_token = request.cookies.get("access_token")
        if access_token:
            decoded_token = jwt.decode(
                access_token, key=os.getenv("JWT_SECRET"), algorithms=["HS256"]
            )
            username = decoded_token["sub"]["username"]
            entry = Entry(username, score, map_pool)
            entry.save_to_json()
    return jsonify({"message": "Success"})


@app.route("/geoguessr/leaderboards")
def leaderboards():
    scores_dir = "/home/IgorGawlowicz/mysite/scores"
    leaderboards_data = []

    # Define the path to the scores.json file
    scores_file_path = os.path.join(scores_dir, "scores.json")

    if os.path.exists(scores_file_path):
        with open(scores_file_path, "r") as scores_file:
            scores_data = json.load(scores_file)

            # Iterate through all entries in the scores.json file
            for entry_id, score_data in scores_data.items():
                leaderboards_data.append(
                    {
                        "user": score_data["username"],
                        "score": score_data["score"],
                        "gamemode": score_data["gamemode"],
                        "date": score_data["date"],
                    }
                )

    # Sort the leaderboard data by score (you can customize the sorting)
    leaderboards_data.sort(key=lambda x: x["score"], reverse=True)

    return render_template("leaderboards.html", leaderboards_data=leaderboards_data)


@app.route("/geoguessr/map")
def map():
    global loc
    try:
        loc = get_random_location(map_pool)
        return render_template(
            "map.html",
            custom_map=loc.map,
            location=loc,
            api=api,
            score=score,
            round=round_counter,
            map_pool=map_pool,
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("gothic.html")


@app.route("/geoguessr/login")
def login():
    return render_template("login.html")


@app.route("/geoguessr/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
