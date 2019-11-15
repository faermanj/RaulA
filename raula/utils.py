import json
from pathlib import Path


def to_json(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def get_raula_home():
    user_home = Path.home()
    raula_home = user_home / ".raula"
    if (not raula_home.exists()):
        raula_home.mkdir(parents=True, exist_ok=True)
    return raula_home