# Classes for scraping

class Description:
    def __init__(self, title, wordtype):
        self.title : str = title;
        self.wordtype : str = wordtype;

    def Display(self, titleColor='\033[00m', wordtypeColor='\033[00m', atStart='', atEnd='\n') -> None:
        wordTypeStr = f'{wordtypeColor}({self.wordtype})\033[00m' if self.wordtype != '' else ''
        print(f'{atStart}{titleColor}{self.title}\033[00m {wordTypeStr}', end=atEnd)

class Translation:
    def __init__(self, description, exampleTexts):
        self.description : Description = description
        self.exampleTexts : list[str] = exampleTexts
    
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
    def __init__(self, description, translations, lessCommons):
        self.description : Description = description
        self.lessCommons : list[Description] = lessCommons
        self.translations : list[Translation] = translations
    
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
    def __init__(self, search, lemmas, srcLanguage, trsLanguage, fastMode):
        self.srcLanguage : str = srcLanguage
        self.trsLanguage : str = trsLanguage
        self.search : str = search

        self.lemmas : list[Lemma] = lemmas
        self.fastMode : bool = fastMode

    def Dict(self) -> dict:
        lemmasDict = list(map(lambda l: l.Dict(), self.lemmas))

        return {
            "search": self.search,
            "lemmas": lemmasDict,
            "source": self.srcLanguage,
            "translated": self.trsLanguage,
            "fastMode": self.fastMode
        }
