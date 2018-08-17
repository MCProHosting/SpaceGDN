#!/bin/sh
cd ~/SpaceGDN
git pull origin master
/usr/local/bin/python2.7 run.py load
