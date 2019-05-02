from airflow import DAG
from airflow.utils import dates

from datetime import timedelta


# default arguments: These are arguments that are automatically passed to any
#                    operator that you instantiate with your DAG. This allows
#                    to easily define configuration that coutns for all of your
#                    operators.
default_args = {
    'owner': 'connect',
    'start_date': dates.days_ago(1),
}


dag = DAG(
    # dag_id: An unique identifier for the DAG
    dag_id='laptop_stats_collector',
    default_args=default_args,
    description='Collects statistics about my laptop',
    # Schedule interval: How often the a DagRun should be scheduled for this
    #                    DAG. Can be a timedelta, cron expression or a cron
    #                    preset
    schedule_interval=timedelta(minutes=1),
    # catchup: Wether a backfill should be performed for the dag or not. As the
    #          metrics we are collecting are a snapshot in time, a backfill
    #          would not be usefull here
    catchup=False
)
