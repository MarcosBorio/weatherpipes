from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from  pipelines.meteostat_hourly_weather_measurements_pipeline import meteostat_hourly_weather_measurements_pipeline

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024,11,14),
    'schedule_interval': '@daily',
    'description': 'Performing an incremental load of the raw_meteostat.hourly_weather_measurements table on a daily basis.'
}

with DAG(dag_id='meteostat_hourly_weather_measurements_incremental_dag',default_args=default_args) as meteostat_hourly_weather_measurements_incremental_dag:

    run_meteostat_hourly_weather_measurements_incremental_task = PythonOperator(
    task_id='run_meteostat_hourly_weather_measurements_incremental_task',
    python_callable=meteostat_hourly_weather_measurements_pipeline,
    retries=5
    )

    run_meteostat_hourly_weather_measurements_incremental_task