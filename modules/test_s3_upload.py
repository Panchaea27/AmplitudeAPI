import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("Access_key_ID")
aws_secret_key = os.getenv("Secret_access_key")
aws_bucket_name = os.getenv("AWB_BUCKET_NAME")

s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key 
)

local_file_loc = "data/test_file.json"
aws_file_dest = "python-import/test_file.json"

s3_client.upload_file(local_file_loc,aws_bucket_name,aws_file_dest)

print("File uploaded")
