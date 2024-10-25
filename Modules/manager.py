import shelve;
import json;

from Modules.scrape import Description, Translation, Lemma, Page;
from Modules.display import ExitMSG;

# Manages Writing/Reading/Getting files

# > shelve data manager

# Writes full page search in a section
def WriteData(section: str, page: Page) -> None:
    with shelve.open('data.db', writeback=True) as dataFile:
        if not section in dataFile: dataFile[section] = []

        # Inserts element into data
        dataFile[section].append(page.Dict());

# Gets data from a section
def GetData(section: str) -> list[Page]:
    with shelve.open('data.db') as dataFile:
        if not section in dataFile: return [];

        return dataFile[section];

# Checks if any data in logs or saved matches the current search
def MatchData(dataSection: str, search: list[str], sourceLang: list[str], transLang: list[str], fastMode: bool) -> (bool, list[Lemma]):
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
            Page(search, lemmas, sourceLang, transLang, fastMode).Display();
            return (True, lemmas)
    
    return (False, [])

def ClearData(section: str) -> None:
    with shelve.open('data.db') as dataFile: dataFile[section] = [];

# > config file manager

def OpenJSON(fileName) -> dict:
    try: 
        with open(fileName, "r") as file:
            return json.load(file);
    except:
        print('\n \033[1;35m(˶˃⤙˂˶)\033[0m To start translating, update the translation');
        print('         config using \033[1mkdi -u \033[0m.')
        ExitMSG('        \033[1mExample:\033[0m \033[3mkdi -u en:fr:.com\033[0m')

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

def DisplayData(section: str) -> None:
    searchList = GetData(section)
    if len(searchList) <= 0: print(f'\n \033[1;35m°՞(ᗒᗣᗕ)՞° You have no information in "{section}".\033[0m'); return;

    print(f'\n \033[1;35m(≧∇≦) Displaying your "{section}":\033[00m\n')

    # Gets every page dictionary in logs and displays information about that page
    for i, page in enumerate(searchList):
        # Makes slashes align after 20 chars, unless the search word has more than 20 chars. (min 2 blank spaces)
        blankSpaces = ' ' * (max(0, 20 - len(page['search'])) + 2)
        print(f"   \033[2m{(i + 1):03d} |\033[0m {page['search']}{blankSpaces}\033[2m|\033[0m\033[2m  {page['source']} - {page['translated']}  {'*' if page['fastMode'] else ''}\033[0m")