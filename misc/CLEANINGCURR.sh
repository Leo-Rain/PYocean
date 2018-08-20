#!/bin/sh

#find /home/alwin/oscar_vel2018 -type f -name '*.csv' -o -name '*.prj' -o -name '*.xls' -o -name '*.shp' -o -name '*.shx' -o -name '*.dbf'
find /home/alwin/oscar_vel2018 -type f -name '*.csv' -exec rm {} +
find /home/alwin/oscar_vel2018 -type f -name '*.xls' -exec rm {} +
find /home/alwin/oscar_vel2018 -type f -name '*.shp' -exec rm {} +
find /home/alwin/oscar_vel2018 -type f -name '*.shx' -exec rm {} +
find /home/alwin/oscar_vel2018 -type f -name '*.prj' -exec rm {} +
find /home/alwin/oscar_vel2018 -type f -name '*.dbf' -exec rm {} +
rm -rf /home/alwin/RESULTOSCAR2018/*
rm -rf /home/alwin/oscar_vel2018/JAN2018
rm -rf /home/alwin/oscar_vel2018/FEB2018
rm -rf /home/alwin/oscar_vel2018/MAR2018
rm -rf /home/alwin/oscar_vel2018/APR2018
rm -rf /home/alwin/oscar_vel2018/MAY2018
rm -rf /home/alwin/oscar_vel2018/JUN2018
rm -rf /home/alwin/oscar_vel2018/JUL2018
rm -rf /home/alwin/oscar_vel2018/AUG2018
rm -rf /home/alwin/oscar_vel2018/SEP2018
rm -rf /home/alwin/oscar_vel2018/OCT2018
rm -rf /home/alwin/oscar_vel2018/NOV2018
rm -rf /home/alwin/oscar_vel2018/DEC2018
