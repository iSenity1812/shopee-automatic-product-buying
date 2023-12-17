import logging
import datetime
import os

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
LOG_FILENAME = datetime.datetime.now().strftime('.\logs\log_%Y-%m-%d_%H-%M-%S.log')
logging.basicConfig(filename = LOG_FILENAME,
                        filemode = "w",
                        format = Log_Format, 
                        level = logging.INFO)


logger = logging.getLogger()


# Clear log

def delete_all_log_files(directory_path):
    try:
        # Iterate through files in the specified directory
        for file_name in os.listdir(directory_path):
            # Check if the file is a log file (you can adjust the condition as needed)
            if file_name.endswith(".log"):
                file_path = os.path.join(directory_path, file_name)
                os.remove(file_path)
                print(f"Log file '{file_path}' deleted successfully.")
        print("All log files deleted successfully.")
    except Exception as e:
        print(f"Error deleting log files: {e}")

# Example usage:
# delete_all_log_files(directory_path)


# logger.info("Con me may")