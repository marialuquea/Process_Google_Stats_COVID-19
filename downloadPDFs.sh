#!/bin/bash

URLs=$(curl "https://www.google.com/covid19/mobility/" | grep 'Mobility_Report_en.pdf"' | sed -E 's/^.*href="(.+)".*$/\1/g')
​
​
URL0="https://www.gstatic.com/covid19/mobility/"
URL1="Mobility_Report_en.pdf"
​
datedwn=$(date +"%Y-%m-%d")
​
outfolder=gdata${datedwn}
​
rm -R $outfolder
mkdir $outfolder
​
cd $outfolder
​
for u in $URLs
do
​
	echo $u
​
	curl -O $u
done


