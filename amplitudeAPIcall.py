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
runtime = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

log_dir = 'data/log'

os.makedirs(log_dir, exist_ok=True)
logname = f'{log_dir}/AmplitudeAPI_log_{runtime}.txt'

with open(logname,'w') as file:
    file.write(f"Amplitude API LOG. Script Start Time: {runtime}\n")
    file.write(f"Extraction of data for the selected period: {starttime} - {endtime}\n")
    file.write("----------------------------\n")


while current_try < max_tries:
    with open(logname,'a') as file:
        file.write(f"Extraction attempt number: {current_try}\n")
    waittime = 5
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
        endruntime = datetime.now()
        with open(logname,'a') as file:
            file.write("Extraction from the API successful\n")
            file.write(f"Extraction completed at {endruntime}\n")
        break
    except Exception as e:
        with open(logname,'a') as file:
            file.write("Attempt failed\n")
            file.write(f"{str(e)}\n")
            file.write("\n")
        print(e)
        current_try +=1
    print(f'waiting {waittime} seconds & trying again! Attempts left: {max_tries-current_try}')
    while waittime > 0:
        print(f"{waittime} seconds left")
        time.sleep(1)
        waittime -=1
if current_try == max_tries:
    print('Max attempt number reached. Exiting.')
    with open(logname,'a') as file:
        file.write("\n")
        file.write("Max attempt number reached. API extraction has failed :(")
    raise Exception(f"Couldn't connect to the API - Status Code: {statuscode}")


print("Extracting data")

target_dir = f'data/from_{starttime}_till_{endtime}_{runtime}'

with open(logname,'a') as file:
    file.write("\n")
    file.write(f"Attempting to extract the files to JSON format. Destination directory: {target_dir}")
    file.write("List of files taken from the API: ")

print(f"data will be extracted to {target_dir}")

os.makedirs(target_dir, exist_ok=True)

with zipfile.ZipFile(filepath, 'r') as file:
    for file_name in file.namelist(): #lists all the files (lowes granularity)
        # print(f"File Name: {file_name}")
        with open(logname,'a') as log_file:
            log_file.write(f"{file_name}\n")
        if file_name.endswith(".gz"):
            with file.open(file_name) as gzs:
                out_filename = file_name.split("/", 1)[-1].replace(".gz", "")
                # print(f"Out_FIlename: {out_filename}")
                out_path = os.path.join(target_dir, out_filename)
                # print(f"outpath: {out_path}")
                with gzip.open(gzs,'rb') as infile:
                    with open(out_path,'wb') as outfile:
                        shutil.copyfileobj(infile, outfile)
                        with open(logname,'a') as log_file:
                            log_file.write(f"Replacement file created: {out_path}\n")




print("Extraction complete")

os.remove(filepath)
print("original zip file deleted")

with open(logname,'a') as file:
    file.write("\n")
    file.write(f"Extracting ZIP files to JSONs completed.\n")
    file.write(f"Original ZIP file deleted.")
    # file.write(f"Ex{datetime.now()}")