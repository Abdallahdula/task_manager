from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/weather/current')
def current_weather():
    city = request.args.get('city', 'Pemba')
    # Mock weather data
    data = {
        "city": city,
        "temperature": "22°C",
        "condition": "Sunny",
        "humidity": "60%"
    }
    return jsonify(data)

@app.route('/api/weather/forecast')
def weather_forecast():
    city = request.args.get('city', 'Zanzibar')
    days = int(request.args.get('days', 3))
    # Generate mock forecast
    forecast = [
        {"day": i+1, "temperature": f"{20+i}°C", "condition": "Partly Cloudy"}
        for i in range(days)
    ]
    return jsonify({
        "city": city,
        "forecast": forecast
    })

if __name__ == '__main__':
    app.run(debug=True,  port=5001)
