#!/bin/sh

code=15

calcPer()
{
 local c=$1
 per=$(echo "scale=2;$c / $baris * 100"|bc -l)
}

echo 'Collecting results:' 
dbus-launch gcp -rf /home/alwin/oscar_vel2018/* /home/alwin/RESULTOSCAR2018/ 
echo 'Results collected'
echo ''
echo 'Removing unnecessary files'
find /home/alwin/RESULTOSCAR2018 -type f -name '*.nc' > dafdel
baris=$(wc -l < dafdel)
i=1
while read p; do
	calcPer $i
	rm $p
	echo "|\e[48;5;${code}m%${per%.*}s\e[31m${per%.*}"
	echo '%s\e[0m%s\r' "%" "|" 
	echo $((i+=1)) >/dev/null
done <dafdel
rm dafdel
echo 'All cleared!'
