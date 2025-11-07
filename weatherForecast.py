from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import unicodedata
import os
def normalize(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8').lower()
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
CORS(app)
@app.route("/")
def home():
    return render_template("index.html")
@app.post("/weatherForecast")
def weather():
    data = request.json
    city = data.get("city")
    city = normalize(city)
    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()

    if "results" not in geo:
        return jsonify({"error": "Không tìm thấy thành phố"}), 404

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_min,temperature_2m_max,weathercode&timezone=auto"
    r = requests.get(url).json()
    desc_map = {
        "Nắng đẹp": "fa-solid fa-sun",
        "Quang mây": "fa-solid fa-cloud-sun",
        "Có mây": "fa-solid fa-cloud-sun",
        "Nhiều mây": "fa-solid fa-cloud",

        "Sương mù": "fa-solid fa-smog",
        "Sương giá": "fa-solid fa-snowflake",

        "Mưa phùn nhẹ": "fa-solid fa-cloud-rain",
        "Mưa phùn": "fa-solid fa-cloud-rain",
        "Mưa phùn to": "fa-solid fa-cloud-showers-heavy",

        "Mưa phùn se lạnh": "fa-solid fa-cloud-rain",
        "Mưa phùn lạnh": "fa-solid fa-cloud-showers-heavy",

        "Mưa nhẹ": "fa-solid fa-cloud-rain",
        "Có mưa": "fa-solid fa-cloud-rain",
        "Mưa lớn": "fa-solid fa-cloud-showers-heavy",

        "Mưa se lạnh": "fa-solid fa-cloud-rain",
        "Mưa rất lạnh": "fa-solid fa-cloud-showers-heavy",

        "Có tuyết nhẹ": "fa-regular fa-snowflake",
        "Có tuyết": "fa-regular fa-snowflake",
        "Tuyết rơi dày": "fa-solid fa-snowflake",
        "Bông tuyết non": "fa-solid fa-snowflake",

        "Mưa rào nhẹ": "fa-solid fa-cloud-rain",
        "Mưa rào": "fa-solid fa-cloud-rain",
        "Mưa rào lớn": "fa-solid fa-cloud-showers-heavy",

        "Mưa có tuyết": "fa-solid fa-cloud-meatball",
        "Mưa có tuyết lớn": "fa-solid fa-cloud-meatball",

        "Dông có sấm": "fa-solid fa-cloud-bolt",
        "Dông có mưa đá": "fa-solid fa-cloud-bolt",
        "Dông mưa đá lớn": "fa-solid fa-cloud-bolt"
    };

    icon_map = {
        0: "Nắng đẹp",                     # Nắng đẹp
        1: "Quang mây",               # Hầu như quang mây
        2: "Có mây",               # Có mây
        3: "Nhiều mây",                   # Nhiều mây

        45: "Sương mù",                   # Sương mù
        48: "Sương giá",                   # Sương mù đóng băng

        51: "Mưa phùn nhẹ",             # Mưa phùn nhẹ
        53: "Mưa phùn",             # Mưa phùn vừa
        55: "Mưa phùn to",             # Mưa phùn to

        56: "Mưa phùn se lạnh",             # Mưa phùn đóng băng nhẹ
        57: "Mưa phùn lạnh",             # Mưa phùn đóng băng mạnh

        61: "Mưa nhẹ",    # Mưa nhẹ
        63: "Có mưa",    # Mưa vừa
        65: "Mưa lớn",    # Mưa to

        66: "Mưa se lạnh",    # Mưa đóng băng nhẹ
        67: "Mưa rất lạnh",    # Mưa đóng băng mạnh

        71: "Có tuyết nhẹ",              # Tuyết nhẹ
        73: "Có tuyết",              # Tuyết vừa
        75: "Tuyết rơi dày",              # Tuyết nặng
        77: "Bông tuyết non",              # Bông tuyết nhỏ

        80: "Mưa rào nhẹ",    # Mưa rào nhẹ
        81: "Mưa rào",    # Mưa rào
        82: "Mưa rào lớn",    # Mưa rào lớn

        85: "Mưa có tuyết",              # Mưa tuyết nhẹ
        86: "Mưa có tuyết lớn",              # Mưa tuyết lớn

        95: "Dông có sấm",             # Dông, có sấm
        96: "Dông có mưa đá",             # Dông kèm mưa đá nhỏ
        99: "Dông mưa đá lớn",
    }

    result = []
    for i in range(4):
        date_obj = datetime.strptime(r["daily"]["time"][i], "%Y-%m-%d")
        day_name = date_obj.strftime("%a")

        min_temp = r["daily"]["temperature_2m_min"][i]
        max_temp = r["daily"]["temperature_2m_max"][i]
        code = r["daily"]["weathercode"][i]
        desc = icon_map.get(code, "Không rõ")
        icon = desc_map.get(desc, "fa-solid fa-cloud")

        result.append({
            "day": day_name,
            "temp": f"{min_temp}°C - {max_temp}°C",
            "icon": icon,
            "desc": desc
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5500, debug=True)
