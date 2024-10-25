from Modules.manager import OpenJSON, GetData;

# Some messages

def Help() -> None:
    print("\n \033[1mDescription\033[0m: A script that translates things directly from the terminal.")
    print("              (˶˃ ᵕ ˂˶) .ᐟ.ᐟ \n")
    print(" \033[1mSyntax\033[0m: kdi yourwordhere [options]\n")
    print(" \033[1mOptions: \033[0m\n")
    print("  -l : Shows log of translations and saved translations.")
    print("  -s : Saves the translation to be used later.")
    print("  -c : Clears logs or saved translations.")
    print("  -i : Displays config information.")
    print("  -u : Updates translation options.")
    print("  -f : Toggles on/off fast mode.")
    print("  -h : Shows this help message.\n")
    print("\033[1mExtended Details:\033[0m\n")
    print(" -c :  Clears one section of the translations that are shown ")
    print("       in the -l option. Defaults to \033[3m'logs'.\033[0m")
    print("         \033[1mSyntax: \033[0m\033[3m-c section\033[0m")
    print("\n             \033[3mExample:\033[0m -c saved\n")
    print(" -u :  Option used to update the configuration of the script, ")
    print("       you can use two syntaxes for this option: ")
    print("         \033[1mSyntax 1\033[0m: \033[3m-u OPT1=ARG1 OPT2=ARG2 ...\033[0m ")
    print("\n             \033[3mExamples:\033[0m sourceLanguage=en translate=de\n")
    print("         \033[1mSyntax 2:\033[0m \033[3m-u ARG1:ARG2:ARG3...\033[0m ")
    print("             In this syntax the options are in the order displayed using the -i option ")
    print('             Its necessary at least one \033[3m":"\033[0m to use this syntax')
    print("\n             \033[3mExamples:\033[0m en:pt:.com")
    print("                       pt:\n")
    print(" -f :  Enables/Disables fast mode. Fast mode allows you to search when the linguee website ")
    print("       responds with an \033[1mHTTP 429\033[0m error, but its translations ")
    print("       are very limited, not containing examples.\n")
    exit();

def ExitMSG(message) -> None:
    print(f"\n {message}\n"); exit();

def MissingArgument(customMessage='argument') -> None:
    ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ No {customMessage} supplied.\033[00m");

def DisplayConfig() -> None:
    config = OpenJSON('config.json')
    print(f'\n \033[1m(˶ ˆ ꒳ˆ˵) \033[0m\033[1mDisplaying useful information:\033[00m\n')
    print(  f' \033[1;33msourceLanguage:\033[00m {config['sourceLanguage'][0]} \033[2m({config['sourceLanguage'][1]})\033[00m')
    print(  f' \033[1;33mtranslate:\033[00m {config['translate'][0]} \033[2m({config['translate'][1]})\033[00m\n')
    print(  f' \033[1;35mdomain:\033[00m {config['domain']}')
    print(f'\n \033[1m* Fast Mode:\033[00m {config['fastTranslation']}\n')

    exit();

def DisplayData(section: str) -> None:
    searchList = GetData(section)
    if len(searchList) <= 0: print(f'\n \033[1;35m°՞(ᗒᗣᗕ)՞° You have no information in "{section}".\033[0m'); return;

    print(f'\n \033[1;35m(≧∇≦) Displaying your "{section}":\033[00m\n')

    # Gets every page dictionary in logs and displays information about that page
    for i, page in enumerate(searchList):
        # Makes slashes align after 20 chars, unless the search word has more than 20 chars. (min 2 blank spaces)
        blankSpaces = ' ' * (max(0, 20 - len(page['search'])) + 2)
        print(f"   \033[2m{(i + 1):03d} |\033[0m {page['search']}{blankSpaces}\033[2m|\033[0m\033[2m  {page['source']} - {page['translated']}  {'*' if page['fastMode'] else ''}\033[0m")