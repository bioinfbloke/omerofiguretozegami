# omerofiguretozegami
Converts OMERO figure data to images and metadata suitable for creating a Zegami collection. 

## python versions
Runs under Python 2.7+

## prerequisites
Needs ImageMagick installed.

You need to set up environment variables containing the information of username, password and hostname for the OMERO database. For example:
```
USER="xxxx"
PASS="xxxx"
HOST="xxxx"
PYTHONPATH=$PYTHONPATH:/opt/ice-python/lib/python2.7/site-packages:/opt/omero/OMERO.server-5.2.7-ice36-b40/lib/python/
export USER PASS HOST PYTHONPATH
```
You may find it convenient to set this up in a script that you source before you run figure2zegami.py but beware of storing usernames and passwords!

Currently requires ImageMagick to be installed.

To run enter:

`python figure2zegami.py`


