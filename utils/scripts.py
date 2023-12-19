import os
import codecs
from typing import Any, Mapping

script_list = []


def add_script(filename: str, globals_: dict[str, Any], locals_: Mapping[str, Any]) -> None:
    global script_list

    if os.path.exists(filename):
        script_list.append(filename)
        exec(codecs.open(filename, encoding="utf-8").read(), globals_, locals_)


def get_scripts() -> list[str]:
    return script_list
