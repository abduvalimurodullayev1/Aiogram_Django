import aiohttp
import math


async def get_address(longitude, latitude, lang='uzbek'):
    language = {
        'uzbek': "uz_UZ",
        'russian': "ru_RU",
        'english': "en_US"
    }
    params = {
        'apikey': '0de10148-40f0-426d-aed6-7b31787ffb83',
        'geocode': f'{longitude},{latitude}',
        "lang": language[lang],
        "kind": "house",
        'format': 'json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://geocode-maps.yandex.ru/1.x/', params=params) as response:
            response = await response.json()

    return response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
        "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]


async def haversine(lon1, lat1, lon2, lat2):
    radius = 6371

    lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance

