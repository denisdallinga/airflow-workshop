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

send_overview_to_slack_task = PythonOperator(
    task_id="send_overview_to_slack",
    python_callable=send_overview_to_slack,
    provide_context=True,
    dag=dag,
    op_kwargs={'metric_types': METRIC_TYPES}
)
