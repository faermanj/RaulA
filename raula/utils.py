import json
import importlib
import logging
import pip
from pathlib import Path

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def pip_probe(dep):
    try:
        importlib.import_module(dep)
        logging.info("Dependency [{}] loaded".format(dep))
    except ModuleNotFoundError:
        logging.info("Installing [{}]".format(dep))
        install(dep)
        try:
            importlib.import_module(dep)
            logging.info("Dependency [{}] bounced".format(dep))
        except ModuleNotFoundError:
            logging.warning("Failed to load [{}]".format(dep))
def to_json(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def get_raula_home():
    user_home = Path.home()
    raula_home = user_home / ".raula"
    if (not raula_home.exists()):
        raula_home.mkdir(parents=True, exist_ok=True)
    return raula_home