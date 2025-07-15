import os
import zipfile
import gzip
import shutil
import tempfile


def unzip_json(zip_file,output_dir='data'):
    if not os.path.exists(zip_file):
        raise FileNotFoundError(f"File {zip_file} not found")

    os.makedirs(output_dir,exist_ok=True)

    with zipfile.ZipFile(zip_file, 'r') as file:
        for file_name in file.namelist():
            if file_name.endswith(".gz"):
            #for each .gz file, create a out_filename (the JSON equivalent) and its path
                with file.open(file_name) as gzs:
                    out_filename = file_name.split("/", 1)[-1].replace(".gz", "")
                    out_path = os.path.join(output_dir, out_filename)
                    #for each of the files
                    with gzip.open(gzs,'rb') as infile:
                        with open(out_path,'wb') as outfile:
                #copy the .gz and save as JSON
                            shutil.copyfileobj(infile, outfile)
                            print('success')



