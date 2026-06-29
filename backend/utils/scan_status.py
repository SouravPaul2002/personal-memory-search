# backend/utils/scan_status.py

import json

SCAN_STATUS_FILE = (
    "backend/data/scan_status.json"
)

def load_scan_status():

    with open(
        SCAN_STATUS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def save_scan_status(data):

    with open(
        SCAN_STATUS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )