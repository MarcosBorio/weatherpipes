# pip install meteostat

## Testear importacion de un punto
## Almacenar en bbdd dimensional

from meteostat import Stations, Hourly, Daily

stations = Stations()
stations = stations.inventory('hourly') #Solo obtener estaciones que tengan informacion historica por hora.
station = stations.fetch(5)
station = station[station['elevation'] < 100] # Obtener todas las estaciones que estan a menos de 100 metros del nivel del mar.

data = Hourly(station)
data = data.normalize() #Quitar gaps de series
data = data.fetch()
##Determinar parametros principales para garantizar completitud con chatgpt y filtrar en dataset solo rows completas
##Insertar datos en la base de datos y chequear data (station y data)
##Crear data extractor principal para guardar informacion historica, cacheando errores y haciendo buffers para que no sea de una vez.  

print(data.head(150))






#from meteostat import Point, Daily
#from datetime import datetime

# Define la ubicación (por ejemplo, una playa específica)
#location = Point(41.5794, 2.5522)  # Latitud y Longitud

# Define el rango de fechas
#start = datetime(2024, 1, 1)
#end = datetime(2024, 2, 25)

# Obtén los datos climáticos diarios
#data = Daily(location, start, end)
#data = data.fetch()

# Muestra los datos
#print(data)
