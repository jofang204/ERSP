Before running, please organize your folder.
There must be folders named raw and soft. Within these folders, files must be
put in coresponding platform folders. Files must be unzipped and untarred before
running the scripts.

bash normalization.sh  # must be run on hegemon server

python soft_parser.py <path-to-softfile>  # can only add gene name and gene title. Also produces idx file

python thre.py

python info.py
