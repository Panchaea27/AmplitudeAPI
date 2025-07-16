
# import list_s3_files as lists3files
import os
# from dotenv import load_dotenv
import shutil


def cleanup_uploaded_files(local_folder,s3_files):
    loc_files = []
    try:
        for item in os.listdir(local_folder):
            item_path = os.path.join(local_folder, item)
            if os.path.isfile(item_path):
                loc_files.append(item)
    except FileNotFoundError:
        print(f"Path not found: {local_folder}")

    delete_list = []
    move_list = []
    check_list = []

    for loc_file in loc_files:
        for s3_file in s3_files:
            if loc_file not in check_list:
                if s3_file not in check_list:
                    if loc_file == s3_file:
                        delete_list.append(loc_file)
                        check_list.append(loc_file)
                    else:
                        move_list.append(loc_file)
                        check_list.append(loc_file)


    for item in delete_list:
        filepath = os.path.join(local_folder,item)
        # print(filepath)
        # print('end of matches')
        os.remove(filepath)

    failed_path = os.path.join(local_folder,'failed_uploads')
    os.makedirs(failed_path,exist_ok=True)
    for item in move_list:
        shutil.move(os.path.join(local_folder,item),failed_path)
    #     print(item)

    # print(delete_list)
    # print(move_list)



