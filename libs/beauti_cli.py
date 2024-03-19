from colorama import *
init(autoreset=True)

def makeOk(text,light=False):
    if light:
        return Fore.LIGHTGREEN_EX + text + Fore.RESET
    else:
        return Fore.GREEN + text + Fore.RESET
def makeWarning(text,light=False):
    if light:
        return Fore.LIGHTYELLOW_EX + text + Fore.RESET
    else:
        return Fore.YELLOW + text + Fore.RESET
def makeError(text,light=False):
    if light:
        return Fore.LIGHTRED_EX + text + Fore.RESET
    else:
        return Fore.RED + text + Fore.RESET
def makeInfo(text,light=False):
    if light:
        return Fore.LIGHTCYAN_EX+ text + Fore.RESET
    else:
        return Fore.CYAN + text + Fore.RESET
def makeBasic(text,light=False):
    if light:
        return Fore.LIGHTWHITE_EX + text + Fore.RESET
    else:
        return Fore.WHITE + text + Fore.RESET
def printOk(text,light=False):
    print(makeOk(text,light))
def printWarning(text,light=False):
    print(makeWarning(text,light))
def printError(text,light=False):
    print(makeError(text,light))
def printInfo(text,light=False):
    print(makeInfo(text,light))
def printBasic(text,light=False):
    print(makeBasic(text,light))