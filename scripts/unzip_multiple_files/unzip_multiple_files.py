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

def recursively_send_files_to_root(current_abs_path, destination_abs_path):
    pass # TODO: Not implemented yet

def send_files_to_root(abs_path):
    return recursively_send_files_to_root(abs_path, abs_path)

def remove_empty_directories(current_abs_path):
    pass # TODO: Not implemented yet

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
                file_name.replace(".zip", "/"))) # TODO: Handle filename conflicts
    # 3 - Loop inside inner folders and send files to
    # the root of the output folder:
    send_files_to_root(ABS_PATH_OUTPUT_FOLDER)
    # 4 - Remove empty inner directories:
    remove_empty_directories(ABS_PATH_OUTPUT_FOLDER)
    logging.debug("Execution ends!")

if __name__ == "__main__":
    main()
