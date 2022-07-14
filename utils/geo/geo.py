from geopy.distance import distance
from geopy.geocoders import Nominatim, Photon
from geopy.adapters import AioHTTPAdapter
from fake_useragent import UserAgent
from .funcs import get_location
import asyncio


async def get_geowork(coordinates=False, name=False, need_coordinates=False, need_name=False):
    await asyncio.sleep(1)
    ua = UserAgent().random
    async with Nominatim(user_agent=ua, adapter_factory=AioHTTPAdapter) as geolocator:
        location = await get_location(geolocator, coordinates, name)
        if location:
            if name and need_name:
                location = await get_location(geolocator, get_coordinates(location))
            return get_res(location, need_coordinates, need_name, nominatim=True)
    
    async with Photon(user_agent=ua, adapter_factory=AioHTTPAdapter) as geolocator:
        location = await get_location(geolocator, coordinates, name)
        if location:
            return get_res(location, need_coordinates, need_name, photon=True)
    return False



def get_res(location, need_coordinates=False, need_name=False, nominatim=False, photon=False):
    res = []
    if need_coordinates:
        res_coor = get_coordinates(location)
        if need_name:
            res.append(res_coor)
        else:
            return res_coor
    if need_name:
        res_name = get_name(location, nominatim, photon)
        if need_coordinates:
            res.append(res_name)
        else:
            return res_name
    return res



def get_coordinates(location):
    return [location.latitude, location.longitude]



def get_name(location, nominatim=False, photon=False):
    if nominatim:
        try:
            res = location.raw['address']['city']
        except:
            try:
                res = location.raw['address']['town']
            except:
                try:
                    res = location.raw['address']['state']
                except:
                    res = location.raw['address']['county']
    if photon:
        try:
            res = location.raw['properties']['city']
        except:
            try:
                res = location.raw['properties']['name']
            except:
                res = location.raw['properties']['state']
    return res


def sort_distance_cities(cities, user_city):
    if len(cities) == 0:
        return False
    elif len(cities) == 1:
        return [{'id': cities[0]['id'], 'name': cities[0]['name'], 'coordinates': cities[0]['coordinates']}]
        
    result = []
    for city in cities:
        lenght = distance((city['coordinates'][0], city['coordinates'][1]), (user_city['coordinates'][0], user_city['coordinates'][1])).km
        result.append([int(lenght), {'id': city['id'], 'name': city['name'], 'coordinates': city['coordinates']}])

    for i in range(len(result)):
        for j in range(len(result)-i-1):
            if result[j][0] > result[j+1][0]:
                result[j], result[j+1] = result[j+1], result[j]
    res = []
    for i in result:
        res.append(i[1])
    return res