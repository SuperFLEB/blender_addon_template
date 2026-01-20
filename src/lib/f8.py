"""
Functions for handling "f8" addon refresh in Blender, to reload file imports that may have changed.
"""

import importlib
import types
import sys
from . import addon as addon_lib, log as log_lib
from fleb.esq import ESQ

importlib.reload(addon_lib)
loaded_modules: set[types.ModuleType] = {addon_lib}

logger = addon_lib.logger()

flushed = False
nonce = id(object())

def reload(*mods: types.ModuleType) -> None:
    """
    Reloads imports that may have changed after an "f8" addon refresh in Blender.
    Modules will only be reloaded once per addon refresh.

    Example:
    ::
        from .lib import f8
        from .lib import some_module
        from .lib import some_other_module

        f8.reload(some_module, some_other_module)

    :note: Don't reload the "f8" module itself.

    :param mods: Modules to reload.
    """

    for mod in mods:
        if not flushed:
            logger.error(f"Loading {mod.__name__}) f8 is not re-initializing on reload! You should call f8.init() in your addon's __init__.py. Reloads probably aren't working.")
        if mod in loaded_modules: continue

        logger.debug(ESQ.green("f8♻  ") + mod.__name__)
        importlib.reload(mod)
        loaded_modules.add(mod)

def _post_init(nonce_was: float) -> None:
    if nonce_was == nonce:
        logger.error("f8 failed to reload!")
    else:
        logger.info(ESQ.green("✔  ") + "using reloaded f8 module")

    global flushed
    flushed = True
    loaded_modules.clear()

def init() -> None:
    global last_self_reload
    logger.info(ESQ.bright.cyan("⏳ ") + "Initialize and reload f8 module")
    nonce_was = nonce
    importlib.reload(sys.modules[__name__])._post_init(nonce_was)

loaded_modules.clear()
