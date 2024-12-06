import os
from src.database.connections import create_engine_connection
from src.database.query import execute_query
from src.database.insert import insert_dataframe
from dotenv import load_dotenv
from src.utils.create_circular_geometry import create_circular_geometry
from pyobis import occurrences
from scripts.obis_sightings_processor import obis_sightings_processor
from src.database.query import execute_query
from sqlalchemy import MetaData, Table

def obis_sightings_pipeline():
    try:
        load_dotenv()
        conn_str = os.getenv('DB_CONNECTION_STRING')

        # Step 1 - Establish connection to the database
        engine = create_engine_connection(conn_str)

        # Step 2 - Fetch station information
        query = "SELECT stationid,latitude,longitude FROM raw_meteostat.stations"
        stations = execute_query(query, engine)

        # Step 3 - Select the needed columns from obis API
        expected_fields = ['id', 'eventDate', 'year', 'month', 'day', 'scientificName', 'vernacularName', 'species', 'genus', 'family', 'phylum', 'kingdom', 'decimalLatitude', 'decimalLongitude','waterBody',
                            'locality', 'country', 'sst', 'sss', 'bathymetry', 'shoredistance', 'depth', 'basisOfRecord', 'coordinateUncertaintyInMeters', 'occurrenceStatus', 'datasetName', 'scientificNameID']

        # Step 4 - Process each station
        for i in stations.itertuples(name='stations'):
            stationid = i[1] 
            latitude = i[2]
            longitude = i[3]

            query = f"Select max(sightingid) as max_sightingid from raw_obis.sightings where stationid = '{stationid}'"
            
            last_sighting = execute_query(query=query,engine=engine,is_select=True)['max_sightingid'][0]

            geometria = create_circular_geometry(latitude, longitude, radius_km=15)

            query = occurrences.search(
                    occurrenceStatus='present',
                    hasCoordinate=True,
                    hasGeospatialIssue=False,
                    marine=True,
                    fields=expected_fields,
                    geometry=geometria,
                    after=last_sighting)

            raw_data = query.execute()

            processed_data= obis_sightings_processor(raw_data,expected_fields,stationid)

            #Step 5 - Delete from target the rows to insert, since there could be the same sighting in different station
            metadata = MetaData()

            table = Table('sightings',metadata, autoload_with=engine, schema='raw_obis')

            sightingids_to_delete = processed_data['sightingid'].tolist()

            with engine.connect() as conn:
                conn.execute(table.delete().where(table.c.sightingid.in_(sightingids_to_delete)))

            #Step 6 - Insert new data to target table
            insert_dataframe(dataframe=processed_data, target_schema='raw_obis',
                                    target_table='sightings', engine=engine, 
                                    chunk_size=10000, if_exists='append')
        
    except Exception as e:
        print(f"Error in function obis_sightings_pipeline: {e}")
        raise RuntimeError(f"Error in functionobis_si ghtings_pipeline: {e}")

    finally:
        # Ensure the connection is closed properly
        engine.dispose()
        print(f"Connections closed successfully")