from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from app import run_news_etl

# Initializing  Default args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # mention the start date of your DAG run
    'start_date': datetime(2023, 3, 26),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Defining the DAG
dag = DAG(
    'news_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    # edit the schedule interval to how frequently the DAG should create a DAG instance 
    schedule_interval=timedelta(hours=1),
    # catchup set to False. When False, the scheduler creates a DAG run only for the latest interval.
    catchup=False
)

# Defining the task - a python callable. Here it the main function from app.py
run_etl = PythonOperator(
    task_id='complete_news_etl',
    python_callable=run_news_etl,
    dag=dag, 
)
# invoking the task
run_etl