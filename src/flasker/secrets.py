from pathlib import Path
import json


def get_secrets(file: Path):
    data = file.read_text()
    secrets = json.loads(data)

    return secrets