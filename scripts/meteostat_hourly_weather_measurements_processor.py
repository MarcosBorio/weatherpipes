from src.utils.generate_hash import generate_hash

def meteostat_hourly_weather_measurements_processor(raw_data):
    try:

        raw_data = raw_data.reset_index() #Convertir indexes station and time en columnas
        raw_data['source'] = 'Meteostat' #Añado fuente
        raw_data.rename(columns={'station':'stationid'},inplace=True)
        raw_data['hourlyweathermeasurementid'] = raw_data.apply(generate_hash, axis=1, columns={'stationid','time'})#Generates a unique hash based on the specified columns
        raw_data = raw_data[['hourlyweathermeasurementid','stationid','time','temp','rhum','prcp','wdir','wspd','wpgt','pres','source']]
        raw_data = raw_data.dropna() #Quitar registros que tengan algun valor nulo

    except Exception as e:

        print(f"Error processing hourly measurements from meteostat: {e}")
        raise RuntimeError(f"Error in function meteostat_hourly_weather_measurements_processor: {e}")
    
    return raw_data
        
