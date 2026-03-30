from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY", "ac04f479dc6b6a2159158fc56dd23489") 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "No city provided"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)

    if res.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = res.json()
    weather = {
        "location": f"{data['name']}, {data['sys']['country']}",
        "temp": round(data["main"]["temp"]),
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "humidity": data["main"]["humidity"],
        "wind": round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
        "pressure": data["main"]["pressure"]
    }
    return jsonify(weather)

if __name__ == "__main__":
    app.run(debug=True)
