#!/bin/sh
find $1 ! -name "*.csv" -type f | rev | cut -d"/" -f1 | sort | uniq | wc -w
