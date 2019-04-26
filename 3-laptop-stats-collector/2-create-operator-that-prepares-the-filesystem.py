#Import the bash operator
from airflow.operators.bash_operator import BashOperator

# Instantiate a Operator. On instance of an operator is called a task
create_base_directory_task = BashOperator(
    # The task id should be unique within the
    task_id='create_base_data_directory',
    dag=dag,
    # Some parameters accept jinja templates and will resolve them when being
    # executed by the scheduler. The bash_command parameter of the BashOperator
    # is one of them. We use an Airflow Variable to read the base data path and
    # we partition the directories by the execution hour of the operator. For
    # more info about macros you can use in templated parameters:
    bash_command=(
        "mkdir -p {{ var.value.base_data_path }}/raw/{{ dag.dag_id }}/"
        "{{ execution_date.strftime('%Y/%m/%d/%H') }}"
    )
)
