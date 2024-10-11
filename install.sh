#!/bin/bash

# Installing python dependencies:
mkdir .venv
python -m venv .venv
source .venv/bin/activate
pip install lxml bs4 requests
deactivate

DIREC="$(pwd)"

if ! [ -d /usr/local/bin ]; then
    mkdir /usr/local/bin;
fi;

cd /usr/local/bin

# Creating executable file to open the program in the terminal
echo "#!/bin/bash"               | cat  > kdi
echo                             | cat >> kdi
echo "cd ${DIREC}"               | cat >> kdi
echo 'source .venv/bin/activate' | cat >> kdi
echo 'python main.pyw $@'        | cat >> kdi

chmod +x kdi