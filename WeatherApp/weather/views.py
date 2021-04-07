from django.shortcuts import render
import requests 
import json 
from .models import WeatherData
from .serializer import WeatherSerializers
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
    
def getWeatherforLocation(request):
    
    if request.method == 'POST':
        
        postal_code = request.POST['postlcode']
        AppKey = 'ZbuM8bKuU663YLm4hVV2ebt7WB0UKVsq'
        
        url_location = 'http://dataservice.accuweather.com/locations/v1/postalcodes/search?q={qparam}&apikey={appkey}'
        response_location = requests.get(url_location.format(qparam = postal_code,appkey = AppKey))
        location_json_data = json.loads(response_location.text)

        # location_key = location_json_data[0]['Key']
        location_key = 501789
        #To Do : Needs to raise error and display that on page for response code errors like 400 
        # {'Code': '400', 'Message': 'Invalid location key: None' & Redirect to same page to ask correct postal code
        
        weather_url = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/{locationKey}?apikey={appkey}" 
        response_weather = requests.get(weather_url.format(locationKey = location_key, appkey = AppKey ))
        weather_json_data = json.loads(response_weather.text)
        
        print ('weather_json_data is ',weather_json_data)
        #get Model Data
        wea_model_data, created = WeatherData.objects.get_or_create(
            zipcode = postal_code,
            country = location_json_data[0]['Country']['LocalizedName'],
            state = location_json_data[0]['AdministrativeArea']['LocalizedName'],
            weather = weather_json_data['Headline']['Text'],
            max_temp = getMaxTemperature(weather_json_data),
            min_temp = getMinTemperature(weather_json_data),
            unit_type = 'F'
        )
        # wea_model_data, created = WeatherData.objects.get_or_create(
        #     zipcode = 517421,
        #     country = 'India',
        #     state = 'Andhra Pradesh',
        #     weather = 'High Tempersture',
        #     max_temp = 78,
        #     min_temp = 64,
        #     unit_type = 'F',
        # )
        
        #weather_json_data is  {'Code': 'ServiceUnavailable', 
        # 'Message': 'The allowed number of requests has been exceeded.', 
        # 'Reference': '/forecasts/v1/daily/1day/None?apikey=ZbuM8bKuU663YLm4hVV2ebt7WB0UKVsq'}
        #
        # wea_model_data.save()

        serializer_data = WeatherSerializers(wea_model_data.__dict__)
        search_results = serializer_data.data
        print ('search_results are', search_results)
        #key is going to reger in the template 
        return render(request, 'weather/display.html', {'search_results':search_results})
        
    
def getMaxTemperature(response_data):
    for d in response_data["DailyForecasts"]:
        return d['Temperature']['Minimum']['Value']


def getMinTemperature(response_data):
    for d in response_data["DailyForecasts"]:
        return d['Temperature']['Maximum']['Value']
    