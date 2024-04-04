
from flask import Flask, redirect, url_for, request, render_template
import requests
import json
from datetime import date
 
app = Flask(__name__)

@app.route('/success/<zip>, <country>')
def success(zip, country):
    #find lat and lon from user input
    geo_response_API = requests.get(f'http://api.openweathermap.org/geo/1.0/zip?zip={zip},{country}&appid=98602286b5dd716117fabd20bd73c23b')

    data = geo_response_API.text
    parse_json = json.loads(data)

    lat = parse_json['lat']
    lon =  parse_json['lon']

    #find city from given and lon
    location_response_API = requests.get(f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=5&appid=98602286b5dd716117fabd20bd73c23b')

    data = location_response_API.text
    parse_json = json.loads(data)
    location = parse_json[0]['name']
    country_show =  parse_json[0]['country']
    
    #find weather report for city and display info
    weather_response_API = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=98602286b5dd716117fabd20bd73c23b')

    data = weather_response_API.text
    parse_json = json.loads(data)

    temp = parse_json['main']['temp']
    feels_like = parse_json['main']['feels_like']
    temp_min = parse_json['main']['temp_min']
    temp_max  = parse_json['main']['temp_max']
    weather_desc = parse_json['weather'][0]['description']


    #kelvin to f conversion
    temp = int((9/5) * (temp - 273.15) + 32)
    temp_min = int((9/5) * ( temp_min - 273.15) + 32)
    temp_max = int((9/5) * ( temp_max - 273.15) + 32)
    feels_like = int((9/5) * (  feels_like - 273.15) + 32)
    
    #get todays date
    today = date.today()
    date2 = today.strftime("%B %d, %Y")
    return render_template('weather.html', today=date2, temp=temp, weather_desc=weather_desc, temp_min=temp_min, temp_max=temp_max, location=location, country_show=country_show,  feels_like =  feels_like )

@app.route('/weatherindex', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['zip']
        user2 = request.form['country']
        return redirect(url_for('success', zip=user, country=user2))
    else:
        user = request.args.get('zip')
        user2 = request.args.get('country')
        return redirect(url_for('success', zip=user, country=user2))
 

if __name__ == '__main__':
    app.run(debug=True)