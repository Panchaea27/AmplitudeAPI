import boto3
import os
from dotenv import load_dotenv

def list_s3_files(bucket_name, aws_access_key, aws_secret_key, s3_folder=""):
    """
    List all files in an S3 bucket folder.
    
    Args:
        bucket_name (str): S3 bucket name
        aws_access_key_id (str): AWS access key
        aws_secret_access_key (str): AWS secret key
        s3_folder (str): Folder path (e.g., "my-folder/")
    
    Returns:
        list: File names in the folder
    """

    s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key 
    )


    content = s3_client.list_objects_v2(
        Bucket = bucket_name,
        Prefix = s3_folder,
        Delimiter='/'
    )
    
    item_list = []

    for item in content.get('Contents',[]):
        if item['Key'] != s3_folder:
            item_list.append(item['Key'])

    return(item_list)



# load_dotenv()
# api_token = os.getenv("API_TOKEN")
# secret_key = os.getenv("SECRET_KEY")
# aws_access_key = os.getenv("Access_key_ID")
# aws_secret_key = os.getenv("Secret_access_key")
# aws_bucket_name = os.getenv("AWB_BUCKET_NAME")
# file_directory = 'data/unzipped'
# aws_folder = 'python-import/'

# print('u3wu')
# print(list_s3_files(aws_bucket_name, aws_access_key, aws_secret_key,'python-import/'))