from airflow import DAG
from airflow.utils import dates


default_args = {
    'owner': 'connect',
    'start_date': dates.days_ago(1)
}

dag = DAG(
    dag_id='laptop_stats_aggregator',
    default_args=default_args,
    description='Aggregates laptop stats and sends them over Slack',
    # This dags runs every hour and aggregates the data collected in the previous
    # hour
    schedule_interval='@hourly',
    catchup=True
)
