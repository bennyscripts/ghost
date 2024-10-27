import colorama
import datetime
import os, sys, pystyle

from . import config

def clear():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

def resize(columns, rows):
    if sys.platform == "win32":
        os.system(f"mode con cols={columns} lines={rows}")
    else:
        os.system(f"echo '\033[8;{rows};{columns}t'")

def get_formatted_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def print_banner():
    copyright_ = f"( Ghost v{config.VERSION} )"
    banner = f""" ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██║  ███╗███████║██║   ██║███████╗   ██║   
██║   ██║██╔══██║██║   ██║╚════██║   ██║   
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   

"""
    print(colorama.Fore.LIGHTBLUE_EX + colorama.Style.BRIGHT)

    # banner = banner.replace("█", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}█{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╗", f"{colorama.Fore.WHITE}{colorama.Style.DIM}╗{colorama.Style.RESET_ALL}")
    # banner = banner.replace("║", f"{colorama.Fore.WHITE}{colorama.Style.DIM}║{colorama.Style.RESET_ALL}")
    # banner = banner.replace("═", f"{colorama.Fore.WHITE}{colorama.Style.DIM}═{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╝", f"{colorama.Fore.WHITE}{colorama.Style.DIM}╝{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╔", f"{colorama.Fore.WHITE}{colorama.Style.DIM}╔{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╚", f"{colorama.Fore.WHITE}{colorama.Style.DIM}╚{colorama.Style.RESET_ALL}")
    
    print(pystyle.Center.XCenter(banner))
    
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}")
    print(pystyle.Center.XCenter(config.MOTD))
    print()
    print(f"{colorama.Fore.BLUE}—————————————————————————————————————{copyright_}—————————————————————————————————————")
    print(f"{colorama.Style.RESET_ALL}")

def print_color(color, text):
    print(color + text + colorama.Style.RESET_ALL)

def print_cmd(text):
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}[COMMAND]{colorama.Style.RESET_ALL} {text}")

def print_info(text):
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colorama.Fore.LIGHTGREEN_EX}{colorama.Style.BRIGHT}[INFO]{colorama.Style.RESET_ALL} {text}")

def print_success(text):
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colorama.Fore.LIGHTGREEN_EX}{colorama.Style.BRIGHT}[SUCCESS]{colorama.Style.RESET_ALL} {text}")

def print_error(text):
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colorama.Fore.LIGHTRED_EX}{colorama.Style.BRIGHT}[ERROR]{colorama.Style.RESET_ALL} {text}")

def print_warning(text):
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colorama.Fore.LIGHTYELLOW_EX}{colorama.Style.BRIGHT}[WARNING]{colorama.Style.RESET_ALL} {text}")

def print_cli(text):
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colorama.Fore.LIGHTMAGENTA_EX}{colorama.Style.BRIGHT}[CLI]{colorama.Style.RESET_ALL} {text}")

def print_sniper(sniper, title, description: dict, success=True):
    colour = colorama.Fore.LIGHTGREEN_EX if success else colorama.Fore.LIGHTRED_EX
    print(f"{colorama.Style.NORMAL}{colorama.Fore.WHITE}[{get_formatted_time()}] {colour}{colorama.Style.BRIGHT}[{sniper.upper()}]{colorama.Style.RESET_ALL} {title}")

    for key, value in description.items():
        print(f"{' '*10} {colorama.Fore.LIGHTYELLOW_EX}{colorama.Style.NORMAL}{key}: {colorama.Style.RESET_ALL}{value}")
    
    print()