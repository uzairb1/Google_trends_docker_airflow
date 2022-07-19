from pytrends.request import TrendReq # type: ignore
import datetime
import gcloud# type: ignore
import os
from gcloud import storage# type: ignore


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "api_key.json"
client = storage.Client()
def create_bucket(bucket_name):
    print(bucket_name)
    check_bucket = client.bucket(bucket_name)
    if not check_bucket.exists():
        bucket = client.create_bucket(bucket_name)
        msg = f"Bucket with name {bucket.name} has been created"
        print(msg)
    else:
        print("bucket already exists")

def get_trends(kw):
    pytrend = TrendReq()
    
    #uncomment the following line to get daily data, since the granurality is higher,
    #this loop should be parallelized by dynamically creating DAGs in Airflow, one DAG for
    #each keyword in the keyword.txt file
    #df = dailydata.get_daily_data(kw, three_yrs_ago.year, three_yrs_ago.month, datetime.datetime.now().year, datetime.datetime.now().month, geo='')
    pytrend.build_payload(kw_list=[kw],timeframe = '2019-07-18 2022-7-18')
    df = pytrend.interest_over_time()
    return df

def upload_to_GCS(bucket_name, df, kw):
    
        bucket = client.get_bucket(bucket_name)
        bucket.blob(bucket_name+'/'+kw+'.csv').upload_from_string(df.to_csv(), 'text/csv')
        #df.to_csv('gs://'+bucket_name)
        #print(df)
        print("data uploaded to bucket {} as {}.csv".format(bucket_name,kw))

def run():
    kw_list=[]
    bucket="keys_data_786_123"
    create_bucket(bucket)
    with open('keywords.txt', 'r') as f:
        kw_list = [line.strip() for line in f]
    for kw in kw_list:
        df= get_trends(kw)
        upload_to_GCS(bucket,df,kw)
run()