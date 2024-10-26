# Importing packages (pip)

from bs4 import BeautifulSoup; 
import requests; 
import lxml;

from Modules.Display.display import ExitMSG;
from Modules.Scrape.parser import GetInfo;
from Modules.Scrape.Scraper import Lemma;

# Custom exception
class StatusException(Exception):
    pass;

class Translator:
    def __init__(self, source: str, target: str, domain: str, fast: bool):
        self.source = source;
        self.target = target;
        self.domain = domain;
        self.fast = fast;
    
    # Connects to url and returns soup object
    def __SoupConnect(self, search) -> BeautifulSoup:
        # Changes target depending on fastMode
        urlParameters = f'qe={search[0]}&source=auto&cw=980&ch=919&as=shownOnStart' if self.fast else f'source=auto&query={search[0]}';

        # linguee url
        url = f'https://www.linguee{self.domain}/{self.source[0]}-{self.target[0]}/search?{urlParameters}'
        
        # Handle requests and errors
        try: 
            res = requests.get(url)

            if res.status_code != 200: raise StatusException(res.status_code)
        except requests.ConnectionError as error:
            ExitMSG(f'\033[1;31m (っ◞‸◟ c) An internet connection error ocurred.\033[0m')
        except requests.exceptions.RequestException as error:
            ExitMSG(f'\033[1;31m (っ◞‸◟ c) An error ocurred:\033[00m\n\n   {error}')
        except StatusException as error:
            print(f'\n \033[1;31m(－－ ; Exception\033[00m: Unexpected HTML status code: \033[1;35mCODE {error}\033[00m');
            if str(error) == '429': 
                print('\n \033[3;90mToo many requests. Try again later...\033[0m')
                if not fastMode: print(' \033[3;90mOr you can enable fast-translation by using the -f option. \033[00m')
            print();
            exit();
    
        return BeautifulSoup(res.text, 'lxml')

    def Translate(self, search: str) -> list[Lemma]:
        soup = self.__SoupConnect(search);

        return GetInfo(soup, self.fast);