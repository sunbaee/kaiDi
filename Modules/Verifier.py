from Modules.Managers.Config.config import *;
from Modules.Managers.Data.data import *;
from Modules.Display.display import ExitMSG, Help;

# Verifies optional arguments and manages options

class ArgumentResponse:
    def __init__(self, search: list[str], saveTranslation: bool):
        self.saveTranslation = saveTranslation;
        self.search = search;

def __InvalidOption(argument):
    ExitMSG(f"\033[1;31m /ᐠ - ˕ -マ {argument} is an invalid option. Use -h option for help. \033[00m");

def CheckArguments(args: list[str]) -> ArgumentResponse:
    # Variables to be returned
    usingOptions = saveTranslation = False;
    search = [];

    # Command line options
    for i, argument in enumerate(args):
        # Get options
        if argument[0] == '-':
            if len(argument) != 2: __InvalidOption(argument);
            
            usingOptions = True;
            match argument[1]:
                # Display options

                # Shows help message
                case 'h': Help();
                # Shows log of translations
                case 'l': 
                    DisplayData('logs'); DisplayData('saved');
                    print('\n\033[1m * :\033[0m Searched with \033[1mfastmode\033[0m\n'); exit();
                # Display options from the configuration file
                case 'i': DisplayConfig();
                
                # Managing files

                # Updates config file
                case 'u': UpdateConfig(args, i, search);
                # Clears logs or saved logs
                case 'c': ClearLog(args, i);
                # Toogle fast translation
                case 'f': ToogleFast();
                # Saves translation to be used later
                case 's': saveTranslation = True;
                # Default message
                case _: __InvalidOption(argument);

        # Get all arguments before the first option (all text to be translated)
        if not usingOptions: search.append(argument);

    return ArgumentResponse(search, saveTranslation);
