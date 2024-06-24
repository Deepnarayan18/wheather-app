from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_weather(city):
    url = f"https://www.weather-forecast.com/locations/{city}/forecasts/latest"
    try:
        # Send GET request to the weather website
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract weather information
        forecast = soup.find(class_='b-forecast__table-description-content').text.strip()

        return forecast
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = scrape_weather(city)
    return render_template('weather.html', city=city, weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
