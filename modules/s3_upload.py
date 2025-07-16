import boto3
import os
from dotenv import load_dotenv


def s3_upload(aws_access_key,aws_secret_key,aws_bucket_name,file_directory,aws_folder):



    s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key 
    )


    upload_files = os.listdir(file_directory)

    for file in upload_files:
        if file.endswith('.json'):
            upload_file_path = os.path.join(file_directory,file)
            print(upload_file_path)
            aws_upload_path = os.path.join(aws_folder,file)
            print(aws_upload_path)
            s3_client.upload_file(upload_file_path,aws_bucket_name,aws_upload_path)
            print('success')
            # os.remove(upload_file_path)
            # print('file deleted')
    

    

            
