from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = '9dbc57d703d6dcc96a30abc8c7ae20c0'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if str(data.get('cod')) == '200':
                icon_code = data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                weather_data = {
                    'city': f"{data['name']}, {data['sys']['country']}",
                    'temperature': f"{data['main']['temp']} °C",
                    'condition': data['weather'][0]['description'].title(),
                    'humidity': f"{data['main']['humidity']}%",
                    'wind': f"{data['wind']['speed']} m/s",
                    'icon': icon_url
                }
            else:
                weather_data['error'] = "City not found!"
        else:
            weather_data['error'] = "Please enter a city name."

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)



