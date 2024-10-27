import json
import os

from . import console

VERSION = "3.1.0"
PRODUCTION = True
DEFAULT_CONFIG = {
    "token": "",
    "prefix": "",
    "rich_presence": True,
    "message_settings": {
        "auto_delete_delay": 15,
        "style": "image"
    },
    "theme": "ghost",
    "snipers": {
        "nitro": {
            "enabled": True,
            "ignore_invalid": False
        }
    },
    "apis": {
        "serpapi": ""
    }
}
DEFAULT_THEME = {
    "title": "Ghost",
    "emoji": "\ud83d\udc99",
    "image": "https://raw.githubusercontent.com/bennyscripts/ghost/refs/heads/main/ghost.png",
    "colour": "#3A7CFE",
    "footer": "ghost.cool",
    "style": "image"
}

class Config:
    def __init__(self) -> None:
        self.config = {}
        self.config_without_theme_dict = {}
        self.theme = {}
            
        if os.path.exists("config.json"):
            self.config = json.load(open("config.json"))
            self.config_without_theme_dict = json.load(open("config.json"))

            if isinstance(self.config["theme"], str):
                self.theme = self.get_theme_file(self.config["theme"])
                self.config["theme_name"] = self.config["theme"]
                self.config["theme"] = self.theme
    
    def check(self):
        if not os.path.exists("backups/"):
            os.mkdir("backups/")
        if not os.path.exists("scripts/"):
            os.mkdir("scripts/")
        if not os.path.exists("data/"):
            os.mkdir("data/")
        if not os.path.exists("data/sniped_codes.txt"):
            open("data/sniped_codes.txt", "w").close()
            
        if not os.path.exists("config.json"):
            json.dump(DEFAULT_CONFIG, open("config.json", "w"), indent=4)
            console.print_info("Created config file")
        if not os.path.exists("themes/"):
            os.makedirs("themes/")
        if not os.path.exists("themes/ghost.json"):
            json.dump(DEFAULT_THEME, open("themes/ghost.json", "w"), indent=4)
            console.print_info("Created theme file")   

        if os.path.exists("config.json"):
            self.config = json.load(open("config.json"))

            for key in DEFAULT_CONFIG:
                if key == "theme":
                    if isinstance(self.config[key], dict):
                        self.config[key] = "ghost"

                if key == "snipers":
                    for sniper in DEFAULT_CONFIG[key]:
                        if sniper not in self.config[key]:
                            self.config[key][sniper] = DEFAULT_CONFIG[key][sniper]

                        if isinstance(self.config[key][sniper], bool):
                            sniper_enabled = self.config[key][sniper]
                            self.config[key][sniper] = DEFAULT_CONFIG[key][sniper]
                            self.config[key][sniper]["enabled"] = sniper_enabled
                        
                        self.config[key][sniper] = {**DEFAULT_CONFIG[key][sniper], **self.config[key][sniper]}

                if key not in self.config:
                    self.config[key] = DEFAULT_CONFIG[key]
                
            json.dump(self.config, open("config.json", "w"), indent=4)

        if self.get("token") == "":
            console.print_error("No token found, please set it below.")
            new_token = input("> ")

            self.set("token", new_token)

        if self.get("prefix") == "":
            console.print_error("No prefix found, please set it below.")
            new_prefix = input("> ")

            self.set("prefix", new_prefix)

    def save(self) -> None:
        if isinstance(self.config["theme"], dict):
            self.save_theme_file(self.config["theme_name"], self.config["theme"])
            self.config["theme"] = self.config["theme_name"]
            self.config.pop("theme_name")

        json.dump(self.config, open("config.json", "w"), indent=4)

    def get(self, key) -> str:
        return self.config[key]

    def set(self, key, value) -> None:
        self.config[key] = value
        self.save()

    def get_theme_file(self, theme):        
        return json.load(open(f"themes/{theme}.json")) if os.path.exists(f"themes/{theme}.json") else None
    
    def save_theme_file(self, theme_name, new_obj) -> None:
        json.dump(new_obj, open(f"themes/{theme_name}.json", "w"), indent=4)

    def set_theme(self, theme_name):
        theme = self.get_theme_file(theme_name)
        self.config["theme_name"] = theme_name
        self.config["theme"] = theme
        self.save()

    def get_themes(self):
        return [file.split(".")[0] for file in os.listdir("themes/")]
    
    def add_nitro_snipe(self, code):
        if self.check_sniped_code(code):
            return False

        with open("data/sniped_codes.txt", "a") as f:
            f.write(f"{code}\n")

        return True

    def get_sniped_codes(self):
        with open("data/sniped_codes.txt", "r") as f:
            return f.read().splitlines()
        
    def remove_sniped_code(self, code):
        codes = self.get_sniped_codes()
        codes.remove(code)
        
        with open("data/sniped_codes.txt", "w") as f:
            f.write("\n".join(codes))

    def check_sniped_code(self, code):
        return code in self.get_sniped_codes()
    
    def get_snipers(self):
        return self.config["snipers"]
    
    def get_sniper_status(self, sniper):
        return self.config["snipers"][sniper]["enabled"]
    
    def enable_sniper(self, sniper):
        self.config["snipers"][sniper]["enabled"] = True
        self.save()

        return self.config["snipers"][sniper]["enabled"]

    def disable_sniper(self, sniper):
        self.config["snipers"][sniper]["enabled"] = False
        self.save()

        return self.config["snipers"][sniper]["enabled"]

    def toggle_sniper(self, sniper):
        self.config["snipers"][sniper]["enabled"] = not self.config["snipers"][sniper]["enabled"]
        self.save()
        return self.config["snipers"][sniper]["enabled"]

    def snipers_ignore_invalid(self, sniper):
        return self.config["snipers"][sniper]["ignore_invalid"]
    
    def toggle_snipers_ignore_invalid(self, sniper):
        self.config["snipers"][sniper]["ignore_invalid"] = not self.config["snipers"][sniper]["ignore_invalid"]
        self.save()
        return self.config["snipers"][sniper]["ignore_invalid"]