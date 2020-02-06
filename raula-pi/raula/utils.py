import json
import importlib
import logging
import pip
import os
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

def dump_env():
    logging.debug("# Environment Dumping")
    for env in os.environ:
        val = os.environ.get(env)
        logging.debug("{}={}".format(env, val))
    logging.debug("# Environment Dumped")

def get_raula_home():
    raula_home = None
    tmp_path = os.environ.get("TMPDIR")
    if(tmp_path):
        tmp_path = Path(tmp_path)
        if(tmp_path.exists()):
            raula_home = tmp_path

    if(not raula_home):
        user_home = Path.home()
        raula_home = user_home / ".raula"

    logging.info("Starting raula home at [{}]".format(str(raula_home)))
    if (not raula_home.exists()):
        raula_home.mkdir(parents=True, exist_ok=True)
    return raula_home
