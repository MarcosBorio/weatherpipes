from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pipelines.meteostat_hourly_weather_measurements_pipeline import meteostat_hourly_weather_measurements_pipeline
from pipelines.meteostat_stations_pipeline import meteostat_stations_pipeline
from pipelines.obis_sightings_pipeline import obis_sightings_pipeline


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024,11,24),
    'schedule_interval': '@daily',
    'description': 'Performing full refresh of meteostat stations and then incremental of both meteostat weather measurements and obis sightings'
}

with DAG(dag_id='twp_raw_data_dag',default_args=default_args) as twp_raw_data_dag:

    run_meteostat_stations_fullrefresh = PythonOperator(
    task_id='run_meteostat_stations_fullrefresh',
    python_callable=meteostat_stations_pipeline,
    retries=5
    )
    
    run_meteostat_hourly_weather_measurements_incremental_task = PythonOperator(
    task_id='run_meteostat_hourly_weather_measurements_incremental_task',
    python_callable=meteostat_hourly_weather_measurements_pipeline,
    retries=5
    )

    run_obis_sightings_incremental_task = PythonOperator(
    task_id='run_obis_sightings_incremental_task',
    python_callable=obis_sightings_pipeline,
    retries=5
    )

    run_meteostat_stations_fullrefresh >> run_meteostat_hourly_weather_measurements_incremental_task
    run_meteostat_stations_fullrefresh >> run_obis_sightings_incremental_task