import colorama
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

    # banner = banner.replace("█", f"{colorama.Fore.WHITE}{colorama.Style.BRIGHT}█{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╗", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}╗{colorama.Style.RESET_ALL}")
    # banner = banner.replace("║", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}║{colorama.Style.RESET_ALL}")
    # banner = banner.replace("═", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}═{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╝", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}╝{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╔", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}╔{colorama.Style.RESET_ALL}")
    # banner = banner.replace("╚", f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}╚{colorama.Style.RESET_ALL}")
    
    print(pystyle.Center.XCenter(banner))
    # for line in banner.splitlines():
    #     print(f"{line}".center(os.get_terminal_size().columns))
    
    print()
    print(f"—————————————————————————————————————{copyright_}—————————————————————————————————————")
    print(f"{colorama.Style.RESET_ALL}")

def print_color(color, text):
    print(color + text + colorama.Style.RESET_ALL)

def print_cmd(text):
    print(f"{colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}[COMMAND]{colorama.Style.RESET_ALL} {text}")

def print_info(text):
    print(f"{colorama.Fore.LIGHTGREEN_EX}{colorama.Style.BRIGHT}[INFO]{colorama.Style.RESET_ALL} {text}")

def print_success(text):
    print(f"{colorama.Fore.LIGHTGREEN_EX}{colorama.Style.BRIGHT}[SUCCESS]{colorama.Style.RESET_ALL} {text}")

def print_error(text):
    print(f"{colorama.Fore.LIGHTRED_EX}{colorama.Style.BRIGHT}[ERROR]{colorama.Style.RESET_ALL} {text}")

def print_warning(text):
    print(f"{colorama.Fore.LIGHTYELLOW_EX}{colorama.Style.BRIGHT}[WARNING]{colorama.Style.RESET_ALL} {text}")

def print_cli(text):
    print(f"{colorama.Fore.LIGHTMAGENTA_EX}{colorama.Style.BRIGHT}[CLI]{colorama.Style.RESET_ALL} {text}")