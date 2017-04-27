#/bin/bash

raw_dir=./raw/*

for f in $raw_dir
do
	platform=`basename $f`
	echo $platform
	python unwanted_list.py $platform > $platform.unwanted 
	
	# remove the unwanted GSMs
	for file in `cat $platform.unwanted`
	do
		rm ./raw/$platform/$file*
	done
	
	rm $platform.unwanted
	ls ./raw/$platform/*CEL* > filelist
	bash scr-rma $platform
	
done

