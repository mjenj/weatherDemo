import requests
from requests.auth import HTTPBasicAuth
import datetime
from django.shortcuts import render
from django.http import HttpResponse

from .models import Request, Weather

#A PI Keys and login details removed for security
mapboxURL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
mapboxAPIKey = "xxxxxxxxxxxxxxxxxxxxxxx"

username = "xxxxxxx"
password = "xxxxxxxxx"

weather_URL = "https://api.meteomatics.com/"

## Views
def index(request):
    context = {'request': request}
    return render(request, 'weather/index.html', context)

def result(request):
    success = False
    if request.method == 'POST':
        address, lat_lon = mapbox_request(request)
        if address is not None: # Check that the mapbox request worked as intended
            temps = weather_request(lat_lon = lat_lon)
            if temps is not None: # Check that the weather API request worked as intended
                success = True
                save_to_database(address=address, temps=temps)


    call = Weather.objects.order_by('-request__request_date').first() # Get last DB entry
    context = {'weather': call, 'success':success}
    return render(request, 'weather/result.html', context)

def history(request):
    weather_history = Weather.objects.order_by('-request__request_date').all # Get all DB entries
    context = {'weather_history': weather_history}

    return render(request, 'weather/history.html', context)


## Data functions

def mapbox_request(request):
    addon = str(request.POST.get('address'))
    addon.replace(" ", "%20")
    newUrl = mapboxURL + addon + '.json'

    params = {'access_token':mapboxAPIKey}
    r = requests.get(url = newUrl, params = params)

    data = r.json()

    # Parse json data for needed values
    if len(data['features']) > 0:
        longitude = data['features'][0]['center'][0]
        latitude = data['features'][0]['center'][1]
        formatted_address = data['features'][0]['place_name']
        return (formatted_address, [latitude, longitude])
    else:
        print("No location found")
        return (None,None)

def weather_request(lat_lon):
    time = datetime.datetime.utcnow()
    string_time = time.strftime('%Y-%m-%dT%H:%M:%SZ') # Save timezone aware time format
    params = "t_2m:C,t_min_2m_24h:C,t_max_2m_24h:C" # Params used by weather API for current, min and max tempratures
    format = "json"

    new_URL = weather_URL + string_time + "/" + params + "/" + str(lat_lon[0]) + "," + str(lat_lon[1]) + "/" + format
    r = requests.get(url = new_URL, auth=HTTPBasicAuth(username, password))

    try:
        data = r.json()
    except:
        print("Error parsing weather data, request response \n" + str(r))
        return

    # Parse json data for needed values
    current_temp_C = data['data'][0]['coordinates'][0]['dates'][0]['value']
    min_temp_C = data['data'][1]['coordinates'][0]['dates'][0]['value']
    max_temp_C = data['data'][2]['coordinates'][0]['dates'][0]['value']

    return (current_temp_C, min_temp_C, max_temp_C)

def save_to_database(address, temps):
    req = Request(address_text = address, request_date = datetime.datetime.now())
    req.save()

    weather = Weather(request = req, currentTemp = temps[0], maxTemp = temps[1], minTemp = temps[2])
    weather.save()
