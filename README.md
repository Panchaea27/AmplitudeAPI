# Amplitude Data Extraction and S3 Upload Pipeline

## Overview

This project provides an automated pipeline to extract event data from Amplitude's Export API, decompress the downloaded archive, and upload the resulting JSON files to an AWS S3 bucket.

It is designed to run daily, retrieving data for the previous day (from midnight to midnight), enabling seamless data ingestion for further processing or analysis.

The pipeline consists of modular Python scripts:

- Extract data via Amplitude API
- Unzip and decompress downloaded archives
- Upload decompressed JSON files to AWS S3
- (Additional utility scripts included for reference)

---

## Features

- **Automated daily extraction:** Extracts the previous day’s data based on system date/time.
- **Archive handling:** Downloads zipped export data, then extracts `.gz` JSON files.
- **AWS S3 integration:** Uploads uncompressed JSON files to a designated S3 bucket folder.
- **Local cleanup:** Deletes files after successful upload to maintain a clean working directory.
- **Modular design:** Each core step encapsulated in its own Python module for clarity and reusability.

---

## Getting Started

### Prerequisites

- Python environment (no specific version required)
- Network access to Amplitude API and AWS S3 services
- AWS credentials with permissions to upload objects to the target S3 bucket
- Amplitude API key and secret key

### Environment Variables

Create a `.env` file in the root directory of the project containing the following keys:

```env
API_TOKEN=<your_amplitude_api_key>
SECRET_KEY=<your_amplitude_secret_key>
Access_key_ID=<your_aws_access_key>
Secret_access_key=<your_aws_secret_key>
AWB_BUCKET_NAME=<your_s3_bucket_name>
```

### Repository Structure

```env
├── main.py                    # Main orchestration script
├── modules/
│   ├── extract_from_api.py    # Handles API extraction logic
│   ├── unzip_json.py          # Extracts and decompresses downloaded files
│   └── s3_upload.py           # Uploads files to AWS S3 and deletes locally
├── cleanup_files.py           # Utility script to clean up local files (not used by main.py)
├── list_s3_files.py           # Utility script for listing S3 bucket files (not used by main.py)
└── .env                      # Environment variables (not included in repo)
```

### How It Works

**Date Range Calculation:**
The main script calculates the extraction window as the previous day, starting at midnight (00:00) and ending at midnight today. Dates are formatted as YYYYMMDDT00 per Amplitude API requirements.

**Data Extraction:**
The extract_amplitude_data function performs an authenticated GET request to Amplitude’s Export API, downloading event data within the specified date range. The response is saved as data.zip.

**File Decompression:**
The unzip_json module opens data.zip, identifies .gz compressed JSON files within, decompresses them, and saves the resulting JSON files into the data/unzipped directory.

**Upload to AWS S3:**
The s3_upload function uploads each JSON file in data/unzipped to the specified folder inside the configured S3 bucket. After successful upload, the local JSON file is deleted to avoid storage buildup.

### Additional Scripts

**cleanup_files.py:**
Contains utility functions to compare local files against those successfully uploaded to S3, deleting matches and moving unmatched files to a failed_uploads folder. This script is not invoked by the main script but included for reference.

**list_s3_files.py:**
A helper script for listing files currently stored in the S3 bucket. Also not invoked by the main pipeline.

## Example: Orchestrating the Ingestion Pipeline with Kestra

Relating to the YAML **kestra_upload_to_s3**

The `amplitude_bison` flow provided in the `amplitude_api_meow` namespace is a Kestra orchestration example that automates the ingestion and transformation of Amplitude data using the `amp_ex_and_load.py` script.

This YAML defines a simple end-to-end process:

- Cloning the source code from a GitHub repository  
- Installing dependencies in a Dockerized Python environment  
- Executing the main ingestion script  
- Retrying gracefully on failure  
- Triggering on a schedule (hourly)

**Note:** Secret values such as API keys, AWS credentials, and tokens are injected using Kestra’s `kv()` function for simplicity. This is a placeholder method appropriate for free/self-hosted Kestra setups only. Do not use `kv()` for sensitive data in production — instead, integrate with a secure secret manager (e.g., AWS Secrets Manager, HashiCorp Vault, etc.).

This flow is useful as a lightweight, portable orchestration layer and can be extended to include:

- Conditional logic  
- Notifications  
- Parallel tasks  
- Data validation steps

You can adapt the `cron` schedule, the Docker image, and the script behavior to match your specific deployment environment.
