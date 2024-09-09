from bs4 import BeautifulSoup;
import requests;
import sys;

class StatusException(Exception):
    pass

class Description:
    def __init__(self, title, wordtype):
        self.title = title.text
        self.wordtype = wordtype

    def Display(self, titleColor='\033[00m', wordtypeColor='\033[00m', atStart='', atEnd='\n'):
        wordTypeStr = f'{wordtypeColor}({self.wordtype.text})\033[00m' if self.wordtype else ''
        print(f'{atStart}{titleColor}{self.title}\033[00m {wordTypeStr}', end=atEnd)

class Translation:
    def __init__(self, description, exampleTexts):
        self.description = description
        self.exampleTexts = exampleTexts
    
    def Display(self):
        self.description.Display('\033[0;37m', '\033[3;90m', '\n   ')

        for example in self.exampleTexts:
            print(f'     \033[0;34m{example.text.strip()}')

class Lemma:
    def __init__(self, description, transInfos, lessCommons):
        self.description = description
        self.lessCommons = lessCommons
        self.transInfos = transInfos
    
    def Display(self):
        self.description.Display('\033[1;32m', '\033[3;90m', '\n ', '')

        for info in self.transInfos:
            info.Display()
        
        if len(self.lessCommons) <= 0: return
        
        print('\n \033[3;32mLess common: \033[00m\n   ', end='')
        for i, lessCommon in enumerate(self.lessCommons):
            if i == len(self.lessCommons) - 1:
                lessCommon.Display('\033[0;37m', '\033[3;90m', '')
                continue

            lessCommon.Display('\033[0;37m', '\033[3;90m', '', ' - ')

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
        raise StatusException(res.status_code)
except requests.exceptions.RequestException as error:
    print(f'\n\033[1;31m (っ◞‸◟ c) An error ocurred\033[00m: ERROR {error}\n')
    exit()
except StatusException as error:
    print(f'\n \033[1;31m(－－ ; Exception\033[00m: Unexpected HTML status code: \033[1;35mCODE {error}\033[00m')
    if error == 429: print('\n \033[3;90mToo many requests. Try again later...')
    print()
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
        exampleTexts = trans.select('.example_lines > .example > .tag_e > span:not(.tag_e_end):not(.dash)')

        transInfos.append(Translation(GetTransDescription(trans), exampleTexts))

    # Add everything to array
    lemmaInfos.append(Lemma(description, transInfos, lessCommonInfo))

for info in lemmaInfos:
    info.Display()

print()
