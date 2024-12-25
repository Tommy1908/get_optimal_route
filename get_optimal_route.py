from dicc import *
import requests
import itertools

# Función para obtener la matriz de distancias desde la API de OSRM
def get_distance_matrix(coords):
    base_url = "https://router.project-osrm.org/table/v1/driving/"
    
    # Preparar la cadena de coordenadas para la API Table
    coords_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
    
    # Llamada a la API Table de OSRM con anotaciones para distancia
    url = f"{base_url}{coords_str}?annotations=distance"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'distances' in data:
            return data['distances']
        else:
            raise Exception("No se encontraron datos de distancias en la respuesta.")
    else:
        raise Exception(f"Error al obtener datos de OSRM: {response.status_code}, {response.text}")

# TSP para encontrar la mejor ruta
def solve_tsp(distance_matrix):
    n = len(distance_matrix)
    waypoints = list(range(n))  # Aca usa todos los puntos, no tiene un inicio o final fijo
    all_routes = itertools.permutations(waypoints)
    min_distance = float('inf')
    best_route = None

    # Aca se evaluan todas las rutas
    for route in all_routes:
        route_distance = 0
        for i in range(len(route) - 1):
            route_distance += distance_matrix[route[i]][route[i + 1]]
        
        if route_distance < min_distance:
            min_distance = route_distance
            best_route = route

    return best_route

# Funcion principal
def get_optimized_route(waypoints) -> list[tuple[float,float]]:
    print("qaaaa")
    print(waypoints)
    distance_matrix = get_distance_matrix(waypoints)
    best_route = solve_tsp(distance_matrix)

    # Arma la lista con el orden optimo
    optimized_order = [waypoints[i] for i in best_route]
    return optimized_order

def to_string(ruta):
    mapsUrl = "https://www.google.com.ar/maps/dir"
    for i, point in enumerate(ruta):
        print(f"{i + 1}: {names[puntoMasCercano(point,names)]}")
        mapsUrl += f"/'{point[0]},{point[1]}'"
    print(mapsUrl)