import os
import zipfile
import gzip
import shutil

def unzip_json(zip_file, output_dir='data/unzipped'):
    # Check if the specified zip file exists; raise error if not
    if not os.path.exists(zip_file):
        raise FileNotFoundError(f"File {zip_file} not found")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the zip archive for reading
    with zipfile.ZipFile(zip_file, 'r') as file:
        # Iterate over each file in the zip archive
        for file_name in file.namelist():
            # Process only files ending with .gz (compressed JSON files)
            if file_name.endswith(".gz"):
                # Open the .gz file inside the zip
                with file.open(file_name) as gzs:
                    # Determine output filename by removing folders and .gz extension
                    out_filename = file_name.split("/", 1)[-1].replace(".gz", "")
                    out_path = os.path.join(output_dir, out_filename)

                    # Decompress the .gz file and write its contents as JSON to output path
                    with gzip.open(gzs, 'rb') as infile:
                        with open(out_path, 'wb') as outfile:
                            shutil.copyfileobj(infile, outfile)
                            print('success')


