from Modules.scrape import Description, Translation, Lemma;
from Modules.display import ExitMSG;

# Functions that parse html elements into scraping objects of the classes from scrape

def GetTransDescription(tag) -> Description:
    # Gets description from a translation class
    titleArr = tag.select('.translation_desc .dictLink')
    wordtypeArr = tag.select('.translation_desc .tag_type')
    
    return Description(titleArr[0].text, '' if len(wordtypeArr) <= 0 else wordtypeArr[0].text)

def GetTranslation(trans) -> Translation:
        # Gets text examples
        exampleTexts = trans.select('.example_lines > .example > .tag_e > span:not(.tag_e_end):not(.dash)')

        return Translation(GetTransDescription(trans), list(map(lambda l: l.text, exampleTexts)))

def GetLemma(lemma) -> Lemma:
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

# Getting lemmas for fast and normal mode

def __FastInfo(soup) -> list[Lemma]:
    # Gets "lemmas" (are called completion items in html)
    compItems = soup.select('.autocompletion_item');

    # Exits if doesnt find elements
    if len(compItems) <= 0: return;
    
    # Finds all "parents" of the translations
    lemmaInfos: list[Lemma] = [];
    for compItem in compItems:
        # Finds title and wordtype inside mainRow and creates description
        mainRowList = compItem.select('.main_row')
        if len(mainRowList) == 0:
            # Ignores empty items 
            if len(compItems) > 1: continue; 
            return;
        
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
    
    return lemmaInfos;

def __NormalInfo(soup) -> list[Lemma]:
    # Gets lemmas (chunks of text)
    lemmas = soup.select('.exact > .lemma:not(.singleline) > div');

    # If there's no titles, no results where found
    if len(lemmas) <= 0: return;

    # Stores lemmas
    return list(map(GetLemma, lemmas));

def GetInfo(soup, fastMode) -> list[Lemma]:
    lemmaList = __FastInfo(soup) if fastMode else __NormalInfo(soup);

    if not lemmaList: ExitMSG("\033[1;31m( ˶•ᴖ•) !! No results where found. \033[00m");

    return lemmaList;