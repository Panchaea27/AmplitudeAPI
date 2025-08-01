import boto3
import os

def s3_upload(aws_access_key, aws_secret_key, aws_bucket_name, file_directory, aws_folder):
    # Initialize S3 client with provided AWS credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    # List all files in the local directory to upload
    upload_files = os.listdir(file_directory)

    # Iterate over each file in the directory
    for file in upload_files:
        # Only process files with .json extension
        if file.endswith('.json'):
            upload_file_path = os.path.join(file_directory, file)  # Local file path
            aws_upload_path = os.path.join(aws_folder, file)  # Destination path in S3 bucket

            print(upload_file_path)
            print(aws_upload_path)

            # Upload the file to the specified S3 bucket and folder
            s3_client.upload_file(upload_file_path, aws_bucket_name, aws_upload_path)
            print('success')

            # Delete the local file after successful upload
            os.remove(upload_file_path)
            print('file deleted')
            
