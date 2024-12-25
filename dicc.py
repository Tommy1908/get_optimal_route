import math

coordsRaw = {}

coords = {}
names = {}

def processDicc():
    print(coordsRaw)
    for k,v in coordsRaw.items():
        coords[k] = (round(v[0], 5), round(v[1], 5))

    for k,v in coordsRaw.items():
        names[(round(v[0], 5), round(v[1], 5))] = k


def puntoMasCercano(server,diccionario):
    minimo:int = -1
    valor:str = None

    for k,v in diccionario.items():
        a = math.sqrt(math.pow(k[0]-server[0], 2) + math.pow(k[1]-server[1], 2))
        if minimo == -1:
            minimo = a
            valor = k
        elif a <= minimo:
            minimo = a
            valor = k
    
    return valor