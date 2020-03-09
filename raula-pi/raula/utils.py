import json
import importlib
import logging
import pip
import os
from pathlib import Path

utils_logger = logging.getLogger('raula.utils')


def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def pip_probe(dep):
    try:
        importlib.import_module(dep)
        utils_logger.info("Dependency [{}] loaded".format(dep))
    except ModuleNotFoundError:
        utils_logger.info("Installing [{}]".format(dep))
        install(dep)
        try:
            importlib.import_module(dep)
            utils_logger.info("Dependency [{}] bounced".format(dep))
        except ModuleNotFoundError:
            utils_logger.warning("Failed to load [{}]".format(dep))


def to_json(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def dump_env():
    utils_logger.debug("# Environment Dumping")
    for env in os.environ:
        val = os.environ.get(env)
        utils_logger.debug("{}={}".format(env, val))
    utils_logger.debug("# Environment Dumped")

def get_raula_home():
    raula_home = None

    boot_dir = Path("/boot")
    if(boot_dir.exists()):
        raula_home = boot_dir

    if(not raula_home):
        user_home = Path.home()
        raula_home = user_home / ".raula"
        if not raula_home.exists():   
            utils_logger.info("Creating raula directory at [{}]".format(str(raula_home)))
            raula_home.mkdir(parents=True, exist_ok=True)

    if(not raula_home):
        tmp_path = os.environ.get("TMPDIR")
        if(tmp_path):
            tmp_path = Path(tmp_path)
            if(tmp_path.exists()):
                raula_home = tmp_path

    utils_logger.info("Starting raula at [{}]".format(str(raula_home)))
    return raula_home
