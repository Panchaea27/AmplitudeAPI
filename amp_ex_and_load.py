from dotenv import load_dotenv
from datetime import datetime,timedelta
import time
import os
from modules.extract_from_api import extract_amplitude_data 
from modules.unzip_json import unzip_json
load_dotenv()


api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.strftime('%Y%m%dT00')
end_date = yesterday.strftime('%Y%m%dT00')

extract_amplitude_data(start_date,end_date,api_token,secret_key)
unzip_json('data.zip')
