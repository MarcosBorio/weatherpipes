import os
from src.database.connections import create_engine_connection
from src.database.query import fetch_data
from meteostat import Hourly
from scripts.meteostat_hourly_weather_measurements_processor import meteostat_hourly_weather_measurements_processor
from src.database.insert import insert_dataframe
from dotenv import load_dotenv

#Modularizar el pipeline y hacer correcto manejo de errores con runtimeerrors en funciones especificas y catch en el main. Ver chatgpt.
def meteostat_hourly_weather_measurements_pipeline(stations_chunk_size=10):

    try:
        #Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        conn_str = os.getenv('DB_CONNECTION_STRING')

        #Step 1 - Connect to the database
        engine = create_engine_connection(conn_str)

        #Step 2 - Get raw data iterating over stored stations and insert processed data 
        query = 'Select stationid from raw_meteostat.stations limit' #Obtain stations ids from abbys database
        stationids_list = fetch_data(query,engine)['stationid'].to_list()
        total_stations = len(stationids_list)
        print(f"Total de estaciones a obtener informacion: {total_stations}")

        for i in range(0,total_stations,stations_chunk_size):
            stations_chunk = stationids_list[i:i + stations_chunk_size]
            print(f"Obteniendo estaciones {i+1} a {i + len(stations_chunk)} de la tabla raw_meteostat.stations")
            raw_data = Hourly(stations_chunk).fetch() #Obtain raw hourly measurements from Meteostat

            #Step 3 - Process raw data
            processed_data = meteostat_hourly_weather_measurements_processor(raw_data)

            #Step 4 - Insert processed data into target table
            insert_dataframe(dataframe=processed_data,target_schema='raw_meteostat',target_table='hourly_weather_measurements',engine=engine,chunk_size=10000)

    except Exception as e:
        print(f"Error in function meteostat_hourly_weather_measurements_pipeline: {e}")

    finally:
       engine.dispose()
       print(f"Sesiones cerradas correctamente")        

    
    
    #Mejorar mensajes y docu
    #Luego seguir con los tipos de extraccion
        ##habra 2 metodos para insertar incremental, uno por id y otro por fecha. De momento ambas tablas son por id ya que hay ID unico en ambas
        #Hacer full refresh historico tambien
    
