#!/bin/bash

raw_dir=./raw/GPL570
platform=GPL570

wanted=`tail -n +2 GPL570-ih.txt | cut -f1`
rm filelist
touch filelist
files=`ls $raw_dir`

# survival and ih
python quickstart.py

for id in $wanted
do
    baseAddress=ftp://ftp.ncbi.nlm.nih.gov/geo/samples/
    GSMID=${id}
    flag=true

    for raw_file in $files; do
	cropped_file=$(echo $raw_file |sed -n 's/.*\(GSM[0-9]*\).*/\1/p')
        if [[ ${GSMID} == ${cropped_file} ]]
        then flag=false
            break
        fi
    done

    if [ ${flag} = true ]
    then
        Len=${#GSMID}
        GSMDIR=${GSMID::Len-3}nnn/
        webLink=${baseAddress}${GSMDIR}${GSMID}/suppl/${GSMID}.CEL.gz
        wget -O ${raw_dir}/${GSMID}.CEL.gz ${webLink}
    fi
    
    ls $raw_dir/$id* >> filelist
    echo "Done with $id"
done


bash scr-rma $platform
soft_touse=`ls ./soft/GPL570/*soft | head -1`
python soft_parser.py $soft_touse
python thre.py
python info.py

# normalization
for f in $raw_dir
do
	echo $f
	platform=`basename $f`
	echo $platform
	python unwanted_list.py $platform > $platform.unwanted

	raw_tar=./raw/GPL570/*

	# # untar the raw files
	# for t in $raw_tar
	# do
	# 	echo $t
	# 	echo "untarring $t"
	# 	tar -xvf $t
	# 	rm $t
	# done
	
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
soft_to_use=`ls ./soft/GPL570/*soft | head -1`
python soft_parser.py $soft_to_use
python thre.py
python info.py



