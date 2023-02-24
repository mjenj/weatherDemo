import requests
from requests.auth import HTTPBasicAuth
import datetime
from django.shortcuts import render
from django.http import HttpResponse

from .models import Request, Weather

# Create your views here.
#API Keys and login details removed for security

mapboxURL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
mapboxAPIKey = "xxxxxxxxxxxxxxxxxxxxxxx"

username = "xxxxxxx"
password = "xxxxxxxxx"

weatherURL = "https://api.meteomatics.com/"

def index(request):
    context = {'request': request}
    return render(request, 'weather/index.html', context)

def result(request):
    success = False
    if request.method == 'POST':
        address, latLon = mapboxRequest(request)
        if address is not None:
            temps = weatherRequest(latLon = latLon)
            if temps is not None:
                success = True
                saveToDB(address=address, temps=temps)


    call = Weather.objects.order_by('-request__request_date').first()
    context = {'weather': call, 'success':success}
    return render(request, 'weather/result.html', context)

def history(request):
    weather_history = Weather.objects.order_by('-request__request_date').all
    context = {'weather_history': weather_history}

    return render(request, 'weather/history.html', context)


## Data functions

def mapboxRequest(request):
    addon = str(request.POST.get('address'))
    addon.replace(" ", "%20")
    newUrl = mapboxURL + addon + '.json'
    print(newUrl)

    PARAMS = {'access_token':mapboxAPIKey}
    r = requests.get(url = newUrl, params = PARAMS)

    data = r.json()
    print(data)
    if len(data['features']) > 0:
        longitude = data['features'][0]['center'][0]
        latitude = data['features'][0]['center'][1]
        formatted_address = data['features'][0]['place_name']

        # printing the output
        print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
            %(latitude, longitude,formatted_address))
        return (formatted_address, [latitude, longitude])
    else:
        print("No location found")
        return (None,None)

def weatherRequest(latLon):
    time = datetime.datetime.utcnow()
    strTime = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    params = "t_2m:C,t_min_2m_24h:C,t_max_2m_24h:C" #temprature
    format = "json"

    newUrl = weatherURL + strTime + "/" + params + "/" + str(latLon[0]) + "," + str(latLon[1]) + "/" + format

    r = requests.get(url = newUrl, auth=HTTPBasicAuth(username, password))
    print(newUrl)

    try:
        data = r.json()
    except:
        print("Error parsing weather data, request response \n" + str(r))
        return

    currentTempC = data['data'][0]['coordinates'][0]['dates'][0]['value']
    minTempC = data['data'][1]['coordinates'][0]['dates'][0]['value']
    maxTempC = data['data'][2]['coordinates'][0]['dates'][0]['value']

    return (currentTempC, minTempC, maxTempC)

def saveToDB(address, temps):
    req = Request(address_text = address, request_date = datetime.datetime.now())
    req.save()

    weather = Weather(request = req, currentTemp = temps[0], maxTemp = temps[1], minTemp = temps[2])
    weather.save()
