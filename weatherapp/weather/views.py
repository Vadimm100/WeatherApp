from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = 'bf53aaac527442ff6e65d719edd86cbc'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    cities = City.objects.all()
    all_cities = []
    if len(cities) == 4:
        cities = City.objects.all()[0].delete()
    for city in cities:
        try:
            res = requests.get(url.format(city)).json()
            city_info = {
                'city': city,
                'temp': res["main"]['temp'],
                'icon': res['weather'][0]['icon'],
                'wind': res['wind']['speed'],
                'humidity': res['main']['humidity']
            }
            all_cities.append(city_info)
        except KeyError:
            print()
    context = {'all_info': all_cities[::-1], 'form': form}
    return render(request, 'weather/index.html', context)
