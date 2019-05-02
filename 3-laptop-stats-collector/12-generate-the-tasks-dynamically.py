METRIC_TYPES = ['open_chrome_tabs', 'load']

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
