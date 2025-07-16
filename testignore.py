from modules.cleanup_files import cleanup_uploaded_files
from modules.list_s3_files import list_s3_files
from dotenv import load_dotenv
import os


local_folder = 'data/unzipped'
load_dotenv()
api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
aws_access_key = os.getenv("Access_key_ID")
aws_secret_key = os.getenv("Secret_access_key")
bucket_name = os.getenv("AWB_BUCKET_NAME")
file_directory = 'data/unzipped'
aws_folder = 'python-import/'

s3_files = list_s3_files(bucket_name, aws_access_key, aws_secret_key, s3_folder="")

cleanup_uploaded_files(local_folder,s3_files)