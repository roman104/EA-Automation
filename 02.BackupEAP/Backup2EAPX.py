# Backup Automation
# version 1.0
# author: Roman Kazicka  inspired by Maros Zvolensky
# Scope: automation script that will perform project transfer based on config file
# Sources: Sparxsystems, enterprise-architect-object-model.pdf
# Name: Backup EA model into EAPX files
# Description: Automate routine backups from client side into EAPX files, Native Format, other DBMS repository
# Inputs:  Configuration file
# Date: 20201201
# change log

# Last change: 20210107
# Descrition of last change
# - creation the app stucture - function definition 

#
# imported libraries
import yaml
import configparser  # call config parser
import time  # to get timestamp
import win32com.client #to be able to call sparx api
import os # to work with directories
import sys
import traceback
import subprocess #to be able to start sparx
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
#import  "F:\\Root\\roman\\01.Agnicoli\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\02.BackupEAP\\Backup2EAPX\\BackupsUtils.py"
# TODO - How to set up Python env to make own modules?
#import  ".\\BackupsUtils"
#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose: read command to be performed - optional

#00. Init application
# definition of global variables
    #Main Configuration file
        #todo = how to make relative path to the config
MyConfigFile="A:\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\02.BackupEAP\\BackupConfig-All.yml" 

#MyConfigFile='r.\BackupConfig.yml' 
MyConfigRepo=None
eaApp=None      # activeX handler
MyRepository=None # Handler to the current repository EA object 
#MySourcesList=  #type <List of str> of Connection Strings suitable for API
MyConnectionsList = [] # type <list> list of connection string from Model Shortcuts
MyRepositoryList = []  # Type Lis of Dictionary, complete list of all repositories with all parameters
RepositoyID=""  #Important for Export To Native- folder name    <MyDestinationFolderNATIVE>\<RepositoryID>
MyDestinationFolderRoot ="1234"   # type <str> in case of EAPX target , it is root folder for backups
MyDestinationFolderEAPX =""     # <MyDestinationFolderRoot>\<YYYYMMDD>\<EAPX>
MyDestinationFolderNATIVE=""    #  <MyDestinationFolderRoot>\<YYYYMMDD>\<NATIVE>
DestinationFolderWithDate = ""   # <MyDestinationFolderRoot>\<YYYYMMDD>
MySourceString = ""       #Sparx scope- onnection string for source, this string is model shortcut string generated from EA
MyDestinationString = ""  #Sparx scope- Connection string to Destination
MyLogFile =  ""           #Sparx scope- Name of Logfile  <DestinationName>_<YYYYMMDD-HHMM>.EAPX
                            # destination name is derived from MySourceString <Location><ModelID-xxx><shortName> e.g.QNAP-011_ea_astro_chrono_graph 
MyLogFilePostfix = "_LogFile"   # Name of Logfile <DestinationName><MyLogFilePostFix>_<YYYYMMDD-HHMM>_.TXT
MyJournal =  ""           #Backup Scope - Name of Journal file: <DestinationName><MyJournal><MyJournalPostfix>_<YYYYMMDD-HHMM>.TXT
MyJournalPostfix = "_Journal" #
MyOutputFormat=[] #list of formats
# Developing Variables
Version = 'Demo' # Release, # this variable stands for controling the flow during development and release.
#Version = 'Release'
MY_ADDRESS = 'webadmin@agnicoli.org'
PASSWORD = '123456'
# Tracking, debugging
    #- Levels:
        #- 0 - all information 
        #- 1 - restricted
        #- 2 - more restricted
        #- -1 - no information
TrackingLevel = 0  
MyJournalFileFolder=""    # Finame to journal file - logfile for the whole process of backup
MyJournalFile =""

# ============================
#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose: read command to be performed - optional

# Init variables, paths to config file
def initBackup():
    global eaApp
    global MyConfigFile
    global MyJournalFile

    print("\t\t\t>>>>>>>>> EA Backup Version =  {}  <<<<<<<<<<<<<<<<".format(Version).upper())
    progressTracking("Backup Init")
    progressTracking("Main Config file="+MyConfigFile)
    progressJournal("\t\t\t>>>>>>>>> EA Backup Version =  {}  <<<<<<<<<<<<<<<<".format(Version).upper())
    progressJournal("Backup Init\n"+"Main Config File="+MyConfigFile)
    #-----------------------------------------------------------------EA 
    if(Version=='Release'):
        eaApp = win32com.client.Dispatch("EA.App") #call EA application
      
    else:
       True
    
    return
 
 # ==============================================
#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose: read command to be performed - optional
#01. Read Config file
# read the models to be backuped

def readConfigFile():

    global MyDestinationFolderRoot
    #global MySourcesList
    global MyConnectionsList
    global MyRepositoryList
    global MyOutputFormat
    global MyDestinationFolderEAPX 
    global MyDestinationFolderNATIVE
    global MyJournalFileFolder
    global MyJournalFile
    progressTracking("Read Config")
    MyConfigRepo = read_yaml(MyConfigFile)
     # read the config yaml
        # pretty print my_config
    #pprint.pprint(my_config)
    # print raw data from yaml file
    if(Version=='Demo'):
        print("------------------------------------------------")
        print("# Raw data:\n",MyConfigRepo,"\n")
    i=0
    #go through all items at 1st level
    for item, doc in MyConfigRepo.items():
        if(Version=='Demo'):print("##Item, doc:\n",i,"=",item, ":", doc,"\n")
        i=i+1
        #go trough all items in Source level
        if(item == 'Sources'):
            j=1
            MyRepositoryList.append(doc)
            for item1  in doc:
                if(Version=='Demo'):print("\ttype=",type(item),"###Source:",j,"=",item1)
                #MyConnectionsList.append(doc[item1]["ToBeBackuped"])
                #(doc[item1]["Description"])
                MyConnectionsList.append(doc[item1]["ConnectionString"])
                
                
                j=j+1
        elif (item=='Destinations'):
            MyDestinationFolderRoot=doc["DestinationFolderRoot"]
            MyDestinationFolderEAPX=MyDestinationFolderRoot+'\\'+'EAPX'
            MyDestinationFolderNATIVE=MyDestinationFolderRoot+'\\'+'NATIVE'
            MyJournalFileFolder=doc["MyJournalFile"]
            MyJournalFile=MyJournalFileFolder+"\\"+time.strftime('%Y%m%d')+"_"+"Backup_LogFile"+".txt"
            ExistDestinationDir(MyJournalFileFolder)
        elif (item=='Destination Type'):
            MyOutputFormat=doc

    l=0
    for s in MyConnectionsList:
        if(Version=='Demo'):print("#ListOfSources:",l,"=",s)
        l=l+1
    if(Version=='Demo'):print("=======================Config File Has been red==================================")
    if(Version=='Demo'):print ("MyJornalFile=",MyJournalFile)
    progressJournal("MyJournalFile="+MyJournalFile)
    return

# =============================================
# ----------------------------------------------------

# send mail
#-------------------------------------------------------------
# 
# name: notification
# Date:
# Purpose: just copy and pASTE if you need new function
def notification():
    progressTracking("Perform notification")
    progressJournal("Perform notification")

    return
# =====================================
# ------------------------------------------
# close
#-------------------------------------------------------------
# Template function=========================
# ----------------------------------------------------
# 
#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose: read command to be performed - optional
def readCmds():
    progressTracking("Read Commands")
    progressJournal("Read Commands")

    return
#=============================================
# ----------------------------------------------------
#  perfoms command
# cmds:
# - backup to EAPs
# - backup to DBMS
# - notification
# - log of the all activities
def performActions(MyAction=""):
    global MyJpurnalFile
    progressTracking("Perform Actions")
    progressJournal("PerformActions")
    cmd="Backup2EAPX"
    cmd=MyAction
    if (cmd == "Backup2EAPX"):
        exportAllSources2EAPX()
        
    elif (cmd == "Backup2XML"):
        exportAllSources2NativeXML()
               
    else:
        return -1
    return
#==========================================
#-----------------------------------------------
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def closeApp(eaApp):
    progressTracking("Close Application")
    progressJournal("Close Application")
    global MyRepository
    #TODO - close repositories (destination, source)
    #TODO - close ea app reference?
    #eaApp.Close()
    # eaApp.Quit()
    if(Version == 'Release'):
        MyRepository.Exit()
    else:
        a=1
    return 
# ======================================

#--------------------------------------------------------------Backups Utils - candidate to separate modul =START
#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def read_yaml(ConfigFile):
    """ A function to read YAML file"""
    #progressTracking("Read Config")
    with open(ConfigFile) as f:
        config = yaml.safe_load(f)
 
    return config
#-------------------------------------------------------------
#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def transmitDBMS2EAPX(MySourceString, MyDestinationString, MyLogFile, MyJournal ):
    global MyRepository
    global aeApp

    if(Version=='Demo'):
        print("TransmitDBMS2EAPX",MySourceString, MyDestinationString, MyLogFile, MyJournal)  
        print(time.strftime('%Y%m%d%H%M'),MySourceString)
        
    else:
        progressTracking("TransmitDBMS2EAPX starts:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
        progressJournal("TransmitDBMS2EAPX starts:\n"+"MySourceString="+ MySourceString +"\n" \
                    +"MyDestinationString="+MyDestinationString+"\n" \
                    +"MyLogFile="+ MyLogFile+"\n" \
                    + "MyJournal="+MyJournal)
        try:
            
            #REM Transfer Project based on connection string to target file (maybe another connection string)
            MyRepository = eaApp.Repository
            #Repository.Windows()
            Project = MyRepository.GetProjectInterface()
            ret=Project.ProjectTransfer(SourceFilePath=MySourceString, TargetFilePath= MyDestinationString, LogFilePath=MyLogFile)
            
            #TODO JOURNAL shoud contain time measurements, and info for user about progress of backup
        except:
            #error log record to MyJournal file
            progressJournal("TransmitDBMS2EAPX EXCEPTION:\n"+"MySourceString="+ MySourceString )
            progressTracking("TransmitDBMS2EAPX EXCEPTION:\n"+"-"+MySourceString)
            
        progressTracking("TransmitDBMS2EAPX:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
    return
    # ======================================
    #-------------------------------------------------------------

#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose:exportAllSources2NativeXML
def exportAllSources2EAPX ( ):

    for OneRepo in MyRepositoryList[0]:
    
    #  for  OneSource in MyConnectionsList:
        OneSource=MyRepositoryList[0][OneRepo]["ConnectionString"]
        if(MyRepositoryList[0][OneRepo]["ToBeBackuped"]==True):
        #if(MyConnectionsList.doc[item1]["ToBeBackuped"]==True):
            
            MySourceString, MyDestinationString, MyLogFile, MyJournal=prepareParametersForEAPX(OneSource)
            transmitDBMS2EAPX(MySourceString, MyDestinationString, MyLogFile, MyJournal)
        else:
            if(Version=='Demo'):print ('Skipped=',OneSource.split('---')[0])
            progressTracking("Skipped="+OneSource.split('---')[0])
            progressJournal("Skipped="+OneSource.split('---')[0])
    return True
# ======================================
#-------------------------------------------------------------
# 
# name:
# Date: 20210120
# Purpose:
def exportAllSources2NativeXML( ):
    global DestinationFolderWithDate
    global RepositoryID
    for OneRepo in MyRepositoryList[0]:
    
    #  for  OneSource in MyConnectionsList:
        OneSource=MyRepositoryList[0][OneRepo]["ConnectionString"]
        RepositoryID=MyRepositoryList[0][OneRepo]["SourceID"]
        if(MyRepositoryList[0][OneRepo]["ToBeBackuped"]==True):
        #if(MyConnectionsList.doc[item1]["ToBeBackuped"]==True):
            
            MySourceString, MyDestinationString, MyLogFile, MyJournal=prepareParametersForNATIVE(OneSource)
           
            transmitDBMS2Native(MySourceString, MyDestinationString, MyLogFile, MyJournal)
        else:
            if(Version=='Demo'):print ('Skipped=',OneSource.split('---')[0])
            progressTracking("Skipped="+OneSource.split('---')[0])
            progressJournal("Skipped="+OneSource.split('---')[0])

    return True
# ======================================
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def transmitDBMS2Native(MySourceString, MyDestinationString, MyLogFile, MyJournal ):
    global MyRepository
    global aeApp
    global MyDestinationFolderNATIVE
    global RepositoryID
    MyDestinationFolderXMLNATIVE= MyDestinationFolderNATIVE+"\\" + time.strftime('%Y%m%d')+"\\"+ RepositoryID
    
    if(Version=='Demo'):
        print("TransmitDBMS2XMLNative",MySourceString, MyDestinationString, MyLogFile, MyJournal)  
        print(time.strftime('%Y%m%d%H%M'),MySourceString)
        
    else:
        progressTracking("TransmitDBMS2XMLNative:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
        progressJournal("TransmitDBMS2XMLNative:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
        try:
            
            #REM Transfer Project based on connection string to target file (maybe another connection string)
            MyRepository = eaApp.Repository
            #Repository.Windows()
            Project = MyRepository.GetProjectInterface()
            #ret=Project.ProjectTransfer(SourceFilePath=MySourceString, TargetFilePath= MyDestinationString, LogFilePath=MyLogFile)
           
            ret=Project.ExportProjectXML(MyDestinationFolderXMLNATIVE)
            
            
            #TODO JOURNAL shoud contain time measurements, and info for user about progress of backup
        except:
            #error log record to MyJournal file
            progressTracking("TransmitDBMS2NATIVE EXCEPTION:\n"+"-"+MySourceString)
    
    return
    # ======================================

#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def prepareParametersForEAPX(MyOneSource):

# MyDestination file
    #Preparing MyDestination Parameter <DestinationName>_<YYYYMMDD-HHMM>.EAPX
    #EnsureDir(Transfer_Directory)
        #  Transfer_Name = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_' + time.strftime('%Y%m%d%H%M') + '.eapx'
        # Transfer_Log = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_log_' + time.strftime('%Y%m%d%H%M') + '.log'
    global MyDestinationFolderRoot
    global MyDestinationFolderEAPX
    global MyDestinationFolderNATIVE
    global MyJournal
    global DestinationFolderWithDate
   
    a=MyOneSource.split(':')
    b=a[1].split('---')
    ModelName=b[0].strip()
    MyConnectionString=b[1].strip()
    
    ExistDestinationDir(MyDestinationFolderEAPX)
    DestinationFolderWithDate=MyDestinationFolderEAPX + "\\" + time.strftime('%Y%m%d')
    ExistDestinationDir(DestinationFolderWithDate)
    MyDestinationString=DestinationFolderWithDate + '\\' + ModelName + '_' + time.strftime('%Y%m%d-%H%M') + '.eapx'
    MyLogFile=          DestinationFolderWithDate + '\\' + ModelName + '_' + MyLogFilePostfix + '_' + time.strftime('%Y%m%d-%H%M') + '.txt'
    MyJournal=          DestinationFolderWithDate + '\\' + ModelName + '_' + MyJournalPostfix + '_' + time.strftime('%Y%m%d-%H%M') + '.txt'
    #returns   MySourceString, MyDestinationString, MyLogFile, MyJournal
    a=0
    return MyConnectionString,MyDestinationString, MyLogFile,MyJournal
#====================================
#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def prepareParametersForNATIVE(MyOneSource):

# MyDestination file
    #Preparing MyDestination Parameter <DestinationName>_<YYYYMMDD-HHMM>.EAPX
    #EnsureDir(Transfer_Directory)
        #  Transfer_Name = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_' + time.strftime('%Y%m%d%H%M') + '.eapx'
        # Transfer_Log = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_log_' + time.strftime('%Y%m%d%H%M') + '.log'
    global MyDestinationFolderRoot
    global MyDestinationFolderEAPX
    global MyDestinationFolderNATIVE
    global MyJournal
    global DestinationFolderWithDate
   
    a=MyOneSource.split(':')
    b=a[1].split('---')
    ModelName=b[0].strip()
    MyConnectionString=b[1].strip()
    
    ExistDestinationDir(MyDestinationFolderNATIVE)
    DestinationFolderWithDate=MyDestinationFolderNATIVE + "\\" + time.strftime('%Y%m%d')
    ExistDestinationDir(DestinationFolderWithDate)
    MyDestinationString=DestinationFolderWithDate + '\\' + ModelName + '_' + time.strftime('%Y%m%d-%H%M') + '.eapx'
    MyLogFile=          DestinationFolderWithDate + '\\' + ModelName + '_' + MyLogFilePostfix + '_' + time.strftime('%Y%m%d-%H%M') + '.txt'
    MyJournal=          DestinationFolderWithDate + '\\' + ModelName + '_' + MyJournalPostfix + '_' + time.strftime('%Y%m%d-%H%M') + '.txt'
    #returns   MySourceString, MyDestinationString, MyLogFile, MyJournal
    a=0
    return MyConnectionString,MyDestinationString, MyLogFile,MyJournal
#====================================
#-------------------------------------------------------------
# 
# name: ExistDestinationDir
# Date:
# Purpose: If not exists, create one
def ExistDestinationDir (directory):
    # Function to check if a given directory exists, if not, it will create it
    if not os.path.exists(directory):
        os.makedirs(directory)
  

    return True
# ======================================
#-------------------------------------------------------------
# 
# name: send e-mail
# Date:
# Purpose: just copy and pASTE if you need new function
def sendEmail (Message ):
    progressTracking("Send E-mails")
    sender = 'roman.kazicka@systemThinking.sk'
    receiver = ['roman.kazicka@systemThinking.sk']

    message = """From: From Person <roman.kazicka@systemThinking.sk>
    To: To person <roman.kazicka@systemThinking.sk>
    Subject: """+Mail_Subject
    message = message + Mail_message
    try:
        #smtpObj = smtplib.SMTP('smtp.exohosting.com',port=25, timeout=10)
        s = smtplib.SMTP(host='smtp.exohosting.com', port=25, timeout=10)
        msg = MIMEMultipart()       # create a message
        email="webadmin@agnicoli.org"
        s.login("webadmin@agnicoli.org", "")
        #smtpObj.sendmail(sender, receiver, message)
    
    
        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST" + time.strftime('%Y%m%d%H%M')
            
            # add in the message body
        msg.attach(MIMEText(message, 'plain'))
            
            # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
        # Terminate the SMTP session and close the connection
        s.quit()
        print('Successfully sent email')    
    except:
        print('Error: Unable to send email')

    return True
# ======================================
#-------------------------------------------------------------
# 
# name: Progress Tracking
# Date: 20210119
# Purpose: Inform User about progress. Main use case is to put information on screen.
def progressTracking ( msg):
    global TrackingLevel
    if(TrackingLevel==0):
        print( time.strftime('%Y%m%d-%H:%M-%S'), ":",msg)
    elif():
        True
    elif():
        True
    else:
        True

    return True
# ======================================
#-------------------------------------------------------------
# 
# name: Progress Yournal-log file
# Date: 202101
# Purpose: Inform User about progress. Main use case is to put information on screen.
def progressJournal ( msg):
    global TrackingLevel
    global MyJournalFile
    f=open(MyJournalFile,"a")
           #print( time.strftime('%Y%m%d-%H:%M-%S'), ":",msg)
    f.write(time.strftime('%Y%m%d-%H:%M-%S')+ ":"+msg+"\n")
    
    f.close()
    return True
# ======================================
#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def template ( ):
  

    return True
# ======================================
#=============================================================  END of MODUL


# -------------------------------------------- main
def myMain():
    readConfigFile()
    initBackup()
    
    readCmds()
    performActions("Backup2EAPX")
    performActions("Backup2XML")
    notification()
    closeApp(eaApp)
    return 


if __name__ == '__main__':
    myMain()