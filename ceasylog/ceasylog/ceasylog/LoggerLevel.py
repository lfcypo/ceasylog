from colorama import Fore, Back


class DEBUG:
    des = "DEBUG"
    level = 1
    msg = " D "
    frontStyle = Fore.BLUE
    backStyle = Back.BLUE + Fore.LIGHTWHITE_EX


class INFO:
    des = "INFO"
    level = 2
    msg = " I "
    frontStyle = Fore.GREEN
    backStyle = Back.GREEN + Fore.LIGHTWHITE_EX


class WARN:
    des = "WARN"
    level = 3
    msg = " W "
    frontStyle = Fore.YELLOW
    backStyle = Back.YELLOW + Fore.LIGHTWHITE_EX


class ERROR:
    des = "ERROR"
    level = 4
    msg = " E "
    frontStyle = Fore.RED
    backStyle = Back.RED + Fore.LIGHTWHITE_EX


class CRITICAL:
    des = "CRITICAL"
    level = 5
    msg = " C "
    frontStyle = Fore.LIGHTRED_EX
    backStyle = Back.LIGHTRED_EX + Fore.LIGHTWHITE_EX
