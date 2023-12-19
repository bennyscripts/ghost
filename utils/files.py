import os
import sys

from . import config

def resource_path(relative_path):
    if config.PRODUCTION:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    else:
        return relative_path

def create_defaults():
    if not os.path.exists("scripts/"):
        os.mkdir("scripts/")