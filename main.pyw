from bs4 import BeautifulSoup;
import requests;
import shelve;
import json;
import sys;

# Custom exception
class StatusException(Exception):
    pass

# Classes for scraping

class Description:
    def __init__(self, title, wordtype):
        self.title = title.text
        self.wordtype = wordtype.text if wordtype else ''

    def Display(self, titleColor='\033[00m', wordtypeColor='\033[00m', atStart='', atEnd='\n'):
        wordTypeStr = f'{wordtypeColor}({self.wordtype})\033[00m' if self.wordtype != '' else ''
        print(f'{atStart}{titleColor}{self.title}\033[00m {wordTypeStr}', end=atEnd)

class Translation:
    def __init__(self, description, exampleTexts):
        self.description = description
        self.exampleTexts = list(map(lambda l: l.text, exampleTexts))
    
    def Display(self):
        self.description.Display('\033[0;37m', '\033[3;90m', '\n   ')

        for example in self.exampleTexts:
            print(f'     \033[0;34m{example.strip()}\033[00m')

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
    
    def Display(self):
        self.description.Display('\033[1;32m', '\033[3;90m', '\n ', '')

        for info in self.translations:
            info.Display()
        
        if len(self.lessCommons) <= 0: return
        
        print('\n \033[3;32mLess common: \033[00m\n   ', end='')
        for i, lessCommon in enumerate(self.lessCommons):
            if i == len(self.lessCommons) - 1:
                lessCommon.Display('\033[0;37m', '\033[3;90m', '')
                continue

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
    def __init__(self, search, lemmas):
        self.search = search
        self.lemmas = lemmas

    def Dict(self):
        lemmasDict = []
        for lemma in self.lemmas:
            lemmasDict.append(lemma.Dict())

        return {
            "search": self.search,
            "lemmas": lemmasDict
        }

def GetTransDescription(tag):
    # Gets description from a translation class
    titleArr = tag.select('.translation_desc .dictLink')
    wordtypeArr = tag.select('.translation_desc .tag_type')
    
    return Description(titleArr[0], None if len(wordtypeArr) <= 0 else wordtypeArr[0])

# Messages

def ExitMSG(message):
    print(f"\n {message}\n")
    exit()

def MissingArgument(customMessage='argument'):
    ExitMSG(f"\033[1;31m ୧(๑•̀ᗝ•́)૭ No {customMessage} supplied.\033[00m")

def Help():
    print("\n Description: A script that translates things directly from the terminal.")
    print("              (˶˃ ᵕ ˂˶) .ᐟ.ᐟ \n")
    print(" Syntax: trs yourwordhere [options]\n")
    print(" Options: ")
    print("  -t                : Translates a chunck of text instead of a single word")
    print("  -s                : Saves the translation to be used later.")
    print("  -c lang:(src-dom) : Change the translated language.")
    print("  -C                : Displays configuration file.")
    print("  -l                : Shows log of translations.")
    print("  -h                : Shows this help message.\n")
    exit()

# Checks arguments
if len(sys.argv) <= 1:
    MissingArgument()

search = sys.argv[1]
saveTranslation = False

# Command line options
for i, argument in enumerate(sys.argv[1:]):
    # Get options
    if argument[0] == '-' and len(argument) >= 2: 
        match argument[1]:
            # Shows help message
            case 'h': Help()
            # Shows log of translations
            case 'l': ExitMSG('log')
            # Changes language
            case 'c':
                if len(sys.argv) <= i + 2: MissingArgument('language')
                newTransLang = sys.argv[i + 2].lower()

                with open('config.json', "r+") as file:
                    config = json.load(file)

                    config['translation_language'] = newTransLang
                    file.seek(0)
                    json.dump(config, file)
                    file.truncate()

                print(f'\n \033[1;33m(๑•̀ㅂ•́)ง✧\033[00m The language was changed to \033[1;00m{newTransLang}.\033[00m')

                if (search[0] == '-'): print(); exit()
            # Translates block of text
            case 't': print('text')
            # Saves translation to be used later
            case 's': saveTranslation = True;
            # Default message
            case _: ExitMSG("\n\033[1;31m /ᐠ - ˕ -マ Invalid option. Use -h option for help. \033[00m\n")

# Get values from json file
with open("config.json", "r") as file:
    config = json.load(file)

dotDomain = config['linguee_domain']
sourceLang = config['source_language']
transLang = config['translation_language']

# Gets linguee url 
url = f'https://www.linguee{dotDomain}/{sourceLang}-{transLang}/search?source=auto&query={search}'

# Handle requests and errors
try: 
    res = requests.get(url)

    if res.status_code != 200:
        raise StatusException(res.status_code)
except requests.exceptions.RequestException as error:
    print(f'\n\033[1;31m (っ◞‸◟ c) An error ocurred\033[00m: ERROR {error}\n')
    exit()
except StatusException as error:
    print(f'\n \033[1;31m(－－ ; Exception\033[00m: Unexpected HTML status code: \033[1;35mCODE {error}\033[00m')
    if str(error) == '429': print('\n \033[3;90mToo many requests. Try again later...\033[00m')
    print()
    exit()

soup = BeautifulSoup(res.text, 'lxml')

# Gets lemmas (chunks of text)
lemmas = soup.select('.exact > .lemma:not(.singleline) > div')

 # If there's no titles, no results where found
if len(lemmas) <= 0:
    ExitMSG("\033[1;31m( ˶•ᴖ•) !! No results where found. \033[00m")

# Stores lemmas
lemmaInfos = []
for lemma in lemmas:
    # Creates descrition with title and wordtype search
    description = Description(lemma.select('h2 .dictLink')[0], lemma.select('h2 .tag_wordtype')[0])

    # Gets less common translations
    lessCommons = lemma.select('.lemma_content .translation_group .translation')
    lessCommonInfo = []
    for lessCommon in lessCommons:
        lessCommonInfo.append(GetTransDescription(lessCommon))

    # Gets common translations
    translations = lemma.select('.lemma_content .translation_lines > .translation')
    transInfos = []
    for trans in translations:
        # Gets text examples
        exampleTexts = trans.select('.example_lines > .example > .tag_e > span:not(.tag_e_end):not(.dash)')

        transInfos.append(Translation(GetTransDescription(trans), exampleTexts))

    # Add everything to array
    lemmaInfos.append(Lemma(description, transInfos, lessCommonInfo))

# Displays result
for info in lemmaInfos:
    info.Display()

print()

# Saves to log history
with shelve.open('data.db', writeback=True) as dataFile:
    # Doesnt append to database, it is overwriting it
    dataFile['logs'] = []
    dataFile['logs'].append(Page(search, lemmaInfos).Dict())

    dataFile.sync()
    print(dataFile['logs'])