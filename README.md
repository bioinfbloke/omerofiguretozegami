# omerofiguretozegami
Converts OMERO figure data to images and metadata suitable for creating a Zegami collection. 

## python versions
Runs under Python 2.7+

## prerequisites
Needs OMERO ICE libraries and python path should be set e.g.
```
export PYTHONPATH=$PYTHONPATH:/opt/OMERO.py-5.2.6-ice35-b35/lib/python/
```
Fill in the details for USER, PASS and HOSTNAME in the script
currently requires ImageMagick to be installed.

To run enter:

`python figure2zegami.py`

## Convert PDF to PNG

When requirements are completely worked out this should be made into a python module. These are the shell commnds to be run in the PDF directory.

```
mogrify -density 400 -background white -format png *.PDF
find . -name "*\-[12345679].png" -exec rm {} \;
```
