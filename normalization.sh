#!/bin/bash

raw_dir=./raw/*

# normalization
for f in $raw_dir
do
	echo $f
	platform=`basename $f`
	echo $platform
	python unwanted_list.py $platform > $platform.unwanted

	# untar the raw files
	for t in $f/*RAW.tar
	do
		echo untarring $t
		tar -xvf $f
		rm $f
	done
	
	# remove the unwanted GSMs
	for file in `cat $platform.unwanted`
	do
		rm ./raw/$platform/$file*
	done
	
	rm $platform.unwanted
	ls ./raw/$platform/*CEL* > filelist
	bash scr-rma $platform
done

# compile into one expr
soft_touse=`ls ./soft/GPL570/*soft | head -1`
python soft_parser.py $soft_touse
python thre.py
python info.py



