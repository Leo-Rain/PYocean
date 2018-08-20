#!/bin/sh

#find /home/alwin/SOEST -type f -name '*.csv' -o -name '*.prj' -o -name '*.xls' -o -name '*.shp' -o -name '*.shx' -o -name '*.dbf'
find /home/alwin/SOEST -type f -name '*.csv' -exec rm {} +
find /home/alwin/SOEST -type f -name '*.xls' -exec rm {} +
find /home/alwin/SOEST -type f -name '*.shp' -exec rm {} +
find /home/alwin/SOEST -type f -name '*.shx' -exec rm {} +
find /home/alwin/SOEST -type f -name '*.prj' -exec rm {} +
find /home/alwin/SOEST -type f -name '*.dbf' -exec rm {} +
rm -rf /home/alwin/RESULTSOEST/*
rm -rf /home/alwin/SOEST/JAN2018
rm -rf /home/alwin/SOEST/FEB2018
rm -rf /home/alwin/SOEST/MAR2018
rm -rf /home/alwin/SOEST/APR2018
rm -rf /home/alwin/SOEST/MAY2018
rm -rf /home/alwin/SOEST/JUN2018
rm -rf /home/alwin/SOEST/JUL2018
rm -rf /home/alwin/SOEST/AUG2018
rm -rf /home/alwin/SOEST/SEP2018
rm -rf /home/alwin/SOEST/OCT2018
rm -rf /home/alwin/SOEST/NOV2018
rm -rf /home/alwin/SOEST/DEC2018
