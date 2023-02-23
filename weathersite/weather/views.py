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
    if request.method == 'POST':
        latLon = mapboxRequest(request)
        temps = weatherRequest(latLon = latLon)
        print(temps)

    call = Request.objects.order_by('-request_date').first
    context = {'request': call}
    return render(request, 'weather/result.html', context)

def history(request):
    requests = Request.objects.order_by('-request_date')
    context = {'requests': requests}
    return render(request, 'weather/history.html', context)


def mapboxRequest(request):
    addon = str(request.POST.get('address'))
    addon.replace(" ", "%20")
    newUrl = mapboxURL + addon + '.json'

    PARAMS = {'access_token':mapboxAPIKey}
    r = requests.get(url = newUrl, params = PARAMS)

    data = r.json()
    # print(data)
    
    latitude = data['features'][0]['center'][0]
    longitude = data['features'][0]['center'][1]
    formatted_address = data['features'][0]['place_name']

    # printing the output
    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
        %(latitude, longitude,formatted_address))
    return [latitude, longitude]

def weatherRequest(latLon):
    time = datetime.datetime.utcnow()
    strTime = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    params = "t_2m:C,t_min_2m_24h:C,t_max_2m_24h:C" #temprature
    format = "json"

    newUrl = weatherURL + strTime + "/" + params + "/" + str(latLon[0]) + "," + str(latLon[1]) + "/" + format

    r = requests.get(url = newUrl, auth=HTTPBasicAuth(username, password))
    data = r.json()
    print(newUrl)
    currentTempC = data['data'][0]['coordinates'][0]['dates'][0]['value']
    minTempC = data['data'][1]['coordinates'][0]['dates'][0]['value']
    maxTempC = data['data'][2]['coordinates'][0]['dates'][0]['value']

    return (currentTempC, minTempC, maxTempC)
