DATA_PATH = ("{{ var.value.base_data_path }}/raw/{{ dag.dag_id }}/"
             "{{ execution_date.strftime('%Y/%m/%d/%H') }}")
