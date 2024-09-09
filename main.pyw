from bs4 import BeautifulSoup;
import requests;
import sys;

class StatusException(Exception):
    pass

class Description:
    def __init__(self, title, wordtype):
        self.title = title.text
        self.wordtype = wordtype

    def Display(self, titleColor='\033[00m', wordtypeColor='\033[00m'):
        wordTypeStr = f'{wordtypeColor}({self.wordtype.text})\033[00m' if self.wordtype else ''
        print(f'   {titleColor}{self.title}\033[00m {wordTypeStr}')

class Translation:
    def __init__(self, description, exampleTexts):
        self.description = description
        self.exampleTexts = exampleTexts
    
    def Display(self):
        self.description.Display('\033[1;90m', '\033[2;37m')

        for example in self.exampleTexts:
            print(f'     \033[1;34m{example.text}')

class Lemma:
    def __init__(self, description, transInfos, lessCommons):
        self.description = description
        self.lessCommons = lessCommons
        self.transInfos = transInfos
    
    def Display(self):
        self.description.Display('\033[2;96m', '\033[1;37m')

        for info in self.transInfos:
            info.Display()
        
        if len(self.lessCommons) <= 0: return
        
        print('\033[2;36mLess common: \033[00m')
        for lessCommon in self.lessCommons:
            lessCommon.Display()

def GetTransDescription(tag):
    # Gets description from a translation class
    titleArr = tag.select('.translation_desc .dictLink')
    wordtypeArr = tag.select('.translation_desc .tag_type')
    
    return Description(titleArr[0], None if len(wordtypeArr) <= 0 else wordtypeArr[0])

fromLang = "english"
toLang = "portuguese"

# Gets linguee url 
url = f'https://www.linguee.com/{fromLang}-{toLang}/search?source=auto&query={sys.argv[1]}'

# Handle requests and errors
try: 
    res = requests.get(url)

    if res.status_code != 200:
        raise StatusException(f"Unexpected HTML status code: CODE \033[1;35m{str(res.status_code)}\033[00m")
except requests.exceptions.RequestException as error:
    print(f'\033[1;31m (っ◞‸◟ c) An error ocurred\033[00m: ERROR {error}')
    exit()
except StatusException as error:
    print(f'\033[1;31m ( ꩜ ᯅ ꩜) Exception\033[00m: {error}')
    exit()

soup = BeautifulSoup(res.text, 'lxml')

# Gets lemmas (chunks of text)
lemmas = soup.select('.exact > .lemma:not(.singleline) > div')

 # If there's no titles, no results where found
if len(lemmas) <= 0:
    print("\033[1;31m No results where found. \033[00m")
    exit()

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
        exampleTexts = trans.select('.example_lines > .example > .tag_e > span:not(.tag_e_end)')

        transInfos.append(Translation(GetTransDescription(trans), exampleTexts))

    # Add everything to array
    lemmaInfos.append(Lemma(description, transInfos, lessCommonInfo))

for info in lemmaInfos:
    info.Display()
