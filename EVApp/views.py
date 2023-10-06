from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

base_dir = settings.BASE_DIR


# Create your views here.
@csrf_exempt
def test(request):
    if request.method.lower() == 'post':
        request_data = json.loads(request.body)
        print(request_data)
        all_data = open(f'{base_dir}/EVApp/static/location.json')
        data = json.load(all_data)  # json formatted string
        mapData = dict()
        city = request_data['body']['city']
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        mapData['location'] = {'longitude' : location.longitude , 'lattitude' : location.latitude}
        mapData['list'] = []
        for each in data['Sheet1']:
            if each['state'].lower() == request_data['body']['state'].lower() \
                    and each['city'].lower() == request_data['body']['city'].lower():
                mapData['list'].append(each)
        all_data.close()
        return JsonResponse(mapData, safe=False)
    return HttpResponse()


