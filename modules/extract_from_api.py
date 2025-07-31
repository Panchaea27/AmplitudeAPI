#modular version of the extraction script
#extraction from api

import os
import requests

def extract_amplitude_data(start_date,end_date,api_key,secret_key,output_file='data.zip'):
    """
    This function extracts data from Amplitude's Export API for a given date range and stores it in an output file data.zip (unless specified differently)
    
    Args:
    start_time (str): start date in format "YYYYMMDDTTHH" (e.g. '202412101020')
    end_time (str): end time in format "YYYYMMDDTTHH" (e.g. '202412101020')
    api_key (str): Amplitude API key
    secret_key (str): Amplitude secret key
    output_file (str): File name to be output, set by default as data.zip

    Output (bool):
    True - if extraction is successful
    False - if extraction failed

    """

    url = 'https://analytics.eu.amplitude.com/api/2/export'

    param = {
        'start': start_date,
        'end': end_date
    }
    try:
        response = requests.get(url, params=param, auth=(api_key,secret_key))
        if response.status_code == 200:
            data = response.content
            print("Extraction successful")
            with open(output_file, 'wb') as file:
                file.write(data)
                print(f"Data saved to {output_file}")
            return True
        else:
            print("API Call failed")
            print(response.status_code)
            return False
    except Exception as e:
        print(f"error: str({e})")
        return False

        