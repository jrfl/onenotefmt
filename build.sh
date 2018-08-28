#!/bin/sh

pymver=$(python -V | tr -d " a-zA-Z" | cut -d. -f1)
PYTHON="python"

# Test for a python ver 3 install. This is simple minded...
# if this crap fails and you *know* you have python3 installed,
# set PYTHON="<path and filename for your python 3 executable>"
# and comment out all the version checking crap below
if [[ "$pymver" != "3" || -z "$pymver" ]]
then
    pymver=$(python3 -V | tr -d " a-zA-Z" | cut -d. -f1)
    if [[ "$pymver" != "3" ]]
    then
        PYTHON=""
    else
        PYTHON="python3"
    fi
fi


if [[ -z "$PYTHON" ]]
then
    echo fail, python3 is required
    exit 3
fi
# End of python versioning crap

$PYTHON main.py

$PYTHON gettoc.py

$PYTHON bldndx.py

echo If there were no python errors, the docset can be found in the
echo onenotefmt.docset directory.
echo Enjoy

