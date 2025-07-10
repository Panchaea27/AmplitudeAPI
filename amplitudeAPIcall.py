# Data Extraction using Amplitude's Export API
# https://amplitude.com/docs/apis/analytics/export

#Load required libraries
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime,timedelta
import time
import zipfile
import gzip
import shutil


yesterday = datetime.now()-timedelta(days=1)

starttime = yesterday.strftime("%Y%m%dT00")
endtime = yesterday.strftime("%Y%m%dT23")

amplitudeurl = 'https://analytics.eu.amplitude.com/api/2/export'

parameters= {
      'start': starttime,
      'end': endtime
}

load_dotenv()
api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
auth_string = api_token,secret_key

current_try = 0
max_tries = 3
waittime = 5

while current_try < max_tries:
    try:
        response = requests.get(amplitudeurl,params=parameters,auth = auth_string)
        statuscode = response.status_code
        if statuscode != 200:
            raise Exception(f"Error! API status code {statuscode}")
        print(f"API Status Code: {response}")
        data = response.content
        filename = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        filepath = f"data/{filename}.zip"
        with open(filepath,'wb') as file:
            file.write(data)
        print(f"Extraction successful. File saved as {filename}")
        break
    except Exception as e:
        print(e)
        current_try +=1
    print(f'waiting.... trying again! Attempts left: {max_tries-current_try}')
    time.sleep(waittime)
if current_try == max_tries:
    print('Max attempt number reached. Exiting.')


print("Extracting data")

target_dir = f'data/from_{starttime}_till_{endtime}'

print(f"data will be extracted to {target_dir}")

os.makedirs(target_dir, exist_ok=True)

with zipfile.ZipFile(filepath, 'r') as file:
    for file_name in file.namelist(): #lists all the files (lowes granularity)
        print(f"File Name: {file_name}")
        if file_name.endswith(".gz"):
            with file.open(file_name) as gzs:
                out_filename = file_name.split("/", 1)[-1].replace(".gz", "")
                print(f"Out_FIlename: {out_filename}")
                out_path = os.path.join(target_dir, out_filename)
                print(f"outpath: {out_path}")
                with gzip.open(gzs,'rb') as infile:
                    with open(out_path,'wb') as outfile:
                        shutil.copyfileobj(infile, outfile)


print("Extraction complete")
