
send_overview_to_slack_task = PythonOperator(
    task_id="send_overview_to_slack",
    python_callable=send_overview_to_slack,
    provide_context=True,
    dag=dag,
    # https://airflow.apache.org/concepts.html#trigger-rules
    trigger_rule='none_failed'
)
