#!/bin/bash

# Checks if docker is installed.
if ! command -v "docker" 2>&1 > /dev/null; then
    echo
    echo -e "You need \033[1mdocker\033[0m to install this program."
    echo -e "See https://www.docker.com/ to install \033[1mdocker.\033[0m"
    echo
    exit 1;
fi

# Checks if docker daemon is running and starts it if it's not.
if ! pgrep -x "docker" > /dev/null; then
    sudo systemctl start docker;
fi

docker build -t kaidi-docker . 

if ! [ -d /usr/local/bin ]; then
    mkdir /usr/local/bin;
fi;

cd /usr/local/bin;

# Creating executable file to open the program in the terminal
echo "#!/bin/bash"                                                     | cat  > kdi;
echo                                                                   | cat >> kdi;
echo 'docker run --rm -v kaidi-data:/usr/src/app/Data kaidi-docker $@' | cat >> kdi;

chmod +x kdi;