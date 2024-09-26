from bs4 import BeautifulSoup; import lxml;
import requests; 

import shelve;
import json;
import sys;

# Read-only
propertyNames = ['sourceLanguage', 'translate', 'domain', 'numberLogs']

# Important variables
search = []
saveTranslation = False
usingOptions = False

# Custom exception
class StatusException(Exception):
    pass;

# Classes for scraping

class Description:
    def __init__(self, title, wordtype):
        self.title = title;
        self.wordtype = wordtype;

    def Display(self, titleColor='\033[00m', wordtypeColor='\033[00m', atStart='', atEnd='\n'):
        wordTypeStr = f'{wordtypeColor}({self.wordtype})\033[00m' if self.wordtype != '' else ''
        print(f'{atStart}{titleColor}{self.title}\033[00m {wordTypeStr}', end=atEnd)

class Translation:
    def __init__(self, description, exampleTexts):
        self.description = description
        self.exampleTexts = exampleTexts
    
    def Display(self):
        self.description.Display('\033[0;37m', '\033[3;90m', '\n     ')

        for example in self.exampleTexts:
            print(f'       \033[0;34m{example.strip()}\033[00m')

    def Dict(self):
        return {
            'description': self.description.__dict__,
            'examples': self.exampleTexts
        }

class Lemma:
    def __init__(self, description, translations, lessCommons):
        self.description = description
        self.lessCommons = lessCommons
        self.translations = translations
    
    def Display(self, fastMode=False):
        self.description.Display('\033[1;32m', '\033[3;90m', '\n   ', '')

        for info in self.translations:
            info.Display()
        
        if len(self.lessCommons) <= 0: return
        
        print('\n     ', end='') if fastMode else print('\n   \033[3;32mLess common: \033[00m\n     ', end='');
        for i, lessCommon in enumerate(self.lessCommons):
            if i == len(self.lessCommons) - 1:
                lessCommon.Display('\033[0;37m', '\033[3;90m', '')
                continue;

            lessCommon.Display('\033[0;37m', '\033[3;90m', '', ' - ')

    def Dict(self):
        transDictArr = []
        for trans in self.translations:
            transDictArr.append(trans.Dict())

        lessCommonDictArr = []
        for lc in self.lessCommons:
            lessCommonDictArr.append(lc.__dict__)

        return {
            'description': self.description.__dict__,
            'translations': transDictArr,
            'lessCommons': lessCommonDictArr
        }

class Page:
    def __init__(self, search, lemmas, srcLanguage, trsLanguage, fastMode):
        self.search = search
        self.lemmas = lemmas
        self.srcLanguage = srcLanguage
        self.trsLanguage = trsLanguage
        self.fastMode = fastMode

    def Dict(self):
        lemmasDict = list(map(lambda l: l.Dict(), self.lemmas))

        return {
            "search": self.search,
            "lemmas": lemmasDict,
            "source": self.srcLanguage,
            "translated": self.trsLanguage,
            "fastMode": self.fastMode
        }

# Functions that transform html elements into scraping objects of the classes above

def GetTransDescription(tag):
    # Gets description from a translation class
    titleArr = tag.select('.translation_desc .dictLink')
    wordtypeArr = tag.select('.translation_desc .tag_type')
    
    return Description(titleArr[0].text, '' if len(wordtypeArr) <= 0 else wordtypeArr[0].text)

def GetTranslation(trans):
        # Gets text examples
        exampleTexts = trans.select('.example_lines > .example > .tag_e > span:not(.tag_e_end):not(.dash)')

        return Translation(GetTransDescription(trans), list(map(lambda l: l.text, exampleTexts)))

def GetLemma(lemma):
    # Creates descrition with title and wordtype search
    wordtype = lemma.select('h2 .tag_wordtype')
    description = Description(lemma.select('h2 .dictLink')[0].text, '' if len(wordtype) <= 0 else wordtype[0].text)

    # Gets less common translations
    lessCommons = lemma.select('.lemma_content .translation_group .translation')
    lessCommonInfo = list(map(GetTransDescription, lessCommons))

    # Gets common translations
    translations = lemma.select('.lemma_content .translation_lines > .translation')
    transInfos = list(map(GetTranslation, translations))

    # Add everything to array
    return Lemma(description, transInfos, lessCommonInfo)

# Final output
def Output(lemmas, mode):
    for lemma in lemmas:
        lemma.Display(mode);
    
    print();

# Connect to url
def SoupConnect(fastMode):
    # Changes target depending on fastMode
    urlParameters = f'qe={search[0]}&source=auto&cw=980&ch=919&as=shownOnStart' if fastMode else f'source=auto&query={search[0]}';

    # linguee url
    url = f'https://www.linguee{dotDomain}/{sourceLang[0]}-{transLang[0]}/search?{urlParameters}'
    
    # Handle requests and errors
    try: 
        res = requests.get(url)

        if res.status_code != 200: raise StatusException(res.status_code)
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

# Binary search
def BSearch(search, dicArray, dicParameter):
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
    
# Writing/Reading/Displaying files
def WriteData(section, page):
    with shelve.open('data.db', writeback=True) as dataFile:
        if not section in dataFile: dataFile[section] = []

        # TO-DO: Sort everything with indexes and alphabetical order (then you can do binary search, but still display it normally)
        bSearch = BSearch(page.search, dataFile[section], 'search')
        index = bSearch[1] if bSearch[0] else bSearch[1] + 1

        # Inserts element into data (now to array is ordered)
        dataFile[section].insert(bSearch[1], page.Dict());

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
        print(f"   {i + 1}.\033[0m {page['search']}{blankSpaces}\033[0m\033[2m|\033[0m\033[3m  {page['source']} - {page['translated']}  \033[0m\033[1m{'*' if page['fastMode'] else ''}\033[0m")

def MatchData(dataSection, search, sourceLang, transLang, fastMode):
    # TO-DO use binary search to find exact search
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

            # Displays and exits            
            Output(lemmas, page['fastMode']); exit();

def OpenJSON(fileName):
    with open(fileName, "r") as file:
        return json.load(file)

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

# Messages

def ExitMSG(message):
    print(f"\n {message}\n")
    exit()

def MissingArgument(customMessage='argument'):
    ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ No {customMessage} supplied.\033[00m")

def Help():
    print("\n \033[1mDescription\033[0m: A script that translates things directly from the terminal.")
    print("              (˶˃ ᵕ ˂˶) .ᐟ.ᐟ \n")
    print(" \033[1mSyntax\033[0m: trs yourwordhere [options]\n")
    print(" \033[1mOptions: \033[0m\n")
    print("  -l : Shows log of translations and saved translations.")
    print("  -s : Saves the translation to be used later.")
    print("  -d : Displays options from the config file")
    print("  -c : Changes config file options.")
    print("  -f : Toggles on/off fast mode.")
    print("  -h : Shows this help message.\n")
    print("\033[1mExtended Details:\033[0m\n")
    print(" -f :  Enables/Disables fast mode. Fast mode allows you to search when the linguee website responds with an \033[1;31mHTTP 429\033[0m error,")
    print("       but its translations are very limited, not containing examples.\n")
    print(" -c :  Option used to change the configuration of the script, ")
    print("       you can use two syntaxes for this option: ")
    print("         \033[1mSyntax 1\033[0m: \033[3mOPT1=ARG1 OPT2=ARG2 ...\033[0m ")
    print("\n            \033[3mExamples:\033[0m sourceLanguage=en translate=de\n")
    print("         \033[1mSyntax 2:\033[0m \033[3mARG1:ARG2:ARG3...\033[0m ")
    print("             In this syntax the options are in the order displayed using the -d option ")
    print('             Its necessary at least one \033[3m":"\033[0m to use this syntax')
    print("\n             \033[3mExamples:\033[0m en:pt:.com")
    print("                       pt:\n")
    exit()

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
            # Changes config file
            case 'c':
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
                        # if no string matches the propertyName, than the propertyName inserted is invalid.
                        correctStr = False
                        for k in list(map(lambda x: prop[0] == x, propertyNames)):
                            if k: correctStr = True
                        if not correctStr: ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ Incorrect config option name. Use -d to see options names.\033[00m")
                        
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
                    if prop[0] == 'sourceLanguage' or prop[0] == 'translate':
                        prop[1] = CheckLanguage(prop[1])

                # Updates config file
                with open('config.json', "r+") as file:
                    config = json.load(file)

                    # Writes all properties and displays changes
                    print(f'\n \033[1;33m(๑•̀ㅂ•́)ง✧\033[00m The following properties were changed: \n')
                    for i, prop in enumerate(properties): 
                        config[prop[0]] = prop[1]

                        argumentString = f'\033[3;37m"{prop[1][0]} ({prop[1][1]})"\033[00m.' if prop[0] == 'sourceLanguage' or prop[0] == 'translate' else f'\033[3;37m"{prop[1]}"\033[00m.';
                        print(f'   \033[1;37m{i + 1}.\033[00m\033[3;37m"{prop[0]}"\033[00m was changed to {argumentString}')

                    file.seek(0)
                    json.dump(config, file)
                    file.truncate()

                # If there's no search, creates new line and exit()
                if (len(search) == 0): print(); exit()
            # Display options from the configuration file
            case 'd':
                config = OpenJSON('config.json')
                print(f'\n \033[1m(˶ ˆ ꒳ˆ˵) \033[0m\033[1mDisplaying useful information:\033[00m\n')
                print(  f' \033[1;33msourceLanguage:\033[00m {config['sourceLanguage'][0]} \033[2m({config['sourceLanguage'][1]})\033[00m')
                print(  f' \033[1;33mtranslate:\033[00m {config['translate'][0]} \033[2m({config['translate'][1]})\033[00m\n')
                print(  f' \033[1;35mdomain:\033[00m {config['domain']}')
                print(  f' \033[1;35mnumberLogs:\033[00m {config['numberLogs']}\n')
                print(  f' \033[1m* Fast Mode:\033[00m {config['fastTranslation']}\n')

                exit()
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

                # If there's no search, creates new line and exit()
                if (len(search) == 0): print(); exit()
            # Default message
            case _: ExitMSG("\033[1;31m /ᐠ - ˕ -マ Invalid option. Use -h option for help. \033[00m")
    
    # Get all arguments before the first option (all text to be translated)
    if not usingOptions: search.append(argument);
    
# Get values from json file
config = OpenJSON('config.json')

sourceLang = config['sourceLanguage']
transLang = config['translate']

dotDomain = config['domain']
fastMode = config['fastTranslation']

# Translates full texts (more than 1 word)
if len(search) > 1:
    # Transforms array in string
    searchText = ''
    for i, word in enumerate(search): 
        fStr = f'{word} '
        if i == len(search) - 1: fStr = word;

        searchText += fStr
    
    deeplUrl = f'https://www.deepl.com/en/translator#{sourceLang[1]}/{transLang[1]}/{searchText}'

    soup = SoupConnect(deeplUrl)
    #[aria-labelledby]="translation-target-heading"
    textTranslation = soup.select('div')

    for div in textTranslation:
        print(div.text)
    exit()

# Checks if translations is saved or is in the logs (loads faster, no need to internet connection)
MatchData('saved', search, sourceLang, transLang, fastMode);
MatchData('logs',  search, sourceLang, transLang, fastMode);

# Gets linguee html 
soup = SoupConnect(fastMode)

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
        mainRow = compItem.select('.main_row')[0]

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