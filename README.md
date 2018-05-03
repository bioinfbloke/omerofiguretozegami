# omerofiguretozegami
Converts OMERO figure data to images and metadata suitable for creating a Zegami collection. 

## python versions
Runs under Python 2.7+

## prerequisites
Needs ImageMagick installed.

You need to set up environment variables containing the information for omero libraries, and hostname for the OMERO database enter :
```
source setup.sh 
```

To run the script to download the OMERO figures and generate the initial metadat table (zegami.tsv) do:

`python figure2zegami.py`

You will be prompted for your OMERO password. The username is assumed to be the one in $USER.

It will then download PDFs of the figures to the directory this is run in and convert them automatically to PNGs. It also creates a zegami.tsv text file that contains the metadata required to make a Zegami collection.

