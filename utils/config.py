import json
import os

from . import console
from . import webhook as webhook_client

MOTD = "Lobsters pee out of their faces. From right under their eyes".lower()
VERSION = "3.3.0"
PRODUCTION = True
DEFAULT_CONFIG = {
    "token": "",
    "prefix": "",
    "rich_presence": True,
    "theme": "ghost",
    "message_settings": {
        "auto_delete_delay": 15,
        "style": "image"
    },
    "snipers": {
        "nitro": {
            "enabled": True,
            "ignore_invalid": False,
            "webhook": ""
        },
        "privnote": {
            "enabled": True,
            "ignore_invalid": False,
            "webhook": ""
        }
    },
    "apis": {
        "serpapi": ""
    }
}
DEFAULT_THEME = {
    "title": "ghost selfbot",
    "emoji": "\ud83d\udc99",
    "image": "https://cdn.discordapp.com/icons/1302632843176050738/e7f5c4fa0080423094fd8025f3f8d5a1.png?size=1024",
    "colour": "#575757",
    "footer": "ghost aint dead"
}

class Sniper:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.enabled = kwargs.get("enabled")
        self.ignore_invalid = kwargs.get("ignore_invalid")
        self.webhook = kwargs.get("webhook")
        self.config = Config()

    def save(self):
        self.config.config["snipers"][self.name] = {
            "enabled": self.enabled,
            "ignore_invalid": self.ignore_invalid,
            "webhook": self.webhook
        }
        self.config.save()

    def __str__(self):
        return self.name
    
    def get_webhook(self):
        return webhook_client.Webhook.from_url(self.webhook)
    
    def set_webhook(self, webhook):
        self.webhook = webhook.url
        self.save()

    def enable(self):
        self.enabled = True
        self.save()

    def disable(self):
        self.enabled = False
        self.save()

    def toggle(self):
        self.enabled = not self.enabled
        self.save()
        
    def ignore_invalid(self):
        self.ignore_invalid = True
        self.save()

    def toggle_ignore_invalid(self):
        self.ignore_invalid = not self.ignore_invalid
        self.save()

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
        if not os.path.exists("data/privnote_saves.json"):
            json.dump({}, open("data/privnote_saves.json", "w"), indent=4)
            
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

    def get_sniper(self, sniper):
        if sniper not in self.config["snipers"]:
            return None
        
        obj = self.config["snipers"].get(sniper)
        obj["name"] = sniper
        return Sniper(**obj)
    
    def get_snipers(self):
        snipers = []
        for sniper in self.config["snipers"]:
            obj = self.config["snipers"][sniper]
            obj["name"] = sniper
            snipers.append(Sniper(**obj))

        return snipers