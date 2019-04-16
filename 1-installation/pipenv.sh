# ensure pipenv is installed
brew install pipenv
# OR
pip install --user pipenv

pipenv --version

# Create a new working directory
mkdir ~/projects/airflow-demo
# And let's set this directory as the airflow home:
export AIRFLOW_HOME=~/projects/airflow-demo

# Install latest version of apache-airflow
cd ~/projects/airflow-demo
pipenv install apache-airflow

# And initialize the database
pipenv run airflow initdb
