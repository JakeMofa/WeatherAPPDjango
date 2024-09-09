from django.shortcuts import render
import requests
import datetime

def index(request):
    api_key = open("/Users/dean/Documents/GitHub/WeatherAPPDjango/WeatherAppDjangomodel/weather_app/API_KEY", "r").read().strip()
    api_key = '<YOUR API KEY>'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')



#this catches the errors
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    try:
        # Fetch current weather data
        response = requests.get(current_weather_url.format(city, api_key)).json()

        # Check if 'coord' key exists in response
        if 'coord' not in response:
            print(f"Error: 'coord' key not found in the response for city: {city}")
            return None, []

        lat, lon = response['coord']['lat'], response['coord']['lon']

        # Fetch forecast data
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

        # Check if 'daily' key exists in forecast response
        if 'daily' not in forecast_response:
            print(f"Error: 'daily' key not found in the forecast response for city: {city}")
            return None, []

        # Process weather data
        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        # Process daily forecasts
        daily_forecasts = []
        for daily_data in forecast_response['daily'][:5]:
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon'],
            })

        return weather_data, daily_forecasts

    except requests.exceptions.RequestException as e:
        print(f"RequestException occurred: {e}")
        return None, []

    except KeyError as e:
        print(f"KeyError occurred: {e}")
        return None, []

#This does not catch the errors to catch errors use this:
# def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
#     response = requests.get(current_weather_url.format(city, api_key)).json()
#     lat, lon = response['coord']['lat'], response['coord']['lon']
#     forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

#     weather_data = {
#         'city': city,
#         'temperature': round(response['main']['temp'] - 273.15, 2),
#         'description': response['weather'][0]['description'],
#         'icon': response['weather'][0]['icon'],
#     }

#     daily_forecasts = []
#     for daily_data in forecast_response['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#             'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#             'description': daily_data['weather'][0]['description'],
#             'icon': daily_data['weather'][0]['icon'],
#         })

#     return weather_data, daily_forecasts




#OLD code 
# from django.shortcuts import render
# import requests
# import datetime

# # Create your views here.
# #make a def function, going to call on the request on the api key
# # now define the url endpoint and interpoint of the weather app api you want to use
# def index(request):
#     API_KEY = open("/Users/dean/Documents/GitHub/WeatherAPPDjango/WeatherAppDjangomodel/weather_app/API_KEY", "r").read().strip()
#     current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
#     forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    
#     #Were going to check if this is a get request or post request
    
    
#     if request.method == "POST":
        
#         # now make  variables  where, creating templates where we will pass the data
#         city1 = request.POST['city1']
#         city2 = request.POST.get('city2', None)
        
#         #Come nack here after making the weather data and forecast dictionary
#         weather_data1 , daily_forecasts1 =  fetch_weather_and_forecast(city1,API_KEY,current_weather_url,forecast_url)
        
#         if city2:
#             weather_data2 , daily_forecasts2 =  fetch_weather_and_forecast(city1,API_KEY,current_weather_url,forecast_url)
            
#         else: weather_data2, daily_forecasts2 = None,  None
        
#         context = {
#             "weather_data1" :  weather_data1,
#             "daily_forecasts1" : daily_forecasts1,
#             "weather_data2" :  weather_data2,
#             "daily_forecasts2" : daily_forecasts2,   
#         }
#         return render(request, "weather_app/index.html", context)
#     else:
#         return render(request, "weather_app/index.html")
    
#     #Then outsource a function or a functionality, of the actual weatherapp request in2 a a sperate function and not an api endpoint
    
# def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
#     #Send a request to the api, get a response and get certain feilds from that response ,take the information and render it into a template
#     response =  requests.get(current_weather_url.format(city,api_key)).json
#     lat , lon =  response['coord']['lat'] , response['coord']['laat']
#     forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json
    
    
#     weather_data = {
#         'city':city,
#         'tempertaure' : round(response['main']['temp'] - 273.15, 2),
#         'description' : response['weather'][0]['description'],
#         'icon': response['weather'][0]['icon']
             
#     }
      
#     daily_forecasts = []
#     for daily_data in forecast_response['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['max'] -273.15, 2),
#             'max_temp': round(daily_data['temp']['min'] -273.15, 2),
#             'description' :  daily_data['weather'][0]['description'],
#             'icon': response['weather'][0]['icon']
#         })
        
    
#     return weather_data, daily_forecasts