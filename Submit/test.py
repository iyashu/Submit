import urllib2
import getpass
import os
import sys
import re
import threading
import keyring
from time import sleep
from poster import encode
from poster import streaminghttp


def wait(arg1 , stop_event):
    while (not stop_event.is_set()):
        sys.stdout.write('.')
        sys.stdout.flush()
        stop_event.wait(0.3)
        

def get_response(Username , pwd , path , lang ,problem):
    url = "http://www.spoj.com/submit/complete/"
    streaminghttp.register_openers()
    name  = Username
    password = pwd
    filename = path
    language = lang
    problemcode = problem
    
    th_stop = threading.Event()
    sys.stdout.write('Submitting  ')
    sys.stdout.flush()
    th = threading.Thread(target = wait , args=(1,th_stop))
    th.daemon = True
    th.start()
    
    try :
        datagen, headers = encode.multipart_encode({'login_user':name,'password':password,"subm_file": open(filename, "rb"),'lang':language,'problemcode':problemcode})
        request = urllib2.Request(url, datagen, headers)
        resp = urllib2.urlopen(request).read()
    except Exception as error:
        print "Error Occured  !!"
        print error
    th_stop.set()
    return resp

def style(name , password , path ,lang ,code):
   
    resp = get_response(name , password , path ,lang ,code)
    print 
    if resp.find('failed')>0:
        print "Incorrect Username or Password "
        return 
    
    match = re.search("Server time:.*?class=\"time\">(.*?)<br>.*?<b>(.*?)</b>",resp,re.DOTALL)
    if match :
        date = match.group(1)
        date = date.replace("\n","").strip()
        time = match.group(2).strip()
    else:
        date = "Undefined !!"
        error = "Undefined !!"
    print "Server Time : %s   %s" % (date , time)
    
    match = re.findall("<h3>(.*?)</h3>",resp,re.DOTALL)
    if len(match) == 0 or (not match[-1].startswith("Solution")):
        print "Error Occurred in Submitting the Answer !!"
        print "May be your problem code is invaild ..."
        return 
    print match[-1]
    
    current = os.path.expanduser('~')
    current = os.path.join(current,'.Submit')
    if not os.path.exists(current):
        os.makedirs(current)
    secret = os.path.join(current , '.secret.txt')
    with open(secret, 'w') as content_file :
        content_file.write(name)
    keyring.set_password('secret',name,password)
    
    match = re.findall("<input.*?type=\"hidden\".*?value=(.*?)/>",resp,re.DOTALL)
    if len(match) == 0:
        print "Error Occurred in gathering the submission ID !!"
        return 
    else :
        ID = match[-1].replace("\"","").strip()
        print "Solution ID : " ,  ID
        return ID
    
    
    return
def main():
    name = raw_input("Enter your spoj username : ")
    password = getpass.getpass("Password : ")
    path = "/home/yash/Desktop/me.cpp"
    lang = '41'
    code = 'TDPRIMES'
    
    style(name , password , path ,lang ,code)

if __name__ == '__main__':
    main()
