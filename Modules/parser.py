from Modules.scrape import *;

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
