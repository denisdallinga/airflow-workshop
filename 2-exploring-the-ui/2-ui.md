# DAGS overview
DAGS are automatically discovered by the airflow webserver and added to the airflow DagBag. Airflow searches all python files for DAG's instantiated in folder set in airflow config.

```
cat airflow.cfg | grep dags_folder
```

# DAG UI
* Show ui of tutorial DAG
* Trigger a DAG manually
* Start the scheduler
* Show ui of the tutorial dag after it has ran

Disable example dags by setting `load_examples` to `False` in `airflow.cfg`
