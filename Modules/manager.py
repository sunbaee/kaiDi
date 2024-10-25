import shelve;
import json;

from Modules.scrape import Description, Translation, Lemma, Page;
from Modules.message import ExitMSG;

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