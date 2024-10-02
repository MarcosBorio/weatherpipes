import os
from meteostat import Stations
from sqlalchemy import create_engine
from src.database.insert import insert_dataframe
from scripts.meteostat_stations_processor import meteostat_stations_processor
from dotenv import load_dotenv

def meteostat_stations_pipeline():

    try:
        #Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        conn_str = os.getenv('DB_CONNECTION_STRING')    

        #Step 1 - Get raw data
        stations = Stations()
        stations = stations.inventory('hourly') #Solo obtener estaciones que tengan informacion historica por hora.
        raw_data = stations.fetch()

        #Step 2 - Process raw data
        processed_data = meteostat_stations_processor(raw_data)

        #Step 3 - Insert processed data into target table
        engine = create_engine(conn_str)
        insert_dataframe(processed_data,'raw_meteostat','stations',engine)

    except Exception as e:
        print(f"Error in function meteostat_stations_pipeline: {e}")

    finally:
       engine.dispose()
       print(f"Sesiones cerradas correctamente")     