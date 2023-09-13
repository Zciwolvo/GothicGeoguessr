from flask import Flask, render_template

from custom_map import CustomMap
from location import Location


app = Flask(__name__, static_url_path="/static")


@app.route("/")
def home():
    return render_template("home.html")


gothic1_map = CustomMap("gothic 1", "./static/maps/g1.png", 1)
gothic2_valley = CustomMap("Valley of mines", "./static/maps/g2_gd.png", 1)
gothic2_irdorath = CustomMap("Irdorath", "./static/maps/g2_irdorath.png", 1)
gothic2_jarkendar = CustomMap("Jarkendar", "./static/maps/g2_jarkendar.png", 1)
gothic2_khorinis = CustomMap("Khorinis", "./static/maps/g2_khorinis.png", 1)
gothic2_map = CustomMap("gothic 2", "./static/maps/g2.png", 1)


loc = Location("/static/locations/1.jpg", 63, 165)


@app.route("/map")
def map():
    return render_template("map.html", custom_map=gothic1_map, location=loc, index=0)


if __name__ == "__main__":
    app.run(debug=True)
