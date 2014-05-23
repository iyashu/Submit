import os
import sys
import getpass
import Judging
import keyring

def get_lang(extension):
    langMap = {'cpp' : '41','py':'4','c' : '11','java':'10'}
    try :
        return langMap[extension]
    except :
        return 
def submit_two(argument,problemcode = None): 
    #Fetching Problem code and lang from file name
    current = os.getcwd()
    filename = argument
    temp = filename.split('.')
    if len(temp) < 2 :
        print "Getting invalid file !!"
        print  filename , " : Having no language extension !!"
        sys,exit(1)
    else:
        lang = get_lang(temp[-1])
        if not lang :
            print "Getting invalid file Extension!!"
            print  "Contact : yashpal.c1995@gmail.com "
            sys.exit(1)
        temp = len(temp[-1])+1
        if not problemcode :
            problemcode = filename[:len(filename)-temp]
        problemcode = problemcode.upper()
        if os.path.exists(filename):
            path = filename
        else :
            path = os.path.join(current,filename)
        if not os.path.exists(path):
            print "Error : Invalid file path !!"
            print "Contact : yashpal.c1995@gmail.com"
            sys.exit(1)
        #check from save password !!
        name = ""
        password = ""
        current = os.path.expanduser('~')
        current = os.path.join(current,'.Submit')
        if not os.path.exists(current):
            os.makedirs(current)
        secret = os.path.join(current , '.secret.txt')
        if not os.path.exists(secret):
            name = raw_input("Enter your spoj username : ")
            password = getpass.getpass("Password : ")
        else :
            with open(secret, 'r+') as content_file :
                content = content_file.readlines()
                if content :
                    name = content[0].replace('\n',"")
                    password=keyring.get_password('secret',name)
                else :
                    name = raw_input("Enter your spoj username : ")
                    password = getpass.getpass("Password : ")
        Judging.main(name,password,path,lang,problemcode)
  
    
def main():
    arguments = sys.argv
    current = os.getcwd()
    if len(arguments)<2 :
        #Missing arguments !!
        print "Submit: missing operands !!"
        print "Try 'Submit --help' for more information"
        return
    elif len(arguments) == 2 :
        argument = arguments[-1]
        if argument == '--help' :
            print "Usage : Submit [problemcode] [solution]"
            print "\tEx : Submit TEST TEST.cpp\n"
            print "Short Usage : Submit [filename]"
            print "\tName your solution file with problemcode !!"
            print "\tEx : 'PRIME1.cpp' to submit PRIME1 problem :-\n\t\tSubmit PRIME1.cpp\n"
            print "Submit --reset \n\tTo reset the saved username/password\n"
            print "Note : Currently the program only supports C,C++,Python and Java solutions. \n"
            print "Contact me : yashpal.c1995@gmail.com"
            #print "0"
            
        elif argument == '--reset':
            current = os.path.expanduser('~')
            current = os.path.join(current,'.Submit','.secret.txt')
            if os.path.exists(current):
                open(current, 'w').close()
                print "Done Successfully !!"
                print "Enter One-time Information while submitting next solution !! :)"
            else:
                print 'Password not set ,so cannot be reset ...'
        else :
            submit_two(argument)
    elif len(arguments) == 3 :
        
        problemcode = arguments[1]
        path = arguments[2]
        submit_two(path,problemcode)
            

if __name__ == '__main__':
    main()