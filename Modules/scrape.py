# Classes for scraping

class Description:
    def __init__(self, title: str, wordtype: str):
        self.title = title;
        self.wordtype = wordtype;

    def Display(self, titleColor='\033[00m', wordtypeColor='\033[00m', atStart='', atEnd='\n') -> None:
        wordTypeStr = f'{wordtypeColor}({self.wordtype})\033[00m' if self.wordtype != '' else ''
        print(f'{atStart}{titleColor}{self.title}\033[00m {wordTypeStr}', end=atEnd)

class Translation:
    def __init__(self, description: Description, exampleTexts: list[str]):
        self.description = description
        self.exampleTexts = exampleTexts
    
    def Display(self) -> None:
        self.description.Display('\033[0;37m', '\033[3;90m', '\n     ')

        for example in self.exampleTexts:
            print(f'       \033[0;34m{example.strip()}\033[00m')

    def Dict(self) -> dict:
        return {
            'description': self.description.__dict__,
            'examples': self.exampleTexts
        }

class Lemma:
    def __init__(self, description: Description, translations: list[Translation], lessCommons: list[Description]):
        self.translations  = translations
        self.description  = description
        self.lessCommons = lessCommons
    
    def Display(self, fastMode=False) -> None:
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

    def Dict(self) -> dict:
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
    def __init__(self, search: str, lemmas: list[Lemma], srcLanguage: str, trsLanguage: str, fastMode: bool):
        self.srcLanguage = srcLanguage
        self.trsLanguage = trsLanguage
        self.search  = search

        self.lemmas  = lemmas
        self.fastMode  = fastMode

    def Dict(self) -> dict:
        lemmasDict = list(map(lambda l: l.Dict(), self.lemmas))

        return {
            "search": self.search,
            "lemmas": lemmasDict,
            "source": self.srcLanguage,
            "translated": self.trsLanguage,
            "fastMode": self.fastMode
        }
