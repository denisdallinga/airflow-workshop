# Setup a custom intergration
https://xxx.slack.com/apps/manage/custom-integrations > incoming webhooks > create new intergration

# Add the HTTP connection to access Slack
{"webhook_token": "MYTOKN"}

Show that the webhook message is not templated
https://github.com/apache/airflow/blob/master/airflow/contrib/operators/slack_webhook_operator.py

Remember to update the http default connection
