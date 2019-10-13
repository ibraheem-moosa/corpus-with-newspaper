#!/bin/sh

mkdir -p $2

find $1 -type f ! -name "*.csv" -exec cp {} $2 \;
