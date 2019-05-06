# Import a python operator
from airflow.operators.python_operator import PythonOperator


# Function that gets the load from the os and writes it to a file
def collect_load(dir, file_name):
    import os
    load_averages = os.getloadavg()
    minutely_average = load_averages[0]

    with open(f"{dir}/{file_name}", 'w') as file:
        file.write(str(minutely_average))


collect_laptop_load_task = PythonOperator(
    task_id='collect_laptop_load',
    dag=dag,
    # Pass a python callable as parameter. This is a function that is executed
    # by the operator
    python_callable=collect_load,
    # Pass key word arguments. They can also be templated
    op_kwargs={
        "dir": ("{{ var.value.base_data_path }}/raw/{{ dag.dag_id }}/"
                "{{ execution_date.strftime('%Y/%m/%d/%H') }}"),
        "file_name": "load_{{ execution_date.strftime('%Y%m%d%H%M') }}.txt"
    }
)
