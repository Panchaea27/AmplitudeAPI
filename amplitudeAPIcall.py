#THIS IS A LEGACY VERSION OF THE AMP_EX_AND_LOAD. IT'S NOT MODULARISED AND IT'S HERE FOR REFERENCE PURPOSES ONLY.



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

# Establishing dateframe for the API pull. (i.e. most recent full day)
yesterday = datetime.now()-timedelta(days=1)

starttime = yesterday.strftime("%Y%m%dT00")
endtime = yesterday.strftime("%Y%m%dT23")


# EU API URL
amplitudeurl = 'https://analytics.eu.amplitude.com/api/2/export'

#parameters for the start-end date of data pull
parameters= {
      'start': starttime,
      'end': endtime
}

#loading API Tokens/Keys to be used to aqccess Amplitude data
load_dotenv()
api_token = os.getenv("API_TOKEN")
secret_key = os.getenv("SECRET_KEY")
auth_string = api_token,secret_key

#Try count. Will be used for while loops which retry the pull if it fails
current_try = 0
max_tries = 3

#returns the script start time
runtime = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

#directory of the log 
log_dir = 'data/log'

#ensured log_dir exists
os.makedirs(log_dir, exist_ok=True)
#name of the log file. Each run of the script creates a new text file
logname = f'{log_dir}/AmplitudeAPI_log_{runtime}.txt'

#Header for the log file. 
with open(logname,'w') as file:
    file.write(f"Amplitude API LOG. Script Start Time: {runtime}\n")
    file.write(f"Extraction of data for the selected period: {starttime} - {endtime}\n")
    file.write("----------------------------\n")

#Main while loop attempting the API pull
while current_try < max_tries:

    #starts the attempt by logging the attempt number
    with open(logname,'a') as file:
        file.write(f"Extraction attempt number: {current_try}\n")
    #waittime is used to space out the API call attempts
    waittime = 5

    #try block for API pull
    try:
        response = requests.get(amplitudeurl,params=parameters,auth = auth_string)
        statuscode = response.status_code
    # if statement will raise an Error if the API status Code is not 200. This will enable another attempt in the while loop 
        if statuscode != 200:
            raise Exception(f"Error! API status code {statuscode}")
        print(f"API Status Code: {response}")
    #record API data in a variable
        data = response.content
    #establishes the zip file name and path (this file will be deleted after the JSON conversion)
        filename = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        filepath = f"data/{filename}.zip"
    #creates and saves the file in the filepath. This creates the zip file
        with open(filepath,'wb') as file:
            file.write(data)
        print(f"Extraction successful. File saved as {filename}")
    #var stores the end of extraction time. used for logging
        endruntime = datetime.now()
    #logs successful extraction and the time it was completed
        with open(logname,'a') as file:
            file.write("Extraction from the API successful\n")
            file.write(f"Extraction completed at {endruntime}\n")
    #if the extraction was successful the while loop breaks
        break
    #if Exception is raised, it will be logged in the log file. Then the current_try counter will go up
    except Exception as e:
        with open(logname,'a') as file:
            file.write("Attempt failed\n")
            file.write(f"{str(e)}\n")
            file.write("\n")
        print(e)
        current_try +=1
    #The terminal will inform of the re-attempt and count down to the next attempt    
    print(f'waiting {waittime} seconds & trying again! Attempts left: {max_tries-current_try}')
    while waittime > 0:
        print(f"{waittime} seconds left")
        time.sleep(1)
        waittime -=1
#if the current_try reaches the max_try, the loop ends and an Exception error is raised. Logged in the log.
if current_try == max_tries:
    print('Max attempt number reached. Exiting.')
    with open(logname,'a') as file:
        file.write("\n")
        file.write("Max attempt number reached. API extraction has failed :(")
    raise Exception(f"Couldn't connect to the API - Status Code: {statuscode}")

#Now the script will attempt to convert the zip into JSON files (unless API call failed)

print("Converting data to JSON")

#defining target directory folder for the unzipped JSONs
target_dir = f'data/from_{starttime}_till_{endtime}_{runtime}'

#logging the attempt to convert the files
with open(logname,'a') as file:
    file.write("\n")
    file.write(f"Attempting to convert the files to JSON format. Destination directory: {target_dir}\n")
    file.write("List of files taken from the API & their new corresponding file paths: \n")

print(f"data will be extracted to {target_dir}")

#check if destination folder exists
os.makedirs(target_dir, exist_ok=True)

#Open the zip file
with zipfile.ZipFile(filepath, 'r') as file:
    for file_name in file.namelist(): #lists all the files (lowes granularity)

        #log each original file name
        with open(logname,'a') as log_file:
            log_file.write(f"{file_name}\n")
        #check if file name is a .gz
        if file_name.endswith(".gz"):
            #for each .gz file, create a out_filename (the JSON equivalent) and its path
            with file.open(file_name) as gzs:
                out_filename = file_name.split("/", 1)[-1].replace(".gz", "")
                out_path = os.path.join(target_dir, out_filename)
                #for each of the files
                with gzip.open(gzs,'rb') as infile:
                    with open(out_path,'wb') as outfile:
                #copy the .gz and save as JSON
                        shutil.copyfileobj(infile, outfile)
                        #log each replacement file name in the log
                        with open(logname,'a') as log_file:
                            log_file.write(f"Replacement file created: {out_path}\n")




print("Extraction complete")

#delete the ZIP file
os.remove(filepath)
print("original zip file deleted")

#log the final part
with open(logname,'a') as file:
    file.write("\n")
    file.write(f"Extracting ZIP files to JSONs completed.\n")
    file.write(f"Original ZIP file deleted.")