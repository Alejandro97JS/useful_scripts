import json, os

# Load configuration params:
CONFIG = {}
with open("../../config.json", mode="r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file).get("change_file_names", {})

# Path to the folder with the files whose name are going to change:
ABS_PATH_TO_FOLDER = CONFIG.get("abs_path_to_folder")
# Condition method to apply (idle condition method as default):
FILE_NAME_CONDITION_METHOD = CONFIG.get("file_name_condition", "idle")
# Action method to apply (idle action method as default):
FILE_NAME_ACTION_METHOD = CONFIG.get("file_name_action", "idle")

# Default methods:

def idle_condition(filename:str)->bool:
    # Never apply:
    return False
    
def idle_action(filename:str)->str:
    # No change:
    return filename

# Custom defined condition methods:

def has_digits_condition(filename:str)->bool:
    return any(char.isdigit() for char in filename)

# Custom defined action methods:

def no_digits_and_lowercase_action(filename:str)->str:
    return "".join([c.lower() for c in filename if not c.isdigit()])

# Mapper for the defined condition methods:
CONDITION_METHODS = {
    "idle": idle_condition,
    "has_digits": has_digits_condition
}

# Mapper for the defined action methods:
ACTION_METHODS = {
    "idle": idle_action,
    "no_digits_and_lowercase": no_digits_and_lowercase_action
}

def main():
    dirname = os.path.dirname(ABS_PATH_TO_FOLDER)
    elems_in_path = os.listdir(dirname)
    files_in_path = [f for f in elems_in_path if os.path.isfile(
        os.path.join(dirname, f))]
    for file in files_in_path:
        if FILE_NAME_CONDITION_METHOD(file):
            new_filename = FILE_NAME_ACTION_METHOD(file)
            os.rename(
                os.path.join(dirname, file),
                os.path.join(dirname, new_filename)
            )

if __name__ == "__main__":
    main()
