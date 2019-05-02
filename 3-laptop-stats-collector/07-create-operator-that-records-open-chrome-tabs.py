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
