#!/bin/bash

# min version for postgrest
MIN_VERSION_POSTGRES_VERSION="9.6"

# get postgres version
PG_VERSION=$(psql --version | awk '{print $3}')

CONFIG_FILE_NAME="postgrest.default.conf"

version_compare () {
    if [[ $1 == $2 ]]
    then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            return 2
        fi
    done
    return 0
}

# Check if postgres is installed and is version 9.6 or higher
function check_if_postgres_is_installed {
    if [ "$(command -v psql)" ]; then
        version_compare "$PG_VERSION" "$MIN_VERSION_POSTGRES_VERSION"
        if [ $? -eq 2 ]; then
            echo "PostgreSQL version is lower than $MIN_VERSION_POSTGRES_VERSION"
            exit 1
        else
            echo "PostgreSQL is installed and version is $PG_VERSION which meets the requirements for postgrest"
        fi
    else
        echo "PostgreSQL is not installed"
        exit 1
    fi
    
}

function install_postgrest {
    check_if_postgres_is_installed
    if ["$(command -v postgrest)"]; then
        echo "Skipping postgrest installation bc already installed"
        return
    fi
    if [ "$(uname)" == "Darwin" ]; then
        # Do something under Mac OS X platform
        echo "Mac OS X found and installing using brew"
        brew install postgrest
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Do something under GNU/Linux platform
        echo "Linux found and installing using apt-get"
        sudo apt-get install postgrest
    fi
}

function run_postgrest {
    # get current path and add the default config file
    postgrest $(pwd)/$CONFIG_FILE_NAME
}

install_postgrest
run_postgrest


