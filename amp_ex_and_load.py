from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from modules.extract_from_api import extract_amplitude_data
from modules.unzip_json import unzip_json
from modules.s3_upload import s3_upload

load_dotenv()  # Load environment variables from .env file

# Fetch API and AWS credentials from environment variables
api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
aws_access_key = os.getenv("Access_key_ID")
aws_secret_key = os.getenv("Secret_access_key")
aws_bucket_name = os.getenv("AWB_BUCKET_NAME")

file_directory = 'data/unzipped'  # Local folder for extracted files
aws_folder = 'python-import/'  # Target folder in S3 bucket

# Define extraction date range: from yesterday 00:00 to today 00:00
yesterday = datetime.now() - timedelta(days=1)
today = datetime.now()
start_date = yesterday.strftime('%Y%m%dT00')
end_date = today.strftime('%Y%m%dT00')

# Extract data from Amplitude API for the specified date range
extract_amplitude_data(start_date, end_date, api_token, secret_key)

# Unzip the downloaded data archive
unzip_json('data.zip')

# Upload the unzipped files to the AWS S3 bucket
s3_upload(aws_access_key, aws_secret_key, aws_bucket_name, file_directory, aws_folder)

