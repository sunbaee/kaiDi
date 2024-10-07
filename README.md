# kaiDi

kaiDi is a **terminal translator/dictionary** made in python.
It scrapes the [linguee website](https://www.linguee.com/) to get its translations and 
translates in the same way you'd translate using the website directly, but from the terminal instead. 

It has some extra functions such as: 
  1. Allowing you to **change the linguee domain** with ease if you want to translate from another language perspective.
  2. **Saving translations** to acess them faster (not needing internet connection).
  3. A **fast mode** that shows some suggestions with the translation.

_The version of python used was python 3.12._

<div align="right">

[Preview](#preview)
[Usability](#usability)
[Installation](#installation)
[Configuration](#configuration)  

</div>

---

## Preview

https://github.com/user-attachments/assets/bd772dbe-65d4-4c0c-88d0-4b348d18df56

## Usability

Here are some of the ways you can use the program in the terminal:
  ```sh
  kdi translation       # translates "translation" according to your configuration.
  
  kdi -u en:de          # switches translation to english - german
  kdi -i                # displays current configuration.
  kdi -l                # displays log. 
  ```

## Installation

  0. **Select a directory where you want to install the script**:
  
      ```bash
      cd your/installation/directory
      ```

  1. **Open the terminal and clone this repository using the following command**:
      ```bash
      git clone https://github.com/sunbaee/kaiDi.git
      ```

  3. **Install the program**:
      ```bash
      cd kaiDi && sudo ./install.sh
      ```

  4. **Add the program to your shell**:
      <details>
      <summary>Bash</summary>
        
      > Add this line to the end of your config file ( `~/.bashrc` ):
      > ```sh
      > export PATH="usr/local/bin:$PATH" 
      > ```
    
      </details>

If everything went right, you should be able to use the program!

## Configuration

The first time you try to translate something, you'll be prompted to set the configuration file.
You can use the -u option to update the configuration file:
```bash
kdi -u sourceLanguage:targetLanguage:lingueeDomain
```
_Use your preferred options instead of the words shown above._

<br>Here's a configuration example for **english-french** translation:

```bash
kdi -u english:french:.com
```
_Note: its possible to use the full language name, but its also possible to use any ISO639 language code for the languages._

<br> _For example: **en for english** and **fr for french**._

