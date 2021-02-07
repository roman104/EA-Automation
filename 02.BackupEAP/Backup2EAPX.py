# Backup Automation
# version 1.0
# author: Roman Kazicka  inspired by Maros Zvolensky
# copyright: ** IMPORTANT NOTICE: All procedures, workflow, 
#  used in this program are Copyright (C) 2021 by
#  Roman Kazicka (Roman.Kazicka@agnicoli.org, http://www.agnicoli.org).
#  Permission is granted to freely use, modify, and distribute these
#  routines provided these credits and notices remain unmodified with any
#  altered or distributed versions of the program.

# Scope: automation script that will perform project transfer based on config file
# Sources: Sparxsystems, enterprise-architect-object-model.pdf
# Name: Backup EA model into EAPX files
# Description: Automate routine backups from client side into EAPX files, Native Format, other DBMS repository
# Inputs:  Configuration file= 
# TODO
    #- Rough Statistics - How much sourcess in Logfile, How Much to be skipped, Reult-How much nackupd successufully, How much Skipped, How Much errors
    #- E-mail notification
# Date: 20201201
# change log

# LAst Change: 
#20210207- Issues:
    #- Export to NATIve - Duration is 0
    # improvemets :
        # - add size of backup (EAPX), or size of Folder (2Native) in Journal
#20210204-
# Issues:
#   1 - EAPX > 2GB
#   2 - NATIVE - onlu for ODBC  
# 20210127:
#   - added tracking and journals missing code
# 20210122
#   journal, progress tracking tuning
# # change: 20210107
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
from timeit import default_timer as timer

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
MyConfigFile="M:\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\02.BackupEAP\\BackupConfig-All.yml" 


#MyConfigFile='r.\BackupConfig.yml' 
MyConfigRepo=None
eaApp=None      # activeX handler
MyRepository=None # Handler to the current repository EA object 
MyProject = None # Handler to EA Object
#MySourcesList=  #type <List of str> of Connection Strings suitable for API
MyConnectionsList = [] # type <list> list of connection string from Model Shortcuts
MyRepositoryList = []  # Type Lis of Dictionary, complete list of all repositories with all parameters
RepositoryID=""  #Important for Export To Native- folder name    <MyDestinationFolderNATIVE>\<RepositoryID>
MyDestinationFolderRoot ="1234"   # type <str> in case of EAPX target , it is root folder for backups
MyDestinationFolderEAPX =""     # <MyDestinationFolderRoot>\<YYYY>\<EAPX>\<YYYYMMDD>
MyDestinationFolderNATIVE=""    #  <MyDestinationFolderRoot>\<YYYY><NATIVE>\<YYYYMMDD>
#DestinationFolderWithDate = ""   # <MyDestinationFolderRoot>\<YYYYMMDD>-local variable
MySourceString = ""       #Sparx scope- onnection string for source, this string is model shortcut string generated from EA
MyDestinationString = ""  #Sparx scope- Connection string to Destination
MyLogFile =  ""           #Sparx scope- Name of Logfile  <DestinationName>_<YYYYMMDD-HHMM>.EAPX
                            # destination name is derived from MySourceString <Location><ModelID-xxx><shortName> e.g.QNAP-011_ea_astro_chrono_graph 
MyLogFilePostfix = "_LogFile"   # Name of Logfile <DestinationName><MyLogFilePostFix>_<YYYYMMDD-HHMM>_.TXT
MyJournal =  ""           #Backup Scope - Name of Journal file: <DestinationName>\<YYYY>\<MyJournals><MyJournalPostfix>_<YYYYMMDD-HHMM>.TXT
MyJournalPostfix = "_Journal" #
MyOutputFormat=[] #list of formats
BackupStatistics = {} # Statistics about Backup Process, <RepoID>, <start>, <end>,<duration>, <Result ><format>  
#       {1: }
# Developing Variables
Version = 'Release'
#Version = 'Demo' # Release, # this variable stands for controling the flow during development and release.
            # all EA components calls are skipped for better debuggingVersion = 'Release'

Success=True  # Global variable for recognition return from methods from EA library
           # it is not clear for me now what measn return values, if it has any meaning
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
#DestinationConnectionString="EAConnectString:QNAP-011_BAK --- DBType=0;Connect=Provider=MSDASQL.1;Persist Security Info=False;Data Source=QNAP-011_BAK;LazyLoad=1;"
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
    global MyProject
    global MyRepository

    print("\t\t\t>>>>>>>>> EA Backup Version =  {}  <<<<<<<<<<<<<<<<".format(Version).upper())
    progressTracking("Backup Init")
    progressTracking("Main Config file="+MyConfigFile)
    progressJournal("\t\t\t>>>>>>>>> EA Backup Version =  {}  <<<<<<<<<<<<<<<<".format(Version).upper())
    progressJournal("Backup Init\n"+"Main Config File="+MyConfigFile)
    #-----------------------------------------------------------------EA 
    if(Version=='Release'):
        eaApp = win32com.client.Dispatch("EA.App") #call EA application
      #REM Transfer Project based on connection string to target file (maybe another connection string)
        MyRepository = eaApp.Repository
            #Repository.Windows()
       # MyProject = MyRepository.GetProjectInterface()
            #ret=Project.ProjectTransfer(SourceFilePath=MySourceString, TargetFilePath= MyDestinationString, LogFilePath=MyLogFile)
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
    global Version
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
        progressTracking("##Item, doc:\n"+str(i)+"="+str(item)+ ":"+ str(doc)+"\n")
        #progressJournal("##Item, doc:\n"+str(i)+"="+str(item)+ ":"+ str(doc)+"\n")--
        i=i+1
        #go trough all items in Source level
        if(item == 'Sources'):
            j=1
            MyRepositoryList.append(doc)
            for item1  in doc:
                progressTracking("\ttype="+str(type(item))+"###Source:"+str(j)+"="+str(item1))
                #MyConnectionsList.append(doc[item1]["ToBeBackuped"])
                #(doc[item1]["Description"])
                MyConnectionsList.append(doc[item1]["ConnectionString"])
                
                
                j=j+1
        elif (item=='Destinations'):
            MyDestinationFolderRoot=doc["DestinationFolderRoot"]
            MyDestinationFolderEAPX=MyDestinationFolderRoot+"\\"+time.strftime('%Y')+'\\'+'EAPX'
            MyDestinationFolderNATIVE=MyDestinationFolderRoot+"\\"+time.strftime('%Y')+'\\'+'NATIVE'
            MyJournalFileFolder=doc["MyJournalFile"]+"\\"+time.strftime('%Y')+"\\"+"Journals"
            MyJournalFile=MyJournalFileFolder+"\\"+time.strftime('%Y%m%d')+"_"+"Backup_LogFile"+".txt"
            ExistDestinationDir(MyJournalFileFolder)
        elif (item=='Destination Type'):
            MyOutputFormat=doc

    l=0
    for s in MyConnectionsList:
        progressTracking("#ListOfSources:"+str(l)+"="+str(s))
        l=l+1
    progressTracking("=======================Config File Has been red==================================")

    progressTracking("MyJornalFile="+MyJournalFile)
    progressJournal("Config File Has been red")
    progressJournal("----------------------------------------Backup started")
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
        exportAllSources_2_EAPX()
        
    elif (cmd == "Backup2XML"):
        exportAllSources_2_Native_XML()
               
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
    progressTracking("===========================================Backup Ended")
    progressJournal("=============================================Backup Ended")
    return 
# ======================================

#--------------------------------------------------------------Backups Utils - candidate to separate modul =START
#-------------------------------------------------------------
#  function
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
#  function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def TransmitDBMS_2_EAPX(MySourceString, MyDestinationString, MyLogFile, MyJournal ):
    global MyRepository
    global MyProject
    global aeApp
    global RepositoryID
    global Success
    SizeOfFile=-1
    ret=Success # for Demo purpose
    progressTracking("TransmitDBMS_2_EAPX starts:\t"+"-----------------------------------"+RepositoryID+ "----->START"+"\n\t" \
                     +MySourceString+"\n\t"+ MyDestinationString+"\n\t"+ MyLogFile+"\n\t"+ MyJournal)
    progressJournal("TransmitDBMS_2_EAPX starts:\t"+"-----------------------------------"+RepositoryID+ "----->START"+"\n\t"+"MySourceString"+MySourceString +"\n\t" \
                    +"MyDestinationString="+MyDestinationString+"\n\t" \
                    +"MyLogFile="+ MyLogFile+"\n\t" \
                    + "MyJournal="+MyJournal)
    
    #     print("TransmitDBMS_2_EAPX starts:\n"+"MySourceString=" + MySourceString + "\n"
    #           + "MyDestinationString="+MyDestinationString+"\n"
    #           + "MyLogFile=" + MyLogFile+"\n"
    #           + "MyJournal="+MyJournal)
    #     print(time.strftime('%Y%m%d%H%M'), MySourceString)
        
    
        
    try:
            
            #REM Transfer Project based on connection string to target file (maybe another connection string)
        #    MyRepository = eaApp.Repository
            #Repository.Windows()
        #    Project = MyRepository.GetProjectInterface()
            if(Version == 'Release'):
                ret1=MyRepository.OpenFile(MySourceString)
                ret2=MyProject.ExportProjectXML(MyDestinationFolderXMLNATIVE)
                ret3=MyProject.ProjectTransfer(SourceFilePath=MySourceString, TargetFilePath= MyDestinationString, LogFilePath=MyLogFile)
                ret4=Myproject.CloseFile()
            else:
                time.sleep(1)   
                #TODO JOURNAL shoud contain time measurements, and info for user about progress of backup
                #TODO get size of file
            
           
    except:
            #error log record to MyJournal file
            progressJournal("TransmitDBMS_2_EAPX EXCEPTION:\n"+"MySourceString="+ MySourceString )
            progressTracking("TransmitDBMS_2_EAPX EXCEPTION:\n"+"-"+MySourceString)
    SizeOfFile=getFileSize(MyDestinationString)       
    #progressTracking("TransmitDBMS_2_EAPX:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
    if(ret==Success):
        progressTracking("TransmitDBMS_2_EAPX:\t"+"-"+RepositoryID+":"+"\t>SizeOfFile="+str(SizeOfFile)+"\t<\texported successfuly")
        progressJournal("TransmitDBMS_2_EAPX :\t"+ RepositoryID+":"   +"\t>SizeOfFile="+str(SizeOfFile)+"\t<\texported successfuly")
    else:
        progressTracking("TransmitDBMS_2_EAPX:\t"+"-"+RepositoryID+":"+"!!!!!!ERROR During EXPORT!!!!!")
        progressJournal("TransmitDBMS_2_EAPX :\t"+ RepositoryID+":"+"!!!!!!ERROR During EXPORT!!!!!")

    return ret1 & ret2 & ret3 & ret4, SizeOfFile
    # ======================================
    #-------------------------------------------------------------

#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose:exportAllSources2NativeXML
def exportAllSources_2_EAPX ( ):
    global RepositoryID
    startTimeAll=timer()# =time.strftime('%Y%m%d%H%M,%S')
    endTimeAll= timer()
    startTime=timer()
    endTime=timer()   
    duration= endTime-startTime
    durationAll=timer()
    for OneRepo in MyRepositoryList[0]:
        startTime=timer()
        progressTracking(" _________________________ XML ITEM="+str(OneRepo)+":<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        progressJournal(" ___________________________XML ITEM="+str(OneRepo)+":<<<<<<<<<<<<<<<<<<<<<<<<")
          
    #  for  OneSource in MyConnectionsList:
        OneSource=MyRepositoryList[0][OneRepo]["ConnectionString"]
        RepositoryID=MyRepositoryList[0][OneRepo]["SourceID"]
        if (MyRepositoryList[0][OneRepo]["ToBeBackuped"]==True and "EAPX" in MyRepositoryList[0][OneRepo]["Actions"]):
        #if(MyConnectionsList.doc[item1]["ToBeBackuped"]==True):
            MySourceString, MyDestinationString, MyLogFile, MyJournal=prepareParametersForEAPX(OneSource)
            ret, Size=TransmitDBMS_2_EAPX(MySourceString, MyDestinationString, MyLogFile, MyJournal)
            endTime= timer()  
            duration=endTime-startTime
            progressTracking(" \t\tDuration="+elapsedTime(startTime,endTime, duration))
            progressJournal(" \t\tDuration="+elapsedTime(startTime,endTime, duration))
            statisticsCollectData ( ">\tItem= "+str(OneRepo), RepositoryID,startTime, endTime,duration, ret, "EAPX")
          
        else:
            
            progressTracking(" _______________________  Skipped="+RepositoryID)
            progressJournal("  _______________________  Skipped="+RepositoryID)
        
    endTimeAll=timer()
    durationAll=endTimeAll-startTimeAll    
    progressTracking(" \t\tDuration All EAPX="+elapsedTime(startTimeAll,endTimeAll, durationAll))
    progressJournal(" \t\tDuration All EAPX ="+elapsedTime(startTimeAll,endTimeAll, durationAll))
    statisticsCollectData ( ">\tAll Items Sumamry= ", "SUM",startTimeAll, endTimeAll,durationAll, Success, Size,"EAPX SUMMARY")
    return True
# ======================================
#-------------------------------------------------------------
# 
# name:
# Date: 20210120
# Purpose:
def exportAllSources_2_Native_XML( ):
    global DestinationFolderWithDate
    global RepositoryID
    startTimeAll=timer()
    endTimeAll= timer()
    startTime=timer()
    endTime=timer()   
    duration= endTime-startTime
    durationAll=timer()
    for OneRepo in MyRepositoryList[0]:
        startTime=timer()
        progressTracking(" _________________________ XML ITEM="+str(OneRepo)+":<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        progressJournal(" ___________________________XML ITEM="+str(OneRepo)+":<<<<<<<<<<<<<<<<<<<<<<<<")
          
    #  for  OneSource in MyConnectionsList:
        OneSource=MyRepositoryList[0][OneRepo]["ConnectionString"]
        RepositoryID=MyRepositoryList[0][OneRepo]["SourceID"]
        if(MyRepositoryList[0][OneRepo]["ToBeBackuped"]==True):
            
        #if(MyConnectionsList.doc[item1]["ToBeBackuped"]==True):
            
            MySourceString, MyDestinationString, MyLogFile, MyJournal=prepareParametersForNATIVE(OneSource)
            
            ret, Size= transmitDBMS_2_Native(MySourceString, MyDestinationString, MyLogFile, MyJournal)

            endTime= timer()  
            duration=endTime-startTime
            progressTracking(" \t\tDuration="+elapsedTime(startTime,endTime, duration))
            progressJournal(" \t\tDuration="+elapsedTime(startTime,endTime, duration))
            statisticsCollectData ( ">\tItem= "+str(OneRepo), RepositoryID,startTime, endTime,duration, ret,Size, "NATIVE_XML")
        else:
            
            progressTracking(" _________________________ Skipped="+RepositoryID)
            progressJournal(" ___________________________Skipped="+RepositoryID)
        
    endTimeAll=timer()
    durationAll=endTimeAll-startTimeAll    
    progressTracking(" \t\tDuration All NATIVE="+elapsedTime(startTimeAll,endTimeAll, durationAll))
    progressJournal(" \t\tDuration All NATIVE ="+elapsedTime(startTimeAll,endTimeAll, durationAll))
    statisticsCollectData ( ">\tAll Items Sumamry= ", "SUM",startTimeAll,endTimeAll,durationAll, Success, Size, "EAPX SUMMARY")
    return True
# ======================================
#  function
# name: transmitDBMS_2_Native
# Date: 20210131
# Purpose: 
def transmitDBMS_2_Native(MySourceString, MyDestinationString, MyLogFile, MyJournal ):
    global MyRepository
    global MyProject
    global aeApp
    global MyDestinationFolderNATIVE
    global RepositoryID
    global Success
    SizeOfFolder=-1
    ret=False
    #MyDestinationFolderXMLNATIVE= MyDestinationFolderNATIVE+"\\" + time.strftime('%Y%m%d')+"\\"+ RepositoryID
    MyDestinationFolderXMLNATIVE=MyDestinationString
    ExistDestinationDir(MyDestinationFolderXMLNATIVE)
    progressTracking("  >>>>>>>>>>>>>>>>>>>>>TransmitDBMS2_NATIVE_XML starts:\t"+"------------------------------------"+RepositoryID+ "----->START"+"\n\t" \
                    +MySourceString+"\n\t"+ MyDestinationString+"\n\t"+ MyLogFile+"\n\t"+ MyJournal)
    progressJournal(">>>>>>>>>>>>>>>>>>>>>>>>TransmitDBMS2_NATIVE_XML starts:\t"+"------------------------------------"+RepositoryID+ "----->START"+"MySourceString="+ MySourceString +"\n\t" \
                    +"MyDestinationString="+MyDestinationString+"\n\t" \
                    +"MyLogFile="+ MyLogFile+"\n\t" \
                    + "MyJournal="+MyJournal)
    #progressTracking("TransmitDBMS2XMLNative:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
    #progressJournal("TransmitDBMS2XMLNative:\n"+"-"+MySourceString+"-"+MyDestinationString+"-"+ MyLogFile+"-"+ MyJournal)
    
        
    try:
        
        #REM Transfer Project based on connection string to target file (maybe another connection string)
    #    MyRepository = eaApp.Repository
        #Repository.Windows()
    #    Project = MyRepository.GetProjectInterface()
        #ret=Project.ProjectTransfer(SourceFilePath=MySourceString, TargetFilePath= MyDestinationString, LogFilePath=MyLogFile)
        if(Version=='Release'):
            ret1=MyRepository.OpenFile(MySourceString)
            ret=MyProject.ExportProjectXML(MyDestinationFolderXMLNATIVE)
            ret2=Myproject.CloseFile()
               
        else:
                time.sleep(1)
        #TODO JOURNAL shoud contain time measurements, and info for user about progress of backup
        #TODO get size of file
        
         
    except:
        #error log record to MyJournal file
        progressTracking("#########   TransmitDBMS2_NATIVE EXCEPTION:\n"+"#######"+MySourceString)
        progressJournal(" #########   TransmitDBMS2_Native EXCEPTION:\n"+"######"+"MySourceString="+ MySourceString )
    
    SizeOfFolder=getFolderSize(MyDestinationFolderXMLNATIVE)
    
    if(ret==Success):
        progressTracking("TransmitDBMS2_NATIVE_XML:\t"+"-"+RepositoryID+":"+"\t>SizeOfFolder="+str(SizeOfFolder)+"\t<\texported successfuly")
        progressJournal("TransmitDBMS2_NATIVE_XML :\t"+ RepositoryID+":"   +"\t>SizeOfFolder="+str(SizeOfFolder)+"\t<\texported successfuly")
    else:
        progressTracking("TransmitDBMS2_NATIVE_XML:\t"+"-"+RepositoryID+":"+"!!!!!!ERROR During EXPORT!!!!!")
        progressJournal("TransmitDBMS2_NATIVE_XML :\t"+ RepositoryID+":"+"!!!!!!ERROR During EXPORT!!!!!")

           
    return ret,SizeOfFolder
    # ======================================
 
            
            
        

#-------------------------------------------------------------
# function
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
    MyDestinationString=DestinationFolderWithDate + '\\' + ModelName + '_' + time.strftime('%Y%m%d-%H%M')  + '.eapx'
    MyLogFile=          DestinationFolderWithDate + '\\' + ModelName + '_' + MyLogFilePostfix + '_' + time.strftime('%Y%m%d-%H%M') + '.txt'
    MyJournal=          DestinationFolderWithDate + '\\' + ModelName + '_' + MyJournalPostfix + '_' + time.strftime('%Y%m%d-%H%M') + '.txt'
    #returns   MySourceString, MyDestinationString, MyLogFile, MyJournal
    a=0
    return MyConnectionString,MyDestinationString, MyLogFile,MyJournal
#====================================
#-------------------------------------------------------------
#  function
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
    global RepositoryID
    a=MyOneSource.split(':')
    b=a[1].split('---')
    ModelName=b[0].strip()
    MyConnectionString=b[1].strip()
    
    ExistDestinationDir(MyDestinationFolderNATIVE)
    DestinationFolderWithDate=MyDestinationFolderNATIVE + "\\" + time.strftime('%Y%m%d')+"\\"+time.strftime('%Y%m%d-%H%M')+'--'+RepositoryID
    ExistDestinationDir(DestinationFolderWithDate)
    ExistDestinationDir(MyDestinationFolderNATIVE)
    
    MyDestinationString=DestinationFolderWithDate 
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
#  function
# name: GetFolderSize
# Date:20210207
# Purpose: calculate result of backuped folder
def getFolderSize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size  

# ======================================
#-------------------------------------------------------------
#  function
# name: getFileSize
# Date: 20210207
# Purpose: backup file size
def getFileSize ( fileName= '.'):
    try:
        fileSize=os.stat(fileName).st_size
    except:
        fileSize=-1
    return fileSize
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
    Mail_Subject=""
    Mail_message=""
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
# name: Time Duration 
# Date:20210204
# Purpose: return time duration in HH:MM:SS
def elapsedTime (myStartTime, myEndTime, myDuration ):
    float_time = 0.6  # in minutes
    hours, seconds = divmod(myDuration , 3600)  # split to hours and seconds
    minutes, seconds = divmod(seconds, 60)  # split the seconds to minutes and seconds
    duration = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
    return duration
# ======================================
#-------------------------------------------------------------
# 
# name: statistics-ColelctData
# Date: 202101
# Purpose: collect data for final statistics
# Statistics about Backup Process, <RepoID>, <start>, <end>,<duration>, <Result ><format>  
def statisticsCollectData ( MyRecordDescription, MyRepoID,MyStartTime, MyEndTime,MyDuration, MySize, MyResult, MyOutputFormat):
    global TrackingLevel
    global MyJournalFile
    global BackupStatistics
    if(MyResult==Success):
        Result="OK"
    else:
        Result="ERROR"
    progressTracking(MyRecordDescription+"\t"+"-"+MyRepoID+":"+"\tStart="+str(MyStartTime)+"\tEndTime="+str(MyEndTime)+"\tDuration="+str(MyDuration)+"\tSize="+str(MySize)+"\tResult="+str(Result)+"\tFormat="+MyOutputFormat)
    progressJournal(MyRecordDescription+"\t"+"-"+MyRepoID+":"+"\tStart="+str(MyStartTime)+"\tEndTime="+str(MyEndTime)+"\tDuration="+str(MyDuration)+"\tSize="+str(MySize)+"\tResult="+str(Result)+"\tFormat="+MyOutputFormat)
    return True
# ======================================
#-------------------------------------------------------------
# 
# name: statistics-Store Data
# Date: 202101
# Purpose: collect data for final statistics
def statisticsStoteData ( msg):
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
   # performActions("Backup2EAPX")

    performActions("Backup2XML")
    notification()
    closeApp(eaApp)
    return 


if __name__ == '__main__':
    myMain()
