# Importing packages (standard)

import json;
import sys;

# Importing modules (local)

from Modules.Translator import Translator;
from Modules.display import *;
from Modules.manager import *;
from Modules.scrape import *;
from Modules.parser import *;

# Read-only
propertyNames = ['sourceLanguage', 'translate', 'domain']

# Used by other functions

# Binary search
def BSearch(search, dicArray, dicParameter) -> (bool, int):
    # Starting variables
    start = 0
    middle = 0
    end = len(dicArray) - 1

    while start <= end:
        middle = (start + end) // 2

        # Gets the search in the position between start and end
        curString = dicArray[middle][dicParameter]

        # If the current position is bigger than the desired search, restarts from behind current position
        # and earches after current position otherwise
        if curString > search:
            end = middle - 1; continue;
        if curString  < search:
            start = middle + 1; continue;
        
        return (True, middle);

    return (False, middle);

def SetProperties(properties: list[list[str]], currentConfig: dict) -> dict:
    temp = currentConfig;
    for prop in properties: 
        temp[prop[0]] = prop[1]
    
    return temp;

# Receives language or language code, checks if it exists and returns the correct language with its iso639 language code.
def CheckLanguage(language) -> list[str]:
    langFile = OpenJSON('languages.json')

    # * inDex is the index inside a specific language (0: language name, 1: language code)

    # Checks if the user inserted an abbreviation or 
    # a language name and changes inDex and languages variables accordingly
    if len(language) == 2:
        languages = langFile['sortedCodes']; inDex = 1
    else:
        languages = langFile['sortedLanguages']; inDex = 0;

    # Binary search to find if the language is in the languages.json file
    searchResult = BSearch(language, languages, inDex)
    if searchResult[0]: return languages[searchResult[1]]

    # Exits if language wasn't found
    ExitMSG(f'\033[1;31m /ᐠ - ˕ -マ Language or language code was not found.\033[00m\033[1m\n' + 
                   f'\n  \033[0m\033[3m* Did you mean "{languages[searchResult[1]][inDex]}" ?\033[0m\n ' +
                    "\n  Use the ISO language standard for names, or the ISO 639-1 for language codes. " + 
                    "\n  The list of ISO standards is available on: \n\033[00m" + 
                    "\n  \033[3mhttps://en.wikipedia.org/wiki/List_of_ISO_639_language_codes\033[00m")

# Main
def Main() -> None:
    # Defining variables used in most of main
    saveTranslation = usingOptions = False;
    search = []

    # Checks arguments
    if len(sys.argv) <= 1: Help();

    # Command line options
    for i, argument in enumerate(sys.argv[1:]):
        # Get options
        if argument[0] == '-' and len(argument) >= 2:
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
                case 'u':
                    # Looks for option arguments
                    if len(sys.argv) <= i + 2: MissingArgument('option argument')

                    properties = []
                    # Loops through option arguments
                    for optArg in sys.argv[i+2:]:
                        if optArg[0] == '-': break;

                        if optArg.find('=') != -1:
                            # Separates into list with propertyName and propertyArgument
                            prop = optArg.split('=')
                            # Checks if the propertyName matches any property available in propertyNames
                            
                            # Creates list with booleans depending 
                            # if the propertyName matches one of the strings in propertyNames,
                            # if no string matches the propertyName, then the propertyName inserted is invalid.
                            correctStr = False;
                            for k in list(map(lambda x: prop[0] == x, propertyNames)):
                                if k: correctStr = True;
                            if not correctStr: ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ Invalid config option name. Use -d to see options names.\033[00m")
                            
                            properties.append(prop)
                        else:
                            # Fast syntax using ':' (only insert arguments, separated by ':')
                            # Checks if argument syntax is correct
                            if optArg.find(':') == -1: ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ Incorrect syntax.\033[00m")

                            # If the string is empty, it's ignored
                            for i, arg in enumerate(optArg.split(':')):
                                if arg == '': continue;

                                # Add string to correponding property
                                properties.append([propertyNames[i], arg])
                    # Checks if languages are correct
                    for prop in properties:
                        if prop[0] == 'sourceLanguage' or prop[0] == 'translate': prop[1] = CheckLanguage(prop[1])

                    try:
                        # Updates config file 
                        with open('config.json', "r+") as file:
                            config = json.load(file)

                            # Writes all properties
                            config = SetProperties(properties, config);

                            file.seek(0)
                            json.dump(config, file)
                            file.truncate()
                    except:
                        # Creates config file if theres no config file
                        with open('config.json', 'w+') as file:
                            if len(properties) < 3: ExitMSG(' \033[1;31m( ｡ •`ᴖ´• ｡)\033[0m You need to set all config options: \033[3msourceLanguage, translate and domain.\033[0m')
                            
                            nullConfig = {"sourceLanguage": "", "translate": "", "domain": "", "fastTranslation": False}

                            print(f'\n \033[1;33m(๑•̀ㅂ•́)ง✧\033[00m The configuration was set successfully.')
                            config = SetProperties(properties, nullConfig);

                            json.dump(config, file); file.truncate();
                    
                    if (len(search) == 0): print(); exit()
                # Clears logs or saved logs
                case 'c':
                    section = ''
                    # Checks if theres no option argument (default to 'logs')
                    if len(sys.argv) <= i + 2 or sys.argv[i+2][0] == '-': section = 'logs'
                    else: 
                        # Checks if option argument is in logs or saved
                        possibleSections = ['logs', 'saved'];
                        for sec in possibleSections: 
                            if sys.argv[i+2] == sec: section = sec; break;

                        if section == '': ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ Invalid section name. The available sections are 'logs' and 'saved'.\033[00m")

                    ClearData(section);
                    ExitMSG(f" \033[1;34mᕙ( •̀ ᗜ •́ )ᕗ\033[0m  The section \033[3m'{section}'\033[0m was cleared.")
                # Toogle fast translation
                case 'f': ToogleFast();
                # Saves translation to be used later
                case 's': saveTranslation = True;
                # Default message
                case _: ExitMSG("\033[1;31m /ᐠ - ˕ -マ Invalid option. Use -h option for help. \033[00m")

        # Get all arguments before the first option (all text to be translated)
        if not usingOptions: search.append(argument);

    # If there's no search, creates new line and exit()
    if (len(search) == 0): print(); exit();

    # Get values from json file
    config = OpenJSON('config.json')

    sourceLang = config['sourceLanguage']
    transLang = config['translate']

    fastMode = config['fastTranslation']
    dotDomain = config['domain']

    # Checks if translations is saved or is in the logs (loads faster, no need to internet connection)
    logMatch = MatchData('logs',  search, sourceLang, transLang, fastMode);
    savMatch = MatchData('saved', search, sourceLang, transLang, fastMode);

    # Saves 'log' to 'saved' if saveTranslation is set to True, exits if the translation is matched
    if logMatch[0]: 
        if saveTranslation: WriteData('saved', Page(search[0], logMatch[1], sourceLang[1], transLang[1], fastMode))
        exit();

    if savMatch[0]: exit();

    translator = Translator(sourceLang, transLang, dotDomain, fastMode);
    lemmaInfos = translator.Translate(search);

    # Displays result
    translationPage = Page(search[0], lemmaInfos, sourceLang[1], transLang[1], fastMode);
    translationPage.Display();

    # Saves to log history
    WriteData('logs', translationPage);

    # Saves to saved section (-s option)
    if saveTranslation: WriteData('saved', translationPage);

if __name__ == "__main__":
    Main();