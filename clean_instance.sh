#!/usr/bin/env bash

# Clean the database instead of erasing it
# sqlite3 var/db/webtools.sqlite3 "delete from paste_paste;"
[ -f var/db/webtools.sqlite3 ] && rm var/db/webtools.sqlite3
rm -rf var/cache/*
rm -rf var/logs/*
rm -rf static/*
find . -name "*.pyc" -exec rm {} +;
