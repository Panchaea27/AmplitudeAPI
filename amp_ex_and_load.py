from dotenv import load_dotenv
from datetime import datetime,timedelta
import time
import os
from modules.extract_from_api import extract_amplitude_data 
from modules.unzip_json import unzip_json
from modules.s3_upload import s3_upload
load_dotenv()


api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
aws_access_key = os.getenv("Access_key_ID")
aws_secret_key = os.getenv("Secret_access_key")
aws_bucket_name = os.getenv("AWB_BUCKET_NAME")
file_directory = 'data/unzipped'
aws_folder = 'python-import/'
yesterday = datetime.now() - timedelta(days=1)
today = datetime.now()
start_date = yesterday.strftime('%Y%m%dT00')
end_date = today.strftime('%Y%m%dT00')

extract_amplitude_data(start_date,end_date,api_token,secret_key)
unzip_json('data.zip')
s3_upload(aws_access_key,aws_secret_key,aws_bucket_name,file_directory,aws_folder)
