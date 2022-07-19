please put in your service account key data into api_key.json first of all then start the airflow server and then build the 
docker images
Lastly run the schedule_get_trends.py to schedule/trigger the task over an Airflow server

to install airflow run:
docker-compose up airflow-init
docker-compose up

to run the code in a docker image run:
docker build . -t get-trends
docker run get-trends

lastly to schedule the task run the following command:
python schedule_get_trends.py

the schedule_get_trends.py file has 2 dags, get_trends and load_data, get trends gets the data from google trends and uploads it to Cloud Storage
Load Data get the data from Cloud Storage and uploads it to BigQuery for querying using the GCloud operator
Dockerfile 