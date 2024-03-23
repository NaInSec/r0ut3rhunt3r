#!/usr/bin/env python3

'''
# Tools Name : R0ut3rHunt3r
# Author : XSVS_Cyb3r
# Sites : https://xsvscyb3r.id
# Email : xsvscyb3r@proton.me
# Github : github.com/XSVSCyb3rID
'''

def generateNewWIFIPW():

DEBUGGING=0

    listPWs=[]
    with open('pwdlist.txt') as f:
        for line in f:
            listPWs.append(line)
    f.closed

    regExpression=' to : '
    with open('r0ut3rhunt3r.txt') as f:
        for line in f:
            match=re.search(regExpression, line)
            if match:
                pwUsed=line[match.end():] 
                
        if DEBUGGING:
            print "last pwd used is : ", pwUsed.rstrip('\n')
    
    index=0
    try:
        index=listPWs.index(pwUsed)
        sizeOfList=len(listPWs)
        if sizeOfList==index+1:
            index=1
        pw2Return=listPWs[index+1]
    except:
        pw2Return=listPWs[0]

    if DEBUGGING:
        print 'pwd to return: ', pw2Return

    logger.error("Changing pwd from : "+pwUsed+" to : "+pw2Return)
    return pw2Return

def changePassword(username, password, logger):
    DEBUGGING=0
    URL4APPW="http://192.168.0.227/cgi-bin/security.cgi"

    newWIFIPW = generateNewWIFIPW()

    vlpayload={'setobject_security_type':'4', 'setobject_wpaspskPhrase':newWIFIPW}

    try:
        r0=requests.post(URL4APPW, vlpayload, auth=(username, password))
    except:
        print 'Error 200, Error Opening URL : ', URL4APPW
        logger.error("Error 200, Error Opening URL - "+ URL4APPW)

    if DEBUGGING:    
        print "result : ", r0.text    
        print "returned : ", r0.status_code

    if r0.status_code != 200:
        if DEBUGGING:
            print "\n [+] Status code was not 200, it was : ", r0.status_code

        logger.error("status code was not 200, it was : "+ r0.status_code)

def check4ConnectionsR(url, username, password, logger):
    DEBUGGING=0
    wg602=1
    ubnt=0
    url1=""
    username1=""
    password1=""
    repattern='([0-9A-F]{2}[:-]){5}([0-9A-F]{2})'
    macList = []
    assocLine="var assoc_list='"
    authoList="var autho_list='"

    if 1==wg602:
        url1=url
        username1=username
        password1=password
        
    elif 1==ubnt:
        url1="url from ubnt device"
    else:
        url1=url
        username1=username
        password1=password

    if DEBUGGING:
        print "URL1 : ", url1
        print "username1 : ", username1
        print "password1 : ", password1

    try:
        r=requests.get(url1, auth=(username1, password1))
    except:
        print "Error 100 Opening URL"
        logger.error("Error 100, Could Not Open URL")
    
    if DEBUGGING:
        print "status code : ", r.status_code
        
    thePage = r.text
    entirePage = thePage.split('\n')
    macFound=''
    matchFound=0
    printed=0
    for line in entirePage:
        '''
        Search for the two lines lines (the mac is a dynamic field), we may also want to log the associations (attempted connections)
        var assocList='assoclist 88:32:9B:7B:A2:D4';
        var authoList='autho_sta_list 88:32:9B:7B:A2:D4';
        '''
        
        matchMac=re.search(repattern, line)
        matchAuth=re.search(authoList, line)
        if matchMac and matchAuth:
            '''
            match=re.search()
            if match:
                matchFound=1
                if DEBUGGING:
                    print "authoList hit found on this line: ", line
            '''
            match1=re.search(repattern, line)
            if match1:
                matchFound=1
                macAddress=line[match1.start():match1.end()]
                
                if DEBUGGING:
                    print "\n\nmacAddress from line: authoList : ", macAddress, "\n\n"
                if not printed:
                    printed=1
                    print "\n", macAddress, "\n"
                macFound=macAddress
    
    if 1==matchFound:
        logEntry="found : "+macFound
        logger.error(logEntry)
        macList.append(macFound)
        changePassword(username, password, logger)

if __name__ == '__main__':
    import requests, re, logging, time, sys
    DEBUGGING=0
    FOREVER=1

    counter=0
    url = "http://192.168.0.227/cgi-bin/stalist.html"
    username = 'admin'
    password = 'password'
    logFileName = 'r0ut3rhunt3r.txt'
    logger=logging.getLogger('r0ut3rhunt3r')
    logHdlr = logging.FileHandler('./r0ut3rhunt3r.txt')
    logFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logHdlr.setFormatter(logFormatter)
    logger.addHandler(logHdlr)
    logger.setLevel(logging.WARNING)
    
    print "Application Started\n"
    while FOREVER:
        if counter > 40:
            counter=0
            sys.stdout.write('\n.')
        else:
            sys.stdout.write('.')
        counter=counter+1
        check4ConnectionsR(url, username, password, logger)
        time.sleep(1)

#
#
#
