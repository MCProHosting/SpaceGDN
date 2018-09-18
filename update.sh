#!/bin/sh
cd /storage/SpaceGDN/
git pull origin master
/usr/local/bin/python2.7 run.py load
