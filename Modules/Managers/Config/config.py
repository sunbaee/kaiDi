import json;

from Modules.Display.display import ExitMSG, MissingArgument;
from Modules.Managers.Config.Matcher import Matcher;

def SetProperties(properties: list[list[str]], currentConfig: dict) -> dict:
    temp = currentConfig;
    for prop in properties: 
        temp[prop[0]] = prop[1]
    
    return temp;

def OpenJSON(fileName) -> dict:
    try: 
        with open(fileName, "r") as file:
            return json.load(file);
    except:
        print('\n \033[1;35m(˶˃⤙˂˶)\033[0m To start translating, update the translation');
        print('         config using \033[1mkdi -u \033[0m.')
        ExitMSG('        \033[1mExample:\033[0m \033[3mkdi -u en:fr:.com\033[0m')

# Read-only
propertyNames = ['sourceLanguage', 'translate', 'domain']

def UpdateConfig(args, currentIndex, search):
    # Looks for option arguments
    if len(args) <= currentIndex + 1: MissingArgument('option argument')

    properties = [];
    # Loops through option arguments
    for optArg in args[currentIndex + 1:]:
        if optArg[0] == '-': break;

        if optArg.find('=') != -1:
            # Separates into list with propertyName and propertyArgument
            prop = optArg.split('=');

            # Checks if the propertyName matches any property available in propertyNames
            correctStr = False;
            for k in list(map(lambda x: prop[0] == x, propertyNames)):
                if k: correctStr = True;
            
            if not correctStr: ExitMSG("\033[1;31m ୧(๑•̀ᗝ•́)૭ Invalid config option name. Use -i to see options names.\033[00m");
            
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
        if prop[0] == 'sourceLanguage' or prop[0] == 'translate': prop[1] = Matcher.CheckLanguage(prop[1], OpenJSON('languages.json'));

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
        # Checks if all properties are set
        if len(properties) < 3: ExitMSG(' \033[1;31m( ｡ •`ᴖ´• ｡)\033[0m You need to set all config options: \033[3msourceLanguage, translate and domain.\033[0m')

        # Creates config file if there's no config file
        with open('config.json', 'w+') as file:
            nullConfig = {"sourceLanguage": "", "translate": "", "domain": "", "fastTranslation": False}

            print(f'\n \033[1;33m(๑•̀ㅂ•́)ง✧\033[00m The configuration was set successfully.')
            config = SetProperties(properties, nullConfig);

            json.dump(config, file); file.truncate();
    
    if (len(search) == 0): print(); exit()

# Toogles fast translation
def ToogleFast() -> None:
    with open('config.json', "r+") as file:
        config = json.load(file)

        # Toogle fast translation (True / False)
        config['fastTranslation'] = not config['fastTranslation']
        
        file.seek(0)
        json.dump(config, file)
        file.truncate()

def DisplayConfig() -> None:
    config = OpenJSON('config.json')
    print(f'\n \033[1m(˶ ˆ ꒳ˆ˵) \033[0m\033[1mDisplaying useful information:\033[00m\n')
    print(  f' \033[1;33msourceLanguage:\033[00m {config['sourceLanguage'][0]} \033[2m({config['sourceLanguage'][1]})\033[00m')
    print(  f' \033[1;33mtranslate:\033[00m {config['translate'][0]} \033[2m({config['translate'][1]})\033[00m\n')
    print(  f' \033[1;35mdomain:\033[00m {config['domain']}')
    print(f'\n \033[1m* Fast Mode:\033[00m {config['fastTranslation']}\n')

    exit();