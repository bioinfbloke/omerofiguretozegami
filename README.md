# omerofiguretozegami
Converts OMERO figure data to images and metadata suitable for creating a Zegami collection. 

## python versions
Runs under Python 2.7+

## prerequisites
Needs OMERO ICE libraries and python path should be set e.g.
```
export PYTHONPATH = /opt/ice-python/lib/python2.7/site-packages:/opt/omero/OMERO.server-5.2.7-ice36-b40/lib/python/
```
Fill in the details for USER, PASS and HOSTNAME in the script
currently requires ImageMagick to be installed.

To run enter:

`python figure2zegami.py`

## Convert PDF to PNG

When requirements are completely worked out this should be made into a python module. These are the shell commnds to be run in the PDF directory.

```
mogrify -background white -format png *.PDF
find . -name "*\-[12345679].png" -exec rm {} \;
rename.pl 's/\-0\.png/\.png/' *.png 
```
