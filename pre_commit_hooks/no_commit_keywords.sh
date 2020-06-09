#!/bin/bash

set -e

NOCOMMIT_PRESENT=$(git grep --ignore-case nocommit)

if [ -n $NOCOMMIT_PRESENT ]
then
    echo "#nocommit tagged - commit prevented"
    echo $NOCOMMIT_PRESENT
    exit 1
else
    exit 0
fi


