from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from  pipelines.meteostat_stations_pipeline import meteostat_stations_pipeline

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024,11,14),
    'schedule_interval': '@weekly',
    'description': 'Performing a full refresh of the raw_meteostat.stations table on a weekly basis.'
}

with DAG(dag_id='meteostat_stations_fullrefresh_dag',default_args=default_args) as meteostat_stations_fullrefresh_dag:

    run_meteostat_stations_fullrefresh_task = PythonOperator(
    task_id='run_meteostat_stations_fullrefresh_task',
    python_callable=meteostat_stations_pipeline,
    retries=5
    )

    run_meteostat_stations_fullrefresh_task