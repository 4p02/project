#!/bin/bash

# min version for postgrest
MIN_VERSION_POSTGRES_VERSION="9.6"

# get postgres version
PG_VERSION=$(psql --version | awk '{print $3}')

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
        if [ "$(uname -a | grep -icP 'debian|ubuntu|mint')" == "1" ]; then
            # Do something under GNU/Linux platform
            echo "Debian-based or Ubuntu-based distro; installing dependencies"
            echo '$ sudo apt-get install ghc cabal-install libghc-postgresql-libpq-dev libpq-dev'
            sudo apt-get install ghc cabal-install libghc-postgresql-libpq-dev libpq-dev

            compile_from_source
            exit
        fi
    else
        echo "Couldn't automatically detect your platform..."
        compile_from_source
        exit
    fi
}

function compile_from_source {
    echo "Compiling from source"
    echo "Dependencies: git, ghc, cabal, libpq-dev, libpq"
    echo "Praying to the dependency gods... good luck..."

    git clone https://github.com/postgrest/postgrest.git /tmp/postgrest
    cd /tmp/postgrest/
    cabal update
    cabal build

    echo "Postgrest is fucking somewhere in /tmp/postgrest/dist/build/<platform>/ghc-version/postgrest-version/x/postgrest/build/postgrest/"
    echo "Place it on your path"
}

function run_postgrest {
    if [[ -e "backend/postgrest.conf" ]]; then
        CONFIG_FILE="backend/postgrest.conf"
    else
        CONFIG_FILE="backend/postgrest.default.conf"
    fi

    # get current path and add the default config file
    postgrest "$CONFIG_FILE"
}

install_postgrest
run_postgrest
