# Uses Nominatim
# No heavy uses (an absolute maximum of 1 request per second).

import requests
import time
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    # Calculates the distance between two geographic points using the Haversine formula
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def geocode(direccion: str, country: str = None, provincia: str = None, barrio: str = None,
            postalcode: str = None) -> list[tuple[float, float, str]]:
    url = "https://nominatim.openstreetmap.org/search"
    headers = {'User-Agent': 'mi-geocoder-app/1.0'}

    # Params of the request
    params = {
        'q': direccion,
        'format': 'json',
        'limit': 1  # Here is the max ammount of answers, it can be used to get multiple options
    }
    if country is not None:
        params['countrycodes'] = country
    if barrio is not None:
        params['city'] = barrio
    if postalcode is not None:
        params['postalcode'] = postalcode
    if provincia is not None:
        params['state'] = provincia

    # Solicitud GET
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                return [(float(item['lat']), float(item['lon']), item['display_name']) for item in data]
        except requests.exceptions.JSONDecodeError:
            print("Error al decodificar JSON.")
    else:
        print(f"Error en la solicitud: {response.status_code}")
    return []


def direccion_to_coord(direccion_dict: dict) -> tuple:
    direccion = direccion_dict['direccion']
    country = direccion_dict.get('country')
    provincia = direccion_dict.get('provincia')
    barrio = direccion_dict.get('barrio')
    postalcode = direccion_dict.get('postalcode')

    # Llamada a geocode con los datos
    opciones = geocode(direccion, country=country, provincia=provincia, barrio=barrio, postalcode=postalcode)

    if not opciones:
        print(f"No se encontraron resultados para '{direccion}'.")
        return None

    #Si se incrementa el limit, puede haber varias opciones y trabajar con eso
    mejor_opcion = opciones[0]
    time.sleep(1)  # Delay de 1 segundo para respetar Nominatim
    return mejor_opcion[:2]