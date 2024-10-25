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