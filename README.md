# kaiDi

kaiDi is a **terminal translator/dictionary** made in python.
It scrapes the [linguee website](https://www.linguee.com/) to get its translations and 
translates in the same way you'd translate using the website directly, but from the terminal instead. 

It has some extra functions such as: 
  1. Allowing you to **change the linguee domain** with ease if you want to translate from another language perspective.
  2. **Saving translations** to acess them faster (not needing internet connection).
  3. A **fast mode** that shows some suggestions with the translation.

<br>

The only dependency needed for this app is docker. See the [docker](https://www.docker.com) website if you don't have docker installed yet.

<div align="right">

[Preview](#preview)
[Usability](#usability)
[Installation](#installation)
[Configuration](#configuration)  

</div>

---

## Preview

https://github.com/user-attachments/assets/785dfdc9-5e40-4efa-9f19-e0bc453aeea1

## Usability

Here are some of the ways you can use the program in the terminal:
<pre>
kdi translation       # translates "translation" according to your configuration.

kdi -u en:de          # switches translation to english - german
kdi -i                # displays current configuration.
kdi -l                # displays log. 
</pre>

## Installation

  0. **Select a directory where you want to install the script**:
  
      ```bash
      cd your/installation/directory
      ```

  1. **Open the terminal and clone this repository using the following command**:
      ```bash
      git clone https://github.com/sunbaee/kaiDi.git
      ```
  
  2. **Install the program**:
      <details>
      <summary>Linux / WSL</summary>
        
      >
      > **Run this command to install:**
      >  ```bash
      >  cd kaiDi && sudo ./install.sh
      >  ```
      > 
      > **Add the program to your shell**:
      > <details>
      >   <summary>Bash</summary>
      >   
      >    > Add this line to the end of your config file ( `~/.bashrc` ):
      >    > ```sh
      >    > export PATH="/usr/local/bin:$PATH" 
      >    > ```
      >
      > </details>
      >
      > <details>
      >   <summary>Fish</summary>
      >  
      >   > Run this command in the shell:
      >   > ```sh
      >   > fish_add_path /usr/local/bin
      >   > ```
      >  
      > </details>
      > <details>
      >   <summary>Zsh</summary>
      >  
      >   > Add this line to the end of your config file ( `~/.zshrc` ):
      >   > ```sh
      >   > path+=('/usr/local/bin')
      >   > export PATH
      >   > ```
      > </details> 
      >  
      
      </details>
<br>

_If everything went right, you should be able to use the program!_

## Configuration

The first time you try to translate something, you'll be prompted to set the configuration file.
You can use the -u option to update the configuration file:
```bash
kdi -u sourceLanguage:targetLanguage:lingueeDomain
```
_Use your preferred options instead of the words shown above._

<details>
<summary>Example</summary>
  
  > Here's a configuration example for **english-french** translation:
  >   
  > ```bash
  > kdi -u english:french:.com
  > ```

</details>

_Note: its possible to use the full language name, but its also possible to use any [ISO639 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) for the languages._

_**For example**: en, fr, de, pt, ..._
