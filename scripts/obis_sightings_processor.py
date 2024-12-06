def obis_sightings_processor(raw_data,expected_fields,stationid):
    try:
        
        # Add missed columns on the dataset
        for col in expected_fields:
            if col not in raw_data.columns:
                raw_data[col] = None

        # Reorganize and lowercase columns names for database insertion
        processed_data = raw_data[expected_fields]
        processed_data.columns = processed_data.columns.str.lower()

        # Rename columns to align with the database schema
        processed_data.rename(columns={'id': 'sightingid'}, inplace=True)

        processed_data['source'] = 'OBIS'

        processed_data.replace(to_replace='NULL',value=None, inplace=True)
      
        processed_data['stationid'] = stationid

        print("Raw sightings data processed successfully")
        
    except Exception as e:
        # Print the error and raise a RuntimeError for higher-level handling
        print(f"Error processing sightings from OBIS: {e}")
        raise RuntimeError(f"Error in function obis_sightings_processor: {e}")
    
    return processed_data
