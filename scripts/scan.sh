#!/bin/env bash

run_terra=$1


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Import the settings file so you don't have to!
source $DIR/.settings


# Terraform machine go brrrrr
if [ "$run_terra" -eq "1" ]; then
   bash $DIR/tf-init.sh
    bash $DIR/tf-plan.sh
    bash $DIR/tf-show.sh
fi


# Scan dat
python $DIR/parse.py