# Importing packages (pip)

from bs4 import BeautifulSoup; 
import requests; 
import lxml;

# Importing packages (standard)

import shelve;
import json;
import sys;

# Importing modules (local)

from Modules.scrape import *;
from Modules.parser import *;
from Modules.messages import *;

# Read-only
propertyNames = ['sourceLanguage', 'translate', 'domain']

# Custom exception
class StatusException(Exception):
    pass;

# Connects to url
def SoupConnect(fastMode, search, sourceLang, transLang, dotDomain):
    # Changes target depending on fastMode
    urlParameters = f'qe={search[0]}&source=auto&cw=980&ch=919&as=shownOnStart' if fastMode else f'source=auto&query={search[0]}';

    # linguee url
    url = f'https://www.linguee{dotDomain}/{sourceLang[0]}-{transLang[0]}/search?{urlParameters}'
    
    # Handle requests and errors
    try: 
        res = requests.get(url)

        if res.status_code != 200: raise StatusException(res.status_code)
    except requests.ConnectionError as error:
        ExitMSG(f'\033[1;31m (っ◞‸◟ c) An internet connection error ocurred.\033[0m')
    except requests.exceptions.RequestException as error:
        ExitMSG(f'\033[1;31m (っ◞‸◟ c) An error ocurred:\033[00m\n\n   {error}')
    except StatusException as error:
        print(f'\n \033[1;31m(－－ ; Exception\033[00m: Unexpected HTML status code: \033[1;35mCODE {error}\033[00m')
        if str(error) == '429': 
            print('\n \033[3;90mToo many requests. Try again later...\033[0m')
            if not fastMode: print(' \033[3;90mOr you can enable fast-translation by using the -f option. \033[00m')
        print()
        exit()
    
    return BeautifulSoup(res.text, 'lxml')

# Used by others

def BSearch(search, dicArray, dicParameter):
    # Binary search

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

def SetProperties(properties, currentConfig):
    temp = currentConfig;
    for i, prop in enumerate(properties): 
        temp[prop[0]] = prop[1]
    
    return temp;

# Final output
def Output(lemmas, mode):
    for lemma in lemmas:
        lemma.Display(mode);
    
    print();

# Writing/Reading/Displaying files
def WriteData(section, page):
    with shelve.open('data.db', writeback=True) as dataFile:
        if not section in dataFile: dataFile[section] = []

        # Inserts element into data
        dataFile[section].append(page.Dict());

def GetData(section):
    with shelve.open('data.db') as dataFile:
        if not section in dataFile: return [];

        return dataFile[section];

def DisplayData(section):
    searchList = GetData(section)
    if len(searchList) <= 0: print(f'\n \033[1;35m°՞(ᗒᗣᗕ)՞° You have no information in "{section}".\033[0m'); return;

    print(f'\n \033[1;35m(≧∇≦) Displaying your "{section}":\033[00m\n')

    # Gets every page dictionary in logs and displays information about that page
    for i, page in enumerate(searchList):
        # Makes slashes align after 20 chars, unless the search word has more than 20 chars. (min 2 blank spaces)
        blankSpaces = ' ' * (max(0, 20 - len(page['search'])) + 2)
        print(f"   \033[2m{(i + 1):03d} |\033[0m {page['search']}{blankSpaces}\033[2m|\033[0m\033[2m  {page['source']} - {page['translated']}  {'*' if page['fastMode'] else ''}\033[0m")

def MatchData(dataSection, search, sourceLang, transLang, fastMode):
    for page in GetData(dataSection):
        if page['search'] == search[0] and page['source'] == sourceLang[1] and page['translated'] == transLang[1] and page['fastMode'] == fastMode:
            # Transforms json into lemmas array to be displayed:

            search = page['search']
            source = page['source']
            translated = page['translated']

            # Creates lemmas with dictionary values
            lemmas = []
            for lemma in page['lemmas']:
                curDesc = Description(lemma['description']['title'], lemma['description']['wordtype'])
                
                translations = []
                for trans in lemma['translations']:
                    transDesc = Description(trans['description']['title'], trans['description']['wordtype'])
                    exampleTexts = trans['examples']
                    translations.append(Translation(transDesc, exampleTexts))

                lessCommons = []
                for lc in lemma['lessCommons']:
                    lessCommons.append(Description(lc['title'], lc['wordtype']))

                lemmas.append(Lemma(curDesc, translations, lessCommons))

            # Displays and returns true
            Output(lemmas, page['fastMode'])
            return (True, lemmas)
    
    return (False, [])

def OpenJSON(fileName):
    try: 
        with open(fileName, "r") as file:
            return json.load(file);
    except:
        print('\n \033[1;35m(˶˃⤙˂˶)\033[0m To start translating, update the translation');
        print('         config using \033[1mkdi -u \033[0m.')
        ExitMSG('        \033[1mExample:\033[0m \033[3mkdi -u en:fr:.com\033[0m')

# Receives language or language code, checks if it exists and returns the correct language with its iso639 language code.
def CheckLanguage(language):
    langFile = OpenJSON('languages.json')

    # * inDex is the index inside a specific language (0: language name, 1: language code)

    # Checks if the user inserted an abbreviation or 
    # a language name and changes inDex and languages variables accordingly
    if len(language) == 2:
        languages = langFile['sortedCodes']
        inDex = 1
    else:
        languages = langFile['sortedLanguages']
        inDex = 0;

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
    search = []
    saveTranslation = False
    usingOptions = False

    # Checks arguments
    if len(sys.argv) <= 1: Help()

    # Command line options
    for i, argument in enumerate(sys.argv[1:]):
        # Get options
        if argument[0] == '-' and len(argument) >= 2:
            usingOptions = True
            match argument[1]:
                # Shows help message
                case 'h': Help()
                # Shows log of translations
                case 'l': 
                    DisplayData('logs'); DisplayData('saved');
                    print('\n\033[1m * :\033[0m Searched with \033[1mfastmode\033[0m\n'); exit();
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
                            correctStr = False
                            for k in list(map(lambda x: prop[0] == x, propertyNames)):
                                if k: correctStr = True
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

                            # Writes all properties and displays changes
                            config = SetProperties(properties, config);

                            file.seek(0)
                            json.dump(config, file)
                            file.truncate()
                    except:
                        # Creates config file if theres no config file
                        with open('config.json', 'w+') as file:
                            if len(properties) < 3: ExitMSG(' \033[1;31m( ｡ •`ᴖ´• ｡)\033[0m You need to set all config options: \033[3msourceLanguage, translate and domain.\033[0m')
                            
                            nullConfig = {"sourceLanguage": "", "translate": "", "domain": "", "fastTranslation": False}

                            print(f'\n \033[1;33m(๑•̀ㅂ•́)ง✧\033[00m The configuration was set successfully:')
                            config = SetProperties(properties, nullConfig);

                            json.dump(config, file); file.truncate();
                    
                    if (len(search) == 0): print(); exit()
                # Display options from the configuration file
                case 'i':
                    config = OpenJSON('config.json')
                    print(f'\n \033[1m(˶ ˆ ꒳ˆ˵) \033[0m\033[1mDisplaying useful information:\033[00m\n')
                    print(  f' \033[1;33msourceLanguage:\033[00m {config['sourceLanguage'][0]} \033[2m({config['sourceLanguage'][1]})\033[00m')
                    print(  f' \033[1;33mtranslate:\033[00m {config['translate'][0]} \033[2m({config['translate'][1]})\033[00m\n')
                    print(  f' \033[1;35mdomain:\033[00m {config['domain']}')
                    print(f'\n \033[1m* Fast Mode:\033[00m {config['fastTranslation']}\n')

                    exit()
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

                    with shelve.open('data.db') as dataFile: dataFile[section] = []
                    ExitMSG(f" \033[1;34mᕙ( •̀ ᗜ •́ )ᕗ\033[0m  The section \033[3m'{section}'\033[0m was cleared.")
                # Saves translation to be used later
                case 's': saveTranslation = True;
                # Toogle fast translation
                case 'f': 
                    with open('config.json', "r+") as file:
                        config = json.load(file)

                        # Toogle fast translation (True / False)
                        config['fastTranslation'] = not config['fastTranslation']
                        print(f' \n\033[1;33m⎚⩊⎚ -✧\033[0m  Fast translation was set to \033[1m{config["fastTranslation"]}\033[0m.')
                        
                        file.seek(0)
                        json.dump(config, file)
                        file.truncate()
                # Default message
                case _: ExitMSG("\033[1;31m /ᐠ - ˕ -マ Invalid option. Use -h option for help. \033[00m")

        # Get all arguments before the first option (all text to be translated)
        if not usingOptions: search.append(argument);

    # If there's no search, creates new line and exit()
    if (len(search) == 0): print(); exit()

    # Get values from json file
    config = OpenJSON('config.json')

    sourceLang = config['sourceLanguage']
    transLang = config['translate']

    dotDomain = config['domain']
    fastMode = config['fastTranslation']

    # Checks if translations is saved or is in the logs (loads faster, no need to internet connection)
    logMatch = MatchData('logs',  search, sourceLang, transLang, fastMode);
    savMatch = MatchData('saved', search, sourceLang, transLang, fastMode);

    # Saves 'log' to 'saved' if saveTranslation is set to True, exits if the translation is matched
    if logMatch[0]: 
        if saveTranslation: WriteData('saved', Page(search[0], logMatch[1], sourceLang[1], transLang[1], fastMode))
        exit();

    if savMatch[0]: exit();

    # Gets linguee html 
    soup = SoupConnect(fastMode, search, sourceLang, transLang, dotDomain);

    # Initialize lemmas
    lemmaInfos = []

    if fastMode: 
        # Gets "lemmas" (are called completion items in html)
        compItems = soup.select('.autocompletion_item');

        # Exits if doesnt find elements
        if len(compItems) <= 0:
            ExitMSG("\033[1;31m( ˶•ᴖ•) !! No results where found. \033[00m")
        
        # Finds all "parents" of the translations
        for compItem in compItems:
            # Finds title and wordtype inside mainRow and creates description
            mainRowList = compItem.select('.main_row')
            if len(mainRowList) == 0: continue;
            
            mainRow = mainRowList[0];

            mainTitle = mainRow.select('.main_item')[0]
            mainType = mainRow.select('.main_wordtype')

            mainDescription = Description(mainTitle.text, '' if len(mainType) <= 0 else mainType[0].text)

            # Finds all translations of the compItem
            transRow = compItem.select('.translation_row')[0]
            transItems = transRow.select('.translation_item')
        
            # Gets all translations from the "parent" (compItem)
            translations = []
            for item in transItems:
                # Gets text and filters it into array with title and wordtype of translation
                itemArr = item.text.replace('\r', '').replace('·', '').split('\n')

                # Creates a description from tags and appends it to translations array.
                translations.append(Description(itemArr[1].strip(), itemArr[2].strip()))

            # Uses translations as less commons (because they are just descriptions), creates lemma and appends it to lemmaInfos to be displayed and saved
            lemmaInfos.append(Lemma(mainDescription, [], translations))
    else:
        # Gets lemmas (chunks of text)
        lemmas = soup.select('.exact > .lemma:not(.singleline) > div')

        # If there's no titles, no results where found
        if len(lemmas) <= 0:
            ExitMSG("\033[1;31m( ˶•ᴖ•) !! No results where found. \033[00m")

        # Stores lemmas
        lemmaInfos = list(map(GetLemma, lemmas))

    # Displays result
    Output(lemmaInfos, fastMode)

    # Saves to log history
    WriteData('logs', Page(search[0], lemmaInfos, sourceLang[1], transLang[1], fastMode))

    # Saves to saved section (-s option)
    if saveTranslation: WriteData('saved', Page(search[0], lemmaInfos, sourceLang[1], transLang[1], fastMode))

if __name__ == "__main__":
    Main();