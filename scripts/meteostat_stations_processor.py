def meteostat_stations_processor(raw_data):
    
    try:
        raw_data = raw_data[raw_data['elevation'] < 100] # Obtener todas las estaciones que estan a menos de 100 metros del nivel del mar.
        raw_data = raw_data.reset_index()
        raw_data['source'] = 'Meteostat' #Añado fuente
        raw_data.rename(columns={'id': 'stationid','name':'stationname'}, inplace=True)
        processed_data = raw_data[['stationid','stationname','country','region','wmo','icao','latitude','longitude','elevation','timezone','source']]

        print("Raw station data processed successfuly")
        
    except Exception as e:
        print(f"Error processing stations from meteostat: {e}")
        raise RuntimeError(f"Error in function meteostat_stations_processor: {e}")
    
    return processed_data
        
