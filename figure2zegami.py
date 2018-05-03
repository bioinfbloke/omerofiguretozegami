"""
Many thanks to Will Moore for helping develop this script
See http://lists.openmicroscopy.org.uk/pipermail/ome-users/2017-February/006362.html
"""

from omero.rtypes import wrap
from omero.gateway import BlitzGateway
import getpass
import omero
import os
import csv
import sys
import threading
import time
import re

USER = os.environ['USER'] 
PASS = getpass.getpass("Enter Password:") 
#PASS = os.environ['PASS']
HOST = os.environ['HOST']

conn = BlitzGateway(USER, PASS, host=HOST, port=4064)
conn.connect()

# cross-group query to find file
conn.SERVICE_OPTS.setOmeroGroup(-1)
# Script should already be installed here for figure app
SCRIPT_PATH = "/omero/figure_scripts/Figure_To_Pdf.py"


#id = 2086989;
format = 'PDF'
zegami_tsv = "zegami.tsv"
y = open(zegami_tsv,'w')
z = csv.writer(y, delimiter="\t")

# write the header
z.writerow(["gene","bangalore","probe", "author","image","figure_id"])

script_service = conn.getScriptService()
script_id = script_service.getScriptID(SCRIPT_PATH)

# keep connection to OMERO alive
def keep_connection_alive():
    while True:
        conn.keepAlive()
        time.sleep(60)
	
th_ka = threading.Thread(target = keep_connection_alive)
th_ka.daemon = True
th_ka.start()

num = 1
for f in conn.getObjects("FileAnnotation", attributes={"ns": "omero.web.figure.json"}):
    # name of figure using naming convention agreed and then made upper case
    figure_name = f.getFile().getName().upper()
    # get rid of non alphas and leave underscore
    # there are some inconsistencies in the gene names that need this e.g. / -
    figure_name = re.sub('[^0-9a-zA-Z_]+', '', figure_name)
    
    #print figure_name
    
    # internal id of the figure
    id = f.getId()
    # name of output, currently a PDF
    #id = 2091667
    file_name = figure_name + "." + format
    image_name = figure_name + ".png"
    meta_data = figure_name.split("_")
    meta_data.append(file_name)
    
    meta_data.append(id)
    #print str(meta_data)
    # ST for testing
    # this works 
    #print(len(meta_data)) 
    # check t:whe name has at least 6 fields (including the added figure id) which is a crude way of enforcing the naming scheme
    if len(meta_data) >= 5:
        # each one should have a banglore id and a tissue, currently BRAIN for testing
        # to do: add more filters 
        #if "VNC" in meta_data[2] or "MB" in meta_data[2] or "OL" in meta_data[2] or "CB" in meta_data[2]:
        if "ZEGAMI1" in file_name and "TEMPLATE" not in file_name:
            # write out zegami tsv file	   
	    min_info = meta_data[:4]
	    min_info.append(image_name);
	    min_info.append(figure_name);
            z.writerow(min_info) 
            
	    if os.path.isfile(image_name):
                print "Got "+image_name+" already. Skipping..."
                continue
	    

	    print "Number of files processed = "+ str(num) + "; id=" + str(id) + "; Figure name = " + figure_name  
 
            figure_ann = conn.getObject("FileAnnotation", id)
            figure_json = "".join(figure_ann.getFileInChunks())
	    #f = open(figure_name+".json","w")
	    #f.write(figure_json)
	    
            script_service = conn.getScriptService()
            # set group for saving figure to same group as file
            conn.SERVICE_OPTS.setOmeroGroup(figure_ann.getDetails().group.id.val)
            input_map = {
                   'Figure_JSON': wrap(figure_json),
                    'Export_Option': wrap(format),       # 'PDF' or 'TIFF'
                    'Webclient_URI': wrap("http://your_server/webclient/"),  # Used in 'info' PDF page for links to images
            }
            proc = script_service.runScript(script_id, input_map, None, conn.SERVICE_OPTS)
            job = proc.getJob()
            cb = omero.scripts.ProcessCallbackI(conn.c, proc)
            
            try:
                print "Job %s ready" % job.id.val
                print "Waiting...."
                while proc.poll() is None:
                        cb.block(1000)
                print "Callback received: %s" % cb.block(0)
                rv = proc.getResults(3)
            finally:
                cb.close()
    
            if rv.get('stderr'):
                print "Error. See file: ", rv.get('stderr').getValue().id.val
    
            if rv.get('New_Figure'):
                figure_id = rv.get('New_Figure').getValue().id.val
		print "Internal figure id = "+str(figure_id)+"!"
		conn.SERVICE_OPTS.setOmeroGroup(-1)
                figure_pdf = conn.getObject("FileAnnotation", figure_id)
                f = open(file_name, 'w')
                print "\nDownloading file",file_name,"..."
                try:
                        for chunk in figure_pdf.getFileInChunks():
                            f.write(chunk)
                except AttributeError:
                        print "Bad PDF problem for " + str(id) + "!"
                finally:
                        f.close()
                        print "File ",file_name,"downloaded!"
                num = num + 1


# Final processing to remove all extraneous pngs
# could probably be done better in python
# create PNGs and tidy up names
os.system('find . -name "*.PDF" -exec mogrify -density 400 -background white -alpha remove -format png {} \;')
os.system('find . -name "*\-[12345679].png" -exec rm {} \;') 
os.system('rename "s/-0//" *.png')
