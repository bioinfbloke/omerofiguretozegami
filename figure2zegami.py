##!/usr/bin/env python
from omero.rtypes import wrap
from omero.gateway import BlitzGateway
import omero
import os
import csv

USERNAME = os.environ["USER"]
PASSWORD = os.environ["PASS"]
HOST = os.environ["HOST"]

conn = BlitzGateway(USERNAME, PASSWORD, host=HOST, port=4064)
conn.connect()

# cross-group query to find file
conn.SERVICE_OPTS.setOmeroGroup(-1)
# Script should already be installed here for figure app
SCRIPT_PATH = "/omero/figure_scripts/Figure_To_Pdf.py"


#id = 2086989;
#to check figures

format = 'PDF'
zegami_tsv = "zegami.tsv"
y = open(zegami_tsv,'w')
z = csv.writer(y, delimiter="\t")

# write the header
z.writerow(["gene","bangalore","probe", "author","pdf","figure_id","path"])

script_service = conn.getScriptService()
script_id = script_service.getScriptID(SCRIPT_PATH)
num = 1

for f in conn.getObjects("FileAnnotation", attributes={"ns": "omero.web.figure.json"}):
    # name of figure using naming convention agreed and then made upper case
    figure_name = f.getFile().getName().upper()
    # internal id of the figure
    id = f.getId()
    # name of output, currently a TIFF
    file_name = figure_name + "." + format
    meta_data = figure_name.split("_")
    meta_data.append(file_name)
    meta_data.append(id)
    #print str(meta_data)
    # ST for testing
    # this works 
    #id = 2086989
    # check the name has 6 fields (including the added figure id) which is a crude way of enforcing the naming scheme
    if len(meta_data) == 6:
    	# each one should have a banglore id and a tissue, currently BRAIN for testing
	# to do: add more filters 
	
	# This is a specific template file that is left in
	if "TEMPLATE" in meta_data[0]:
		continue
	
	
    	if "VNC" in meta_data[2] or "MB" in meta_data[2] or "OL" in meta_data[2] or "CB" in meta_data[2]:
    		print "Checking if "+file_name+" is downloaded."
		print "Number of files processed = "+ str(num)
	    	print "id="+ str(id)
  	  	print "0 = "+ str(meta_data)
  	  	print "1 = "+meta_data[1]
		print "2 = "+meta_data[2]
		# add a column to metadata
		meta_data.append(figure_name+".png")
    		z.writerow(meta_data)
    
    		# skip download if exists
    		if os.path.isfile(file_name):
    			print "Got "+file_name+" already."
    			continue
		
		
		figure_ann = conn.getObject("FileAnnotation", id)
		figure_json = "".join(figure_ann.getFileInChunks())
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

		if rv.get('File_Annotation'):
  			figure_id = rv.get('File_Annotation').getValue().id.val
  			figure_pdf = conn.getObject("FileAnnotation", figure_id)
   			f = open(file_name, 'w')
   			print "\nDownloading file",file_name,"..."
   			
			try:
       				for chunk in figure_pdf.getFileInChunks():
           				f.write(chunk)
  			finally:
       				f.close()
       				print "File ",file_name,"downloaded!"
		

		# create a png
		os.system('mogrify -density 400 -background white -alpha remove -format png '+file_name)
		num = num + 1


# Final processing to remove all extraneous pngs
# could probably be done better in python
os.system('find . -name "*\-[12345679].png" -exec rm {} \;') 
os.system('rename "s/-0//" *.png')
		

