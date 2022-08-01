#!/bin/sh
# this one runs with python3.8 not 3.6
location=$1
/usr/local/bin/python3.8 download_backup_file.py ${location}
return $?
