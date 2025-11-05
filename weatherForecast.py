from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import python_weather
import asyncio
import os
   # Cho phép fetch từ file HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "controllers")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)
@app.get("/")
def home():
    return render_template('index.html')

@app.post("/weatherForecast")
def weather():
    data = request.json
    city = data.get("city")

    async def fetch_weather(city):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            return await client.get(city)

    weather_data = asyncio.run(fetch_weather(city))

    return jsonify({
        "location": weather_data.location,
        "date": str(weather_data.datetime),
        "temp": weather_data.temperature,
        'wind_speed': weather_data.wind_speed,
        "desc": weather_data.description
    })


if __name__ == "__main__":
    app.run(port=5500, debug=True)
