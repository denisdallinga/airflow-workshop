# Laptop stats collector
We want to build an application that every minute get's some stats of my local machine, and stores these stats in some files. Then each hour, the stats are aggregated and an overview message is posted to slack.

We want to collect the following metrics:
- How many chrome tabs are open?
- What is the load on my laptop?

For this we are going to build two DAG's. One collector DAG that will run every minute. It will collect the metrics and write them to disk. The other collector dag will aggregate the metrics, save them to disk and send a summary to slack.
