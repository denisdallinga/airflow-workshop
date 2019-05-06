from airflow import DAG
from airflow.utils import dates
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import (BranchPythonOperator,
                                               PythonOperator)

default_args = {
    'owner': 'connect',
    'start_date': dates.days_ago(1)
}

dag = DAG(
    dag_id='laptop_stats_aggregator',
    default_args=default_args,
    description='Aggregates laptop stats and sends them over Slack',
    schedule_interval='@hourly',
    catchup=True
)

SOURCE_PATH = ("{{ var.value.base_data_path }}/raw/laptop_stats_collector/"
               "{{ execution_date.strftime('%Y/%m/%d/%H') }}")
RESULT_PATH = ("{{ var.value.base_data_path }}/refined/{{ dag.dag_id }}/"
               "{{ execution_date.strftime('%Y/%m/%d/%H') }}")


def path_exists(path, file_glob, true_path, false_path):
    import glob
    if len(glob.glob(f"{path}/{file_glob}")) > 0:
        return true_path
    else:
        return false_path


def aggregate_metrics(source_path, file_glob, result_path, result_file_name):
    import glob

    file_paths = glob.glob(f"{source_path}/{file_glob}")
    total = 0
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            measured_value = file.read()
            total += float(measured_value)

    average_measurement = total / len(file_paths)

    with open(f"{result_path}/{result_file_name}", 'w') as file:
        file.write(str(average_measurement))

    return average_measurement

def send_overview_to_slack(metric_types, **context):
    from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook

    data = []
    for metric_type in metric_types:
        xcom_data = context['task_instance'].xcom_pull(
            task_ids=f"aggregate_{metric_type}_metrics"
        )
        if xcom_data:
            data.append(f"{metric_type}: {xcom_data}")

    if data:
        message = ("Hello Denis, here are your average laptop stats for "
                   f"{context['execution_date'].strftime('%Y-%m-%d %H:%M')}: "
                   f"{' '.join(data)}")
    else:
        message = ("Hello Denis, no data has been collected for "
                   f"{context['execution_date'].strftime('%Y-%m-%d %H:%M')}")

    SlackWebhookHook(http_conn_id='slack_connection', message=message).execute()

METRIC_TYPES = ['open_chrome_tabs', 'load']

send_overview_to_slack_task = PythonOperator(
    task_id="send_overview_to_slack",
    python_callable=send_overview_to_slack,
    provide_context=True,
    op_kwargs={'metric_types': METRIC_TYPES},
    dag=dag,
    trigger_rule='none_failed'
)


create_data_directory_task = BashOperator(
    task_id='create_data_directory',
    dag=dag,
    bash_command=f"mkdir -p {RESULT_PATH}"
)

for metric_type in METRIC_TYPES:
    check_if_files_exists_task = BranchPythonOperator(
        task_id=f"check_if_{metric_type}_files_exists",
        python_callable=path_exists,
        op_kwargs={
            'path': SOURCE_PATH,
            'file_glob': f"{metric_type}_*.txt",
            'true_path': f"{metric_type}_files_exists",
            'false_path': f"{metric_type}_files_do_not_exists"
        },
        dag=dag
    )

    files_exists_task = DummyOperator(
        task_id=f"{metric_type}_files_exists",
        dag=dag
    )

    files_do_not_exists_task = DummyOperator(
        task_id=f"{metric_type}_files_do_not_exists",
        dag=dag
    )

    aggregate_metrics_task = PythonOperator(
        task_id=f"aggregate_{metric_type}_metrics",
        python_callable=aggregate_metrics,
        op_kwargs={
            'source_path': SOURCE_PATH,
            'file_glob': f"{metric_type}_*.txt",
            'result_path': RESULT_PATH,
            'result_file_name': f"{metric_type}_average.txt"
        },
        dag=dag
    )

    check_if_files_exists_task >> [files_exists_task, files_do_not_exists_task]

    aggregate_metrics_task << [create_data_directory_task, files_exists_task]

    aggregate_metrics_task >> send_overview_to_slack_task
