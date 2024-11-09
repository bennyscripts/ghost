# anyone reading this, i sincerely apologize for the mess you're about to witness
# tkinter sucks and i hate it

import os
import discord
import requests
import threading
import ttkbootstrap as ttk

from utils import console
from utils import config

from pathlib import Path
from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText

PATH = Path(__file__).parent

class GhostGUI:
    def __init__(self, bot=None):
        self.bot = bot
        self.width = 600
        self.height = 450
        self.bot_started = False

        self.root = ttk.tk.Tk()
        self.root.title("Ghost")
        self.root.geometry(f"{self.width}x{self.height}")
        # self.root.resizable(False, False)
        self.root.style = ttk.Style()
        self.root.style.theme_use("darkly")
        self.root.style.configure("TEntry", background=self.root.style.colors.get("secondary"))
        self.root.style.configure("TCheckbutton", background=self.root.style.colors.get("secondary"))

        # self.root.style.configure("primary.TButton", background="#254bff")
        # self.root.style.configure("secondary.TButton", background="#383838")
        # self.root.style.configure("success.TButton", background="#00db7c")
        # self.root.style.configure("danger.TButton", background="#e7230f")
        # self.root.style.configure("warning.TButton", background="#f39500")

    def format_changelog(self, changelog):
        info = {
            "New": [],
            "Fixed": [],
            "Changed": [],
            "Removed": []
        }

        for line in changelog:
            if line == "":
                continue

            line = line[8:]

            for char in line.split(" "):
                if char.lower() in ["added", "add", "new"]:
                    info["New"].append(line)
                    break
                elif char.lower() in ["fixed", "fix"]:
                    info["Fixed"].append(line)
                    break
                elif char.lower() in ["changed", "change"]:
                    info["Changed"].append(line)
                    break
                elif char.lower() in ["removed", "remove"]:
                    info["Removed"].append(line)
                    break
                else:
                    info["Changed"].append(line)
                    break

        text = ""

        for key in info:
            text += f"{key}:\n"
            for item in info[key]:
                text += f"  - {item}\n"
            text += "\n"

        return text

    def get_changelog(self):
        resp = requests.get("https://api.github.com/repos/bennyscripts/ghost/releases")
        if resp.status_code != 200:
            return "0", "Failed to get changelog."
        
        data = resp.json()

        if len(data) == 0:
            return "0", "No changelog available."

        version = data[0]["tag_name"]
        changelog = data[0]["body"]

        changelog = changelog.split("## ")[2]

        changelog = changelog.replace("##", "").replace("###", "").replace("####", "").replace("#####", "").replace("######", "")
        changelog = changelog.replace("**", "").replace("*", "").replace("`", "")
        changelog = changelog.replace("> ", "")
        changelog = changelog.replace("\r", "").replace("\n\n", "\n")

        changelog = "\n".join([line for line in changelog.split("\n") if line.strip() != ""])
        changelog = "\n".join(changelog.split("\n")[1:])

        return version, self.format_changelog(changelog.split("\n"))

    def quit(self):
        console.print_info("Quitting Ghost...")

        if os.name == "nt":
            os.kill(os.getpid(), 9)
        else:
            os._exit(0)

    def draw_sidebar(self):
        width = self.width // (self.width // 100)
        self.sidebar = ttk.Frame(self.root, width=width, height=self.height)
        self.sidebar.pack(fill=ttk.BOTH, side=ttk.LEFT)
        self.sidebar.configure(style="dark.TFrame")
        self.sidebar.grid_propagate(False)
        
        home_button = ttk.Button(self.sidebar, text="Home", command=self.draw_home)
        settings_button = ttk.Button(self.sidebar, text="Settings", command=self.draw_settings)
        theming_button = ttk.Button(self.sidebar, text="Theming", command=self.draw_theming)
        snipers_button = ttk.Button(self.sidebar, text="Snipers", command=self.draw_snipers)
        logout_button = ttk.Button(self.sidebar, text="Quit", command=self.quit)

        home_button.configure(style="primary.TButton")
        settings_button.configure(style="primary.TButton")
        theming_button.configure(style="primary.TButton")
        snipers_button.configure(style="primary.TButton")
        logout_button.configure(style="danger.TButton")

        home_button.grid(row=0, column=0, sticky=ttk.NSEW, pady=(10, 2), padx=10, ipady=5)
        settings_button.grid(row=1, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=5)
        theming_button.grid(row=2, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=5)
        snipers_button.grid(row=3, column=0, sticky=ttk.NSEW, pady=2, padx=10, ipady=5)
        logout_button.grid(row=5, column=0, sticky=ttk.NSEW, pady=(2, 10), padx=10, ipady=10)

        self.sidebar.grid_rowconfigure(4, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

    def draw_main(self, scrollable=False):
        width = self.width - (self.width // 100)
        main = ScrolledFrame(self.root, width=width, height=self.height) if scrollable else ttk.Frame(self.root, width=width, height=self.height)
        main.pack(fill=ttk.BOTH, expand=True, padx=10, pady=10)

        return main
    
    def clear_main(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()

        self.draw_sidebar()
    
    def draw_home(self):
        self.clear_main()
        main = self.draw_main()
        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35
        latest_version, latest_changelog = self.get_changelog()

        title = ttk.Label(main, text=f"Ghost v{config.VERSION}", font=("Arial", 20, "bold"))
        subtitle = ttk.Label(main, text=config.MOTD, font=("Arial Italic", 14))
        
        title.grid(row=0, column=0, sticky=ttk.NSEW)
        subtitle.grid(row=1, column=0, columnspan=2, sticky=ttk.NSEW)

        changelog_frame = ttk.Frame(main, bootstyle="secondary")
        changelog_frame.grid(row=2, column=0, sticky=ttk.NSEW, pady=15)

        changelog_title = ttk.Label(changelog_frame, text=f"Latest Changelog")
        changelog_title.configure(background=self.root.style.colors.get("secondary"))
        # place the title along the top edge of the frame
        changelog_title.pack(fill=ttk.X, padx=10, pady=5)

        changelog_text_frame = ScrolledFrame(changelog_frame, width=width, height=350, bootstyle="secondary")
        changelog_text = ttk.Label(changelog_text_frame, text=latest_changelog, wraplength=width, justify=ttk.LEFT)
        changelog_text.configure(foreground=self.root.style.colors.get("light"), background=self.root.style.colors.get("secondary"))
        changelog_text.pack(fill=ttk.BOTH, expand=True, padx=10, pady=2)

        changelog_text_frame.pack(fill=ttk.BOTH, expand=True)

        main.grid_columnconfigure(0, weight=1)

    def draw_snipers(self):
        self.clear_main()
        main = self.draw_main()
        cfg = config.Config()

        snipers = cfg.get_snipers()
        snipers_tk_entries = {}

        def save_sniper(sniper_name):
            sniper: config.Sniper = cfg.get_sniper(sniper_name)

            for key, entry in snipers_tk_entries[sniper_name].items():
                if key == "webhook":
                    sniper.set_webhook(entry.get())
                elif key == "enabled":
                    if entry.instate(["selected"]):
                        sniper.enable()
                    else:
                        sniper.disable()
                else:
                    sniper.set(key, entry.instate(["selected"]))

            sniper.save()
        
        title = ttk.Label(main, text="Snipers", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky=ttk.NSEW)

        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35 // 2

        snipers_wrapper_frame = ttk.Frame(main, width=width)
        snipers_wrapper_frame.configure(style="default.TLabel")
        snipers_wrapper_frame.grid(row=1, column=0, sticky=ttk.NSEW, pady=13)
        main.grid_columnconfigure(0, weight=1)

        for index, sniper in enumerate(snipers):
            column = index % 2
            row = 1 + (index // 2)
            padding = (5, 2)

            snipers_tk_entries[sniper.name] = {}

            # if the sniper is on the first column then remove the left padding and vice versa
            if column == 0:
                padding = (0, 2)
            elif column == 1:
                padding = ((5, 0), 2)

            sniper_frame = ttk.Frame(snipers_wrapper_frame, width=width, style="secondary.TFrame")
            sniper_frame.grid(row=row, column=column, sticky=ttk.NSEW, padx=padding[0], pady=padding[1])

            snipers_wrapper_frame.grid_columnconfigure(column, weight=1)

            sniper_title = ttk.Label(sniper_frame, text=f"{sniper.name.capitalize()} Sniper", font=("Arial", 16, "bold"))
            sniper_title.configure(background=self.root.style.colors.get("secondary"))
            sniper_title.grid(row=0, column=0, sticky=ttk.NSEW, pady=(5, 0), padx=5)

            for index, (key, value) in enumerate(sniper.to_dict().items()):
                if isinstance(value, bool):
                    checkbox = ttk.Checkbutton(sniper_frame, text=" ".join(word.capitalize() for word in str(key).split("_")), style="success.TCheckbutton")
                    checkbox.grid(row=index + 1, column=0, sticky=ttk.W, pady=(5, 0), padx=7)

                    if value:
                        checkbox.invoke()
                    else:
                        for _ in range(2):
                            checkbox.invoke() 

                    snipers_tk_entries[sniper.name][key] = checkbox
                else:
                    label = ttk.Label(sniper_frame, text=f"{key.capitalize()}")
                    label.configure(background=self.root.style.colors.get("secondary"))

                    entry = ttk.Entry(sniper_frame, bootstyle="secondary")
                    if value != "":
                        entry.insert(0, value)
                    else:
                        entry.insert(0, "Paste your webhook here...")

                    label.grid(row=index + 1, column=0, sticky=ttk.W, pady=(8, 0), padx=5)
                    entry.grid(row=index + 2, column=0, sticky=ttk.EW, padx=5, columnspan=2)

                    sniper_frame.grid_columnconfigure(1, weight=1)

                    snipers_tk_entries[sniper.name][key] = entry

            row = len(sniper.to_dict()) + 2

            save_button = ttk.Button(sniper_frame, text="Save", style="success.TButton", command=lambda sniper_name=sniper.name: save_sniper(sniper_name))
            save_button.grid(row=row, column=0, sticky=ttk.EW, pady=(5, 0), columnspan=2, ipady=5)

    def draw_theming(self):
        self.clear_main()
        main = self.draw_main()
        cfg = config.Config()

        themes = cfg.get_themes()
        theme_dict = cfg.theme.to_dict()
        theme_tk_entries = []

        def save_theme():
            for index, (key, value) in enumerate(theme_dict.items()):
                cfg.theme.set(key, theme_tk_entries[index].get())

            cfg.theme.save()

            # get the message style entry
            message_style = message_style_entry.cget("text")
            cfg.set("message_settings.style", message_style)

        def set_theme(theme):
            select_theme_menu.configure(text=theme)
            cfg.set_theme(theme)
            self.draw_theming()

        def delete_theme():
            double_check = ttk.Toplevel(self.root)

            double_check.title("Are you sure?")
            double_check.resizable(False, False)

            label = ttk.Label(double_check, text="Are you sure you want to delete this theme?")
            delete_button = ttk.Button(double_check, text="Yes", style="danger.TButton", command=lambda: delete(double_check))

            label.grid(row=0, column=0, sticky=ttk.NSEW, padx=10, pady=10)
            delete_button.grid(row=1, column=0, sticky=ttk.NSEW, padx=10, pady=10)

        def delete(toplevel):
            toplevel.destroy()

            if cfg.theme.name.lower() == "ghost":
                console.print_error("Cannot delete the default theme.")
                return
            
            cfg.delete_theme(cfg.theme.name)
            self.draw_theming()

        def create_theme(theme_name):
            if theme_name is None or theme_name == "":
                console.print_error("Please enter a theme name.")
                return
            
            success = cfg.create_theme(theme_name)
            
            if isinstance(success, bool) and not success:
                console.print_error("Theme already exists.")
                return
            
            cfg.set_theme(success.name)
            cfg.save()
            self.draw_theming()

        title = ttk.Label(main, text="Theming", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky=ttk.NSEW)

        width = main.winfo_reqwidth() - self.sidebar.winfo_reqwidth() - 35

        theme_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        theme_frame.grid(row=1, column=0, sticky=ttk.NSEW, pady=15)

        main.grid_columnconfigure(0, weight=1)

        create_theme_label = ttk.Label(theme_frame, text="Create a new theme")
        create_theme_label.configure(background=self.root.style.colors.get("secondary"))

        create_theme_entry = ttk.Entry(theme_frame, bootstyle="secondary")
        create_theme_button = ttk.Button(theme_frame, text="Create", style="success.TButton", command=lambda: create_theme(create_theme_entry.get()))

        create_theme_label.grid(row=0, column=0, sticky=ttk.W, padx=(10, 0), pady=(10, 0))
        create_theme_entry.grid(row=0, column=1, sticky="we", padx=(10, 10), pady=(10, 0))
        create_theme_button.grid(row=0, column=2, sticky=ttk.E, padx=(0, 11), pady=(10, 0))

        select_theme_label = ttk.Label(theme_frame, text="Select a theme")
        select_theme_label.configure(background=self.root.style.colors.get("secondary"))

        select_theme_menu = ttk.Menubutton(theme_frame, text=cfg.theme.name, bootstyle="dark")
        select_theme_menu.menu = ttk.Menu(select_theme_menu, tearoff=0)
        select_theme_menu["menu"] = select_theme_menu.menu

        for theme in themes:
            select_theme_menu.menu.add_command(label=str(theme), command=lambda theme=theme.name: set_theme(theme))

        message_style_label = ttk.Label(theme_frame, text="Global message style")
        message_style_label.configure(background=self.root.style.colors.get("secondary"))

        message_style_entry = ttk.Menubutton(theme_frame, text=cfg.config["message_settings"]["style"], bootstyle="dark")
        message_style_entry.menu = ttk.Menu(message_style_entry, tearoff=0)
        message_style_entry["menu"] = message_style_entry.menu

        for style in ["codeblock", "image"]:
            message_style_entry.menu.add_command(label=style, command=lambda style=style: message_style_entry.configure(text=style))

        select_theme_label.grid(row=1, column=0, sticky=ttk.W, padx=(10, 0), pady=(10, 0))
        select_theme_menu.grid(row=1, column=1, columnspan=2, sticky="we", padx=(10, 10), pady=(10, 0))

        message_style_label.grid(row=2, column=0, sticky=ttk.W, padx=(10, 0), pady=(10, 0))
        message_style_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=(10, 10), pady=(10, 0))

        # draw a horizontal line
        ttk.Separator(theme_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="we", padx=(10, 10), pady=(15, 5))

        for index, (key, value) in enumerate(theme_dict.items()):
            padding = (10, 0)
            entry = ttk.Entry(theme_frame, bootstyle="secondary")
            entry.insert(0, value)

            if index == 0:
                padding = (padding[0], (10, 0))
            elif index == len(theme_dict) - 1:
                padding = (padding[0], (0, 10))

            label = ttk.Label(theme_frame, text=key.capitalize())
            label.configure(background=self.root.style.colors.get("secondary"))
            
            label.grid(row=index + 4, column=0, sticky=ttk.W, padx=padding[0], pady=padding[1])
            entry.grid(row=index + 4, column=1, columnspan=2, sticky="we", padx=padding[0], pady=padding[1])

            theme_frame.grid_columnconfigure(1, weight=1)
            theme_tk_entries.append(entry)

        ttk.Separator(theme_frame, orient="horizontal").grid(row=len(theme_dict) + 5, column=0, columnspan=3, sticky="we", padx=(10, 10), pady=(5, 15))

        save_theme_label = ttk.Label(theme_frame, text="Remember to save your changes!", font=("Arial Italic", 14))
        save_theme_label.configure(background=self.root.style.colors.get("secondary"))
        save_theme_button = ttk.Button(theme_frame, text="Save", style="success.TButton", command=save_theme)
        delete_theme_button = ttk.Button(theme_frame, text="Delete", style="danger.TButton", command=delete_theme)
        
        save_theme_label.grid(row=len(theme_dict) + 6, column=0, columnspan=2, sticky=ttk.W, padx=(10, 0), pady=(0, 10))
        save_theme_button.grid(row=len(theme_dict) + 6, column=1, sticky=ttk.E, padx=(0, 5), pady=(0, 10))
        delete_theme_button.grid(row=len(theme_dict) + 6, column=2, sticky=ttk.E, padx=(0, 11), pady=(0, 10))

    def draw_settings(self):
        self.clear_main()
        main = self.draw_main(scrollable=False)
        cfg = config.Config()

        config_tk_entries = {}
        config_entries = {
            "token": "Token",
            "prefix": "Prefix",
            "theme": "Theme",
            "rich_presence": "Enable rich presence",
            "gui": "Enable GUI",
            "message_settings.auto_delete_delay": "Auto delete delay",
        }

        def save_cfg():
            for index, (key, value) in enumerate(config_entries.items()):
                tkinter_entry = config_tk_entries[key]

                if key == "rich_presence" or key == "theme" or key == "gui":
                    continue

                if key == "prefix":
                    self.bot.command_prefix = tkinter_entry.get()

                if "message_settings" in key:
                    if tkinter_entry.get().isdigit():
                        cfg.set(key, int(tkinter_entry.get()), save=False)
                    else:
                        console.print_error("Auto delete delay must be an integer.")
                        continue

                cfg.set(key, tkinter_entry.get())

            cfg.set("rich_presence", config_tk_entries["rich_presence"].instate(["selected"]), save=False)
            cfg.set("gui", config_tk_entries["gui"].instate(["selected"]), save=False)
            
            cfg.save()
            cfg.check()

        width = self.width - self.sidebar.winfo_reqwidth() - 35

        title = ttk.Label(main, text="Settings", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky=ttk.W)

        config_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        config_frame.grid(row=1, column=0, sticky=ttk.EW, pady=15)

        main.grid_columnconfigure(0, weight=1)

        for index, (key, value) in enumerate(config_entries.items()):
            if key == "rich_presence" or key == "gui":
                continue

            padding = (10, 0)
            cfg_value = cfg.get(key)
            entry = ttk.Entry(config_frame, bootstyle="secondary") if key != "token" else ttk.Entry(config_frame, bootstyle="secondary", show="*")
            if key == "theme":
                entry.insert(0, "Use theming page to edit your theme.")
                entry.configure(state="readonly")
            else:
                entry.insert(0, cfg_value)

            if index == 0:
                padding = (padding[0], (10, 0))
            elif index == len(config_entries) - 1:
                padding = (padding[0], (0, 5))

            label = ttk.Label(config_frame, text=value)
            label.configure(background=self.root.style.colors.get("secondary"))
            
            label.grid(row=index + 1, column=0, sticky=ttk.W, padx=padding[0], pady=padding[1])
            entry.grid(row=index + 1, column=1, sticky="we", padx=padding[0], pady=padding[1], columnspan=3)

            config_frame.grid_columnconfigure(1, weight=1)
            config_tk_entries[key] = entry

        rpc_checkbox = ttk.Checkbutton(config_frame, text="Enable rich presence", style="success.TCheckbutton")
        rpc_checkbox.grid(row=len(config_entries) + 1, column=0, columnspan=2, sticky=ttk.W, padx=(13, 0), pady=(10, 0))
        if cfg.get("rich_presence"):
            rpc_checkbox.invoke()
        else:
            for _ in range(2):
                rpc_checkbox.invoke()

        gui_checkbox = ttk.Checkbutton(config_frame, text="Enable GUI", style="success.TCheckbutton")
        gui_checkbox.grid(row=len(config_entries) + 2, column=0, columnspan=2, sticky=ttk.W, padx=(13, 0), pady=(10, 0))
        if cfg.get("gui"):
            gui_checkbox.invoke()
        else:
            for _ in range(2):
                gui_checkbox.invoke()

        config_tk_entries["rich_presence"] = rpc_checkbox
        config_tk_entries["gui"] = gui_checkbox

        restart_required_label = ttk.Label(config_frame, text="A restart is required to apply changes!", font=("Arial Italic", 14))
        restart_required_label.configure(background=self.root.style.colors.get("secondary"))

        restart_required_label.grid(row=len(config_entries) + 3, column=0, columnspan=2, sticky=ttk.W, padx=(10, 0), pady=10)
        save_cfg_button = ttk.Button(config_frame, text="Save", style="success.TButton", command=save_cfg)
        save_cfg_button.grid(row=len(config_entries) + 3, column=3, sticky=ttk.E, padx=(0, 11), pady=10)

        # -----------------

        apis_subtitle = ttk.Label(main, text="API Keys", font=("Arial", 16, "bold"))
        apis_subtitle.grid(row=2, column=0, sticky=ttk.W, pady=(15, 5))

        apis_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        apis_frame.grid(row=3, column=0, sticky=ttk.EW, pady=5)

        api_keys_tk_entries = {}
        api_keys_entries = {
            "serpapi": "SerpAPI",
        }

        def save_api_keys():
            for index, (key, value) in enumerate(api_keys_entries.items()):
                tkinter_entry = api_keys_tk_entries[key]
                cfg.set(f"apis.{key}", tkinter_entry.get())

            cfg.save()

        for index, (key, value) in enumerate(api_keys_entries.items()):
            padding = (10, 0)
            cfg_value = cfg.get(f"apis.{key}")
            entry = ttk.Entry(apis_frame, bootstyle="secondary", show="*")
            entry.insert(0, cfg_value)

            if index == 0:
                padding = (padding[0], (10, 0))
            elif index == len(api_keys_entries) - 1:
                padding = (padding[0], (0, 5))

            label = ttk.Label(apis_frame, text=value)
            label.configure(background=self.root.style.colors.get("secondary"))
            
            label.grid(row=index + 1, column=0, sticky=ttk.W, padx=(10, 5), pady=padding[1])
            entry.grid(row=index + 1, column=1, sticky="we", padx=(0, 10), pady=padding[1], columnspan=2)

            apis_frame.grid_columnconfigure(1, weight=1)
            api_keys_tk_entries[key] = entry

        save_api_keys_button = ttk.Button(apis_frame, text="Save", style="success.TButton", command=save_api_keys)
        save_api_keys_button.grid(row=len(api_keys_entries) + 1, column=2, sticky=ttk.E, padx=(0, 11), pady=10)

        # -----------------

        session_spoofing_subtitle = ttk.Label(main, text="Session Spoofing", font=("Arial", 16, "bold"))
        session_spoofing_subtitle.grid(row=4, column=0, sticky=ttk.W, pady=(15, 5))

        session_spoofing_frame = ttk.Frame(main, width=width, style="secondary.TFrame")
        session_spoofing_frame.grid(row=5, column=0, sticky=ttk.EW, pady=5)

        session_spoofing_checkbox = ttk.Checkbutton(session_spoofing_frame, text="Enable session spoofing", style="success.TCheckbutton")
        session_spoofing_checkbox.grid(row=0, column=0, columnspan=2, sticky=ttk.W, padx=(13, 0), pady=(10, 0))
        
        if cfg.get("session_spoofing"):
            session_spoofing_checkbox.invoke()
        else:
            for _ in range(2):
                session_spoofing_checkbox.invoke()

        session_spoofing_device_label = ttk.Label(session_spoofing_frame, text="Session spoofing device")
        session_spoofing_device_label.configure(background=self.root.style.colors.get("secondary"))

        session_spoofing_device_entry = ttk.Menubutton(session_spoofing_frame, text=cfg.get("session_spoofing.device"), bootstyle="dark")
        session_spoofing_device_entry.menu = ttk.Menu(session_spoofing_device_entry, tearoff=0)
        session_spoofing_device_entry["menu"] = session_spoofing_device_entry.menu

        for device in ["mobile", "desktop", "web", "embedded"]:
            session_spoofing_device_entry.menu.add_command(label=device, command=lambda device=device: session_spoofing_device_entry.configure(text=device))

        session_spoofing_device_label.grid(row=1, column=0, sticky=ttk.W, padx=(10, 0), pady=(5, 0))
        session_spoofing_device_entry.grid(row=1, column=1, sticky="we", padx=(10, 10), pady=(5, 0))

        def save_session_spoofing():
            cfg.set("session_spoofing.enabled", session_spoofing_checkbox.instate(["selected"]))
            cfg.set("session_spoofing.device", session_spoofing_device_entry.cget("text"))
            cfg.save()

        save_session_spoofing_button = ttk.Button(session_spoofing_frame, text="Save", style="success.TButton", command=save_session_spoofing)
        save_session_spoofing_button.grid(row=2, column=1, sticky=ttk.E, padx=(0, 11), pady=10)

        restart_required_label = ttk.Label(session_spoofing_frame, text="A restart is required to apply changes!", font=("Arial Italic", 14))
        restart_required_label.configure(background=self.root.style.colors.get("secondary"))

        restart_required_label.grid(row=2, column=0, sticky=ttk.W, padx=(10, 0), pady=10)

        session_spoofing_frame.grid_columnconfigure(1, weight=1)

    def run(self):
        cfg = config.Config()
        if cfg.get("gui"):
            bot_start_btn = ttk.Button(self.root, text="Start Ghost", command=self.start_bot_thread)
            bot_start_btn.pack(fill=ttk.BOTH, side=ttk.BOTTOM, pady=10)

            bot_start_btn.invoke()
            bot_start_btn.destroy()

            while not self.bot_started:
                pass

            self.draw_sidebar()
            self.draw_home()

            self.root.mainloop()

        else:
            self.start_bot()

    def start_bot(self):
        cfg = config.Config()

        try:
            console.print_info("Starting Ghost...")
            self.bot.run(cfg.get("token"), log_handler=console.handler)
        except discord.errors.LoginFailure:
            console.print_error("Failed to login, please check your token.")
            self.quit()

    def start_bot_thread(self):
        self.thread = threading.Thread(target=self.start_bot)
        self.thread.start()

if __name__ == "__main__":
    gui = GhostGUI()
    gui.run()
