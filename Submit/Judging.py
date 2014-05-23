import os
import re
import sys
import time
import getpass
import urllib2
import threading

import test

def wait(arg1 , stop_event):
    try :
        while (not stop_event.is_set()):
            sys.stdout.write('.')
            sys.stdout.flush()
            stop_event.wait(0.3)
    except Exception as error :
        print "Error Ocurred while running thread !!"
        

def get_status(url,ID):
    try :
        htmltext = urllib2.urlopen(url)
    except Exception as error:
        print "Unable to Fetch Result !!"
        print error
    htmltext = htmltext.read(13000)
    pat = "id=\"statusres_"+ ID + "\".*?>(.*?)</td>"
    match = re.search(pat,htmltext,re.DOTALL)
    if not match :
        print "Error in parsing the webpage !!"
        return
    resp = match.group(1)
    resp = resp.replace("\n","")
    resp = resp.replace("\t" , "")
    resp = resp.strip()
    result = resp.find("runtime error")
    if result >= 0 :
        match = re.search("<a.*?>(.*?)</a>",resp,re.DOTALL)
        if match :
            resp = "runtime error" + '(' + match.group(1) + ')'
        match = re.search("runtime error(.+)",resp,re.DOTALL)
        if match :
            resp = "runtime error" + '(' + match.group(1).replace(" ","") + ')'
        else : resp = "runtime error"
    return resp,htmltext
 
def parse(htmltext , ID):
    ID = ID.strip()
    pattern = "id=\"statustime_" + ID + "\">.*?<a.*?>(.*?)</a>"
    match = re.search(pattern,htmltext,re.DOTALL)
    if match :
        match = match.group(1)
        match = match.replace("\n","")
        match = match.replace("\t","")
        match = match.strip()
    else:
        match = "0.0"
    time = match
    pattern = "id=\"statusmem_" + ID + "\">(.*?)</td>.*?<p>(.*?)</p>(.*?)/td>"
    match = re.search(pattern,htmltext,re.DOTALL)
    if match:
        memory = match.group(1)
        memory = memory.replace("\n","")
        memory = memory.replace("\t","")
        memory = memory.strip()
    else : memory = "0M"
    if match :
        lang = match.group(2)
        lang = lang.replace("\n","")
        lang = lang.replace("\t","")
        lang= lang.strip()
        st = match.group(3)
        temp = re.search("class=.*?>(.*?)</p>",st,re.DOTALL)
        if temp :
            lang = lang + '('+ temp.group(1) + ')'
    else : lang = "Default"
    
    return time,memory ,lang
    
def check(status , htmltext,ID):
    
    status = status.strip()
    if status.startswith("accepted") :
        print 
        print  "Hooray !! Your solution got " + status
        extime , memory , lang = parse(htmltext , ID)
        print "Execution Time : %s \t" % extime,
        print "Memory Used : %s \t" % memory ,
        print "Language : %s " % lang
        return True
    elif status.startswith("wrong") :
        print
        print "Oops !! Wrong Answer .Check the boundary constraint "
        extime , memory , lang = parse(htmltext , ID)
        print "Execution Time : %s \t" % extime,
        print "Memory Used : %s \t" % memory ,
        print "Language : %s " % lang
        return True
    elif status.startswith("time") :
        print
        print "Oops !! Time Limit Exceeded .Try to optimize your algorithm"
        extime , memory , lang = parse(htmltext , ID)
        print "Execution Time : %s \t" % extime,
        print "Memory Used : %s \t" % memory ,
        print "Language : %s " % lang
        return True
    elif status.startswith("runtime"):
        print
        print "Oops !! %s.Don't get frustrated , Try again !" % status
        extime , memory , lang = parse(htmltext , ID)
        print "Execution Time : %s \t" % extime,
        print "Memory Used : %s \t" % memory ,
        print "Language : %s " % lang
        return True
    elif status.startswith("compilation"):
        print
        print "Oops !! Compilation Error "
        print "Check your syntax !!"
        return True
    return False
    
   
def main(name,password,path,lang,code):
    
    ID = test.style(name , password , path ,lang ,code)
    if not ID :
        return
    ID = ID.strip()
    status = ""
    statusList =[]
    print "Waiting for the response from the server !!"
    
    url = "http://www.spoj.com/status/" + name
    
    th_stop = threading.Event()
    th = threading.Thread(target = wait , args=(1,th_stop))
    th.daemon = True
    try :
        th.start()
        for i in range(500):
            
            status ,htmltext= get_status(url,ID)
            if status in statusList:
                pass
            else :
                if status.strip() == "waiting..":
                    pass
                else :
                    statusList.append(status)
                temp = status.replace(" ","")
                temp = temp.replace(',',"")
                if temp.isdigit() :
                    print "\n"
                    print "Your Score of the above problem : %s "% temp
                    status = "accepted"
                if check(status , htmltext , ID):
                    
                    break
                print "\n"+status     
            time.sleep(1)
        th_stop.set()
    except Exception as error :
        print error 
    
if __name__ == '__main__':
    main()










