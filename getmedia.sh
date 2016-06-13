#!/bin/bash

if [ $# -ne 1 ]; then
	echo "ERROR: Wrong usage!"
	exit 1
fi

readonly program=$1

url=$(youtube-dl -g "$program")
if [ $? -ne 0 ]; then
	echo "ERROR: Cannot get video URL for the program!"
	exit 1
fi
