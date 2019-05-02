# A branch python operator is an operator that allows you to let your DAG take
# different paths based on conditions. The callable function should return the
# task_id of the task that should be executed next. The task should be an
# immediate downstream child of the BranchPythonOperator
from airflow.operators.python_operator import BranchPythonOperator
# A dummy operator is an operator that does nothing. I use it to make a dag
# more readable
from airflow.operators.dummy_operator import DummyOperator



# Python function to check wether there are files to process. We use this as
# the callable of the BranchPythonOperator, so it will need to return the task
# ids of the tasks to branch to.
def path_exists(path, file_glob, true_path, false_path):
    import glob
    if len(glob.glob(f"{path}/{file_glob}")) > 0:
        return true_path
    else:
        return false_path


SOURCE_PATH = ("{{ var.value.base_data_path }}/raw/laptop_stats_collector/"
               "{{ execution_date.strftime('%Y/%m/%d/%H') }}")


check_if_load_files_exists_task = BranchPythonOperator(
    task_id="check_if_load_files_exists",
    python_callable=path_exists,
    op_kwargs={
        'path': SOURCE_PATH,
        'file_glob': 'load_*.txt',
        'true_path': 'load_files_exists',
        'false_path': 'load_files_do_not_exists'
    },
    dag=dag
)

# Dummy operators to make the DAG more readable. You could move on to the tasks
# that need to be executed next immediately ofcourse
load_files_exists_task = DummyOperator(
    task_id='load_files_exists',
    dag=dag
)

load_files_do_not_exists_task = DummyOperator(
    task_id='load_files_do_not_exists',
    dag=dag
)

check_if_load_files_exists_task >> [load_files_exists_task,
                                    load_files_do_not_exists_task]
