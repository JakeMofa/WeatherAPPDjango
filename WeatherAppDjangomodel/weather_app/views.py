from django.shortcuts import render
import requests
import datetime

# Create your views here.
#make a def function, going to call on the request on the api key
# now define the url endpoint and interpoint of the weather app api you want to use
def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    
    #Were going to check if this is a get request or post request
    
    
    if request.method == "POST":
        
        # now make  variables  where, creating templates where we will pass the data
        city1 = request.post['city1']
        city2 = request.get('city2', None)
    
    else:
        return render(request, "weather_app/index.html")
    
    #Then outsource a function or a functionality, of the actual weatherapp request in2 a a sperate function and not an api endpoint
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    #Send a request to the api, get a response and get certain feilds from that response ,take the information and render it into a template
    response =  requests.get(current_weather_url.format(city,api_key)).json
      