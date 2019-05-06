from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

RESULT_PATH = ("{{ var.value.base_data_path }}/refined/{{ dag.dag_id }}/"
               "{{ execution_date.strftime('%Y/%m/%d/%H') }}")

create_data_directory_task = BashOperator(
    task_id='create_data_directory',
    dag=dag,
    bash_command=f"mkdir -p {RESULT_PATH}"
)

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

    # Values that are returned by a callable of a PythonOperator are pushed to
    # an XCom. An XCom facilitates operator intercommunication. It can be used
    # to share meta data or context between operators, but should be used with
    # care.  In general, if two operators need to share information, like a
    # filename or small amount of data, you should consider combining them into
    # a single operator.
    return average_measurement



aggregate_metrics_task = PythonOperator(
    task_id='aggregate_load_metrics',
    python_callable=aggregate_metrics,
    op_kwargs={
        'source_path': SOURCE_PATH,
        'file_glob': 'load_*.txt',
        'result_path': RESULT_PATH,
        'result_file_name': 'load_average.txt'
    },
    dag=dag
)

aggregate_metrics_task << [create_data_directory_task, load_files_exists_task]
