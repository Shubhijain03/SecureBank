from colorama import Fore, Style, init

init(autoreset=True)


def heading(text):
    print(Fore.BLUE + Style.BRIGHT + text)


def success(text):
    print(Fore.GREEN + Style.BRIGHT + text)


def error(text):
    print(Fore.RED + Style.BRIGHT + text)


def warning(text):
    print(Fore.YELLOW + Style.BRIGHT + text)


def info(text):
    print(Fore.CYAN + text)