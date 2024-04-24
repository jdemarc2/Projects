import boto3
import env
import json
import requests
import geocoder
import schedule
import time

from geopy.geocoders import Nominatim

def get_weather_data():
    g = geocoder.ip('me')
    print(g.latlng)

    lat, lon = g.latlng

    api_key = api_key

    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    print("API URL:", api_url)

    weather_data = requests.get(api_url)

    print("Weather Data:", weather_data.json())

    return weather_data.json()

def parse_weather_data(weather_info):
    city = weather_info['name']
    weather_description = weather_info['weather'][0]['description']
    wind_speed_mph = round(weather_info['wind']['speed'] * 2.237, 2)  # Convert m/s to mph
    humidity = weather_info['main']['humidity']
    temperature_f = round((weather_info['main']['temp'] - 273.15) * 9/5 + 32, 2)  # Convert Kelvin to Fahrenheit
    feels_like_f = round((weather_info['main']['feels_like'] - 273.15) * 9/5 + 32, 2)  # Convert Kelvin to Fahrenheit

    return {
        "city": city,
        "weather_description": weather_description,
        "wind_speed_mph": wind_speed_mph,
        "humidity": humidity,
        "temperature_f": temperature_f,
        "feels_like_f": feels_like_f
    }

def construct_message(weather_report):
    return f'''
Weather Report:
City: {weather_report['city']}
Weather: {weather_report['weather_description']}
Wind Speed: {weather_report['wind_speed_mph']} mph
Humidity: {weather_report['humidity']}%
Temperature: {weather_report['temperature_f']}°F
Feels Like: {weather_report['feels_like_f']}°F
'''

def send_weather_report_via_sns(message):
    # Send the weather data via AWS SNS
    topicArn = 'arn:aws:sns:us-east-2:783761575106:Personal'
    snsClient = boto3.client(
        'sns',
        aws_access_key_id=env.accessKey,
        aws_secret_access_key=env.secretKey,
        region_name='us-east-2'
    )

    response = snsClient.publish(
        TopicArn=topicArn,
        Message=message,
        Subject='Weather Report'
    )

    print(response['ResponseMetadata']['HTTPStatusCode'])

def main():
    weather_info = get_weather_data()
    weather_report = parse_weather_data(weather_info)
    message = construct_message(weather_report)
    send_weather_report_via_sns(message)

def job():
    print("Running job...")
    main()

schedule.every().day.at("07:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every 60 seconds
