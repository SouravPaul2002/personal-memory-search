import json
import os

REGISTRY_FILE = "backend/indexing/file_registry.json"


def load_registry():

    if not os.path.exists(REGISTRY_FILE):
        return {}

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry):

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            registry,
            f,
            indent=4,
            ensure_ascii=False
        )