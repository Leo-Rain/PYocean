#!/bin/sh

#find /home/alwin/NCDC2017 -type f -name '*.csv' -o -name '*.prj' -o -name '*.xls' -o -name '*.shp' -o -name '*.shx' -o -name '*.dbf'
find /home/alwin/NCDC2017 -type f -name '*.csv' -exec rm {} +
find /home/alwin/NCDC2017 -type f -name '*.xls' -exec rm {} +
find /home/alwin/NCDC2017 -type f -name '*.shp' -exec rm {} +
find /home/alwin/NCDC2017 -type f -name '*.shx' -exec rm {} +
find /home/alwin/NCDC2017 -type f -name '*.prj' -exec rm {} +
find /home/alwin/NCDC2017 -type f -name '*.dbf' -exec rm {} +
rm -rf /home/alwin/RESULTNCDC2017/*
