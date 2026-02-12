# utilities/data_paths.py
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

TEST_DATA_PATH = os.path.join(
    ROOT_DIR,
    "testData",
    "login_ddt_data.xlsx"
)
