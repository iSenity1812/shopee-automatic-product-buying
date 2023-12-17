import os

def create_folder():
    # Get cur directory
    cur_dir = os.getcwd()

    # Join the cur dir with new folder
    new_folder_path = os.path.join(cur_dir, "logs")
    return os.makedirs(new_folder_path)

create_folder()