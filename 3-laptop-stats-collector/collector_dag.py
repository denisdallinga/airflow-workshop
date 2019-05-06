from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates
from datetime import timedelta


default_args = {
    'owner': 'connect',
    'start_date': dates.days_ago(1)
}

dag = DAG(
    dag_id='laptop_stats_collector',
    default_args=default_args,
    description='Collects statistics about my laptop',
    schedule_interval=timedelta(minutes=1),
    catchup=False
)

DATA_PATH = ("{{ var.value.base_data_path }}/raw/{{ dag.dag_id }}/"
             "{{ execution_date.strftime('%Y/%m/%d/%H') }}")

create_data_directory_task = BashOperator(
    task_id='create_data_directory',
    dag=dag,
    bash_command=f"mkdir -p {DATA_PATH}"
)


def collect_load(dir, file_name):
    import os
    load_averages = os.getloadavg()
    minutely_average = load_averages[0]

    with open(f"{dir}/{file_name}", 'w') as file:
        file.write(str(minutely_average))


collect_laptop_load_task = PythonOperator(
    task_id='collect_laptop_load',
    dag=dag,
    python_callable=collect_load,
    op_kwargs={
        "dir": DATA_PATH,
        "file_name": "load_{{ execution_date.strftime('%Y%m%d%H%M') }}.txt"
    }
)

collect_open_chrome_tabs_command = (
    "ps -ef | grep Chrome | grep type=renderer | wc -l | sed 's/ //g' > "
    + DATA_PATH +
    "/open_chrome_tabs_{{ execution_date.strftime('%Y%m%d%H%M') }}.txt"
)

collect_open_chrome_tabs_task = BashOperator(
    task_id='collect_open_chrome_tabs',
    dag=dag,
    bash_command=collect_open_chrome_tabs_command
)

create_data_directory_task >> [collect_laptop_load_task,
                               collect_open_chrome_tabs_task]
