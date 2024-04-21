import json, os, logging, zipfile

logging.getLogger().setLevel(logging.DEBUG)

# Load configuration params:
CONFIG = {}
with open("../../config.json", mode="r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file).get("unzip_multiple_files", {})

# Path to the folder with the input zip files:
ABS_PATH_INPUT_FOLDER = CONFIG.get("abs_path_input_folder")
# Path to the output folder with the input zip files:
ABS_PATH_OUTPUT_FOLDER = CONFIG.get("abs_path_output_folder")

FILENAME_MAX_RETRIES = 5

def append_retry(filename:str, retry_num:int)->str:
    filename_split = filename.split(".")
    extension = filename_split[-1]
    base_filename = "".join(filename_split[:-1])
    return base_filename + "_" + str(retry_num) + "." + extension

def recursively_send_files_to_root(current_abs_path:str, destination_abs_path:str)->None:
    dirname = os.path.dirname(current_abs_path)
    elems_in_path = os.listdir(dirname)
    files_in_path = [f for f in elems_in_path if os.path.isfile(
        os.path.join(dirname, f))]
    directories_in_path = [d for d in elems_in_path if os.path.isdir(
        os.path.join(dirname, d))]
    for file in files_in_path:
        retry = 1
        ok = False
        while not ok and retry < FILENAME_MAX_RETRIES:
            try:
                os.rename(
                    os.path.join(dirname, file),
                    os.path.join(destination_abs_path, file if retry == 1
                                 else append_retry(file, retry))
                )
                ok = True
            except Exception as e:
                logging.warning(f"Exception moving file: {e}\n" + 
                        f"Trying again ({retry+1}/{FILENAME_MAX_RETRIES})...")
                retry += 1
        if not ok and retry == FILENAME_MAX_RETRIES:
            logging.warning(f"Could not move file {os.path.join(dirname, file)}")
    # Recursively send files in the inner directories to the destination path:
    for d in directories_in_path:
        recursively_send_files_to_root(
            os.path.join(current_abs_path, d+"/"), # Move to inner directory
            destination_abs_path # Destination folder does not change.
        )

def send_files_to_root(abs_path:str)->None:
    return recursively_send_files_to_root(abs_path, abs_path)

def remove_empty_directories(current_abs_path:str)->None:
    # Recursively go to inner folders:
    dirname = os.path.dirname(current_abs_path)
    elems_in_path = os.listdir(dirname)
    directories_in_path = [d for d in elems_in_path if os.path.isdir(
        os.path.join(dirname, d))]
    for d in directories_in_path:
        remove_empty_directories(os.path.join(
            current_abs_path, d+"/")) # Clean inner directory
    current_elems_in_path = os.listdir(dirname)
    if len(current_elems_in_path) == 0:
        os.rmdir(dirname)

def main():
    logging.debug("Execution has started...")
    input_dirname = os.path.dirname(ABS_PATH_INPUT_FOLDER)
    logging.debug(f"Folder to modify is {input_dirname}")
    # 1 - Create output directory if it does not exist:
    if not os.path.isdir(ABS_PATH_OUTPUT_FOLDER):
        os.makedirs(ABS_PATH_OUTPUT_FOLDER)
    # 2 - Extract zip files to output directory:
    zip_files = [f
        for f in os.listdir(input_dirname)
        if os.path.isfile(os.path.join(input_dirname, f)) and f.endswith(".zip")]
    for file_name in zip_files:
        file_full_path = os.path.join(input_dirname, file_name)
        with zipfile.ZipFile(file_full_path, mode="r") as f:
            f.extractall(os.path.join(ABS_PATH_OUTPUT_FOLDER,
                file_name.replace(".zip", "/")))
    # 3 - Loop inside inner folders and send files to
    # the root of the output folder:
    send_files_to_root(ABS_PATH_OUTPUT_FOLDER)
    # 4 - Remove empty inner directories:
    remove_empty_directories(ABS_PATH_OUTPUT_FOLDER)
    logging.debug("Execution ends!")

if __name__ == "__main__":
    main()
