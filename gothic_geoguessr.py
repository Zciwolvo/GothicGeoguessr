from flask import render_template, request, jsonify, Blueprint
import random

from custom_map import CustomMap
from location import Location

gothic_blueprint = Blueprint("gothic", __name__)

api = ""


score = 0
round_counter = 1


gothic1_map = CustomMap("gothic1", "./static/maps/g1.png", 7)
gothic2_map = CustomMap("gothic2", "./static/maps/g2.png", 7)


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


@gothic_blueprint.route("/geoguessr/")
def home():
    global score, round_counter
    round_counter = 1
    score = 0
    return render_template("gothic.html")


@gothic_blueprint.route("/geoguessr/start_game", methods=["POST"])
def start_game():
    global score, round_counter, map_pool
    round_counter = 1
    score = 0
    data = request.get_json()
    map_pool = data["selectedGamePool"]
    return jsonify({"message": "Success"})


@gothic_blueprint.route("/geoguessr/update_score_and_round", methods=["POST"])
def update_score_and_round():
    global score, round_counter
    data = request.get_json()
    score += data["score"]
    round_counter += 1
    return jsonify({"message": "Success"})


@gothic_blueprint.route("/geoguessr/map")
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


@gothic_blueprint.route("/geoguessr/login")
def login():
    return render_template("login.html")


@gothic_blueprint.route("/geoguessr/register")
def register():
    return render_template("register.html")
