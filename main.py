import geocode
import get_optimal_route
from dicc import *

def get_input():
    print("The input can be given in 2 different ways")
    print("Adress(street & number) or coords")

    waypoints:str = []

    while True:
        i = input("Input the coordinates or 's' to stop: ")
        if i.lower() == 's':
            break
        name = input("Name of the point: ")
        waypoints.append((name, process_input(i)))
    return waypoints


def process_input(point) -> tuple:
        try:
            return process_coords(point)
        except ValueError:
            return process_address(point)

# Will try to parse coordinates in str to tuple[float,float], will work if the input is two numbers separated by ','
def process_coords(point) -> tuple[float,float]:
    # Attempt to parse coordinates in the format "(lat, lon)"
    coord_point = point.strip().replace("(", "").replace(")", "")
    lat, lon = map(float, coord_point.split(","))
    return (lat, lon)

# Will ask for more information about the address, then send the info to the geocode module
def process_address(point) -> tuple[float,float]:
    # Handle user-provided address input
    point_dict = {"direccion": point}
    print("Insert the following information if needed/known, else 'x'")
    country = input("Country (ISO): ").strip()
    province = input("Province: ").strip()
    city = input("City: ").strip()
    postalcode = input("Postal Code: ").strip()
    
    if country.lower() != 'x':
        point_dict["country"] = country
    if province.lower() != 'x':
        point_dict["province"] = province
    if city.lower() != 'x':
        point_dict["city/barrio"] = city
    if postalcode.lower() != 'x':
        point_dict["postalcode"] = postalcode
    
    # Convert address to coordinates (requires `geocode` module)
    try:
        res =  geocode.direccion_to_coord(point_dict)
        if res == None:
            print("Error finding address, try again with more/less information")
            point = input("Insert address: ")
            return process_address(point)
        else:
            return res
    except Exception as e:
        print(f"Error converting address to coordinates: {e}")
        return None



list = get_input()
waypoints = []

# Fill dicc & waypoints list
for i in list:
    coordsRaw[i[0]] = i[1]
    waypoints.append(i[1])
processDicc()

if len(waypoints) > 1:
    ruta = get_optimal_route.get_optimized_route(waypoints)
    get_optimal_route.to_string(ruta)
else:
    get_optimal_route.to_string(waypoints)
