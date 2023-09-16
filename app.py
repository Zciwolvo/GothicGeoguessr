from flask import Flask, render_template, request, jsonify, redirect, url_for
import random

from custom_map import CustomMap
from location import Location


app = Flask(__name__, static_url_path="/geoguessr/static")

api = ""


score = 0
round_counter = 1


gothic1_map = CustomMap(
    "gothic1",
    "https://drive.google.com/uc?id=1mqBhVNb4LErYSNvq9zBo2r-iIgspk79b",
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
    return jsonify({"message": "Success"})


@app.route("/geoguessr/map")
def map():
    global loc
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


@app.route("/geoguessr/login")
def login():
    return render_template("login.html")


@app.route("/geoguessr/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
