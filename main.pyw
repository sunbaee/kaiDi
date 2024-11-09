# Importing packages (standard)
import sys;

# Importing modules (local)
from Modules.Managers.Data.data import WriteData, MatchData;
from Modules.Managers.Config.config import OpenJSON;
from Modules.Display.display import Help, ExitMSG;

from Modules.Verifier import CheckArguments;
from Modules.Translator import Translator;
from Modules.Scrape.Scraper import Page;

# Main
def Main() -> None:
    # Checks arguments
    if len(sys.argv) <= 1: Help();

    # Interpreting arguments
    res = CheckArguments(sys.argv[1:]);
    saveTranslation = res.saveTranslation;
    search = res.search;

    # If there's no search, creates new line and exit()
    if (len(search) == 0): print(); exit();

    # Get values from json file
    config = OpenJSON('Data/config.json')

    sourceLang = config['sourceLanguage']
    transLang = config['translate']

    fastMode = config['fastTranslation']
    dotDomain = config['domain']

    # Checks if translations is saved or is in the logs (loads faster, no need to internet connection)
    logMatch = MatchData('logs',  search, sourceLang, transLang, fastMode);
    savMatch = MatchData('saved', search, sourceLang, transLang, fastMode);

    # Saves 'log' to 'saved' if saveTranslation is set to True, exits if the translation is matched
    if logMatch[0]: 
        if saveTranslation: WriteData('saved', Page(search[0], logMatch[1], sourceLang[1], transLang[1], fastMode))
        exit();

    if savMatch[0]: exit();

    translator = Translator(sourceLang, transLang, dotDomain, fastMode);
    lemmaInfos = translator.Translate(search);

    page = Page(search[0], lemmaInfos, sourceLang[1], transLang[1], fastMode);
    
    # Displays result
    page.Display();

    # Saves to log history
    WriteData('logs', page);

    # Saves to saved section (-s option)
    if saveTranslation: WriteData('saved', page);

if __name__ == "__main__":
    Main();