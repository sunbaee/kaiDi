# Matcher class for managers
class Matcher:
    # Binary search
    @staticmethod
    def __BSearch(search, dicArray, dicParameter) -> (bool, int):
        # Starting variables
        start = 0
        middle = 0
        end = len(dicArray) - 1

        while start <= end:
            middle = (start + end) // 2

            # Gets the search in the position between start and end
            curString = dicArray[middle][dicParameter]

            if curString > search:
                end = middle - 1; continue;
            if curString  < search:
                start = middle + 1; continue;
            
            # Returns exact match of value
            return (True, middle);

        # Returns nearest found value
        return (False, middle);
    
    # Receives language or language code, checks if it exists and returns the correct language with its iso639 language code.
    @staticmethod
    def CheckLanguage(language: str, langFile: dict) -> list[str]:
        # * inDex is the index inside a specific language (0: language name, 1: language code)

        # Checks if the user inserted an abbreviation or 
        # a language name and changes inDex and languages variables accordingly
        if len(language) == 2:
            languages = langFile['sortedCodes']; inDex = 1
        else:
            languages = langFile['sortedLanguages']; inDex = 0;

        # Binary search to find if the language is in the languages.json file
        searchResult = Matcher.__BSearch(language, languages, inDex);
        if searchResult[0]: return languages[searchResult[1]]

        # Exits if language wasn't found
        ExitMSG(f'\033[1;31m /ᐠ - ˕ -マ Language or language code was not found.\033[00m\033[1m\n' + 
                        f'\n  \033[0m\033[3m* Did you mean "{languages[searchResult[1]][inDex]}" ?\033[0m\n ' +
                        "\n  Use the ISO language standard for names, or the ISO 639-1 for language codes. " + 
                        "\n  The list of ISO standards is available on: \n\033[00m" + 
                        "\n  \033[3mhttps://en.wikipedia.org/wiki/List_of_ISO_639_language_codes\033[00m")
