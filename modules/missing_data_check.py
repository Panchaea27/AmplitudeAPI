
import list_s3_files as lists3files
import os
from dotenv import load_dotenv

def find_missing_amplitude_data(bucket_name, aws_access_key, aws_secret_key, s3_folder, start_date=None, end_date=None):
    """
    Check S3 bucket for missing Amplitude data files.

    Args:
        bucket_name (str): S3 bucket name
        aws_access_key_id (str): AWS access key
        aws_secret_access_key (str): AWS secret key
        s3_folder (str): S3 folder prefix
        start_date (date, optional): Start date. Defaults to 1 week before yesterday
        end_date (date, optional): End date. Defaults to yesterday

    Returns:
        list: List of tuples (start_date, end_date) for missing data ranges
    """

    object_list = lists3files.list_s3_files(bucket_name, aws_access_key, aws_secret_key, s3_folder)
    print(object_list)
    cleaned_list = []
    for item in object_list:
        if s3_folder in item:
            cleaned_list.append(item.replace(s3_folder,''))
            print(cleaned_list)
    


load_dotenv()
api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
aws_access_key = os.getenv("Access_key_ID")
aws_secret_key = os.getenv("Secret_access_key")
aws_bucket_name = os.getenv("AWB_BUCKET_NAME")
file_directory = 'data/unzipped'
aws_folder = 'python-import/'

find_missing_amplitude_data(aws_bucket_name,aws_access_key,aws_secret_key,'python-import/')