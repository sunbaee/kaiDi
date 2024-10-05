# kaiDi

kaiDi is a **terminal translator/dictionary** made in python.
It scrapes the [linguee website](https://www.linguee.com/) to get its translations and 
translates in the same way you'd translate using the website directly, but from the terminal instead. 

It has some extra functions such as: 
  1. Allowing you to **change the linguee domain** with ease if you want to translate from another language perspective.
  2. **Saving translations** to acess them faster (not needing internet connection).
  3. A **fast mode** that shows some suggestions with the translation.

<br>_The version of python used was python 3.12_.

## Preview

https://github.com/user-attachments/assets/bd772dbe-65d4-4c0c-88d0-4b348d18df56

## Usability

You can run the program using the following terminal command when inside the kaiDi folder.
```bash
python main.pyw {translation}
```

_Use the word you want to translate instead of {translation} in the command above._

## Installation

1. Open the terminal and clone this repository using the following command:
```bash
git clone https://github.com/sunbaee/kaiDi.git
```
2. Enter the directory named kaiDi.

3. Install the necessary dependencies using the following command:

```bash
pip install lxml bs4 requests
```

If everything went right, you should be able to use the program!

## Configuration

The first time you try to translate something, you'll be prompted to set the configuration file.
You can use the -u option to update the configuration file:
```bash
python main.pyw -u {sourceLanguage}:{targetLanguage}:{lingueeDomain}
```
_Use your preferred options instead of the words that are in brackets {}._

<br>Here's a configuration example for **english-french** translation:
```bash
python main.pyw -u english:french:.com
```
_Note: its possible to use the full language name, but its also possible to use any ISO639 language code for the languages._

<br> _For example: **en for english** and **fr for french**._

