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
MyConfigFile="A:\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\02.BackupEAP\\BackupConfig.yml" 

#MyConfigFile='r.\BackupConfig.yml' 
MyConfigRepo=None
eaApp=None      # activeX handler
MyRepository=None # Handler to the current repository EA object 
MySourcesList=[]  #type <List of str> of Connection Strings to be backuped
MyDestinationFolderRoot ="1234"   # type <str> in case of EAPX target , it is root folder for backups
MyDestinationFolderEAPX =""     # <MyDestinationFolderRoot>\<EAPX>
MyDestinationFolderNATIVE=""    #  <MyDestinationFolderRoot>\<NATIVE>
MySourceString = ""       #Sparx scope- onnection string for source, this string is model shortcut string generated from EA
MyDestinationString = ""  #Sparx scope- Connection string to Destination
MyLogFile =  ""           #Sparx scope- Name of Logfile  <YYYYMMDD-HHMM>_<DestinationName>.EAPX
                            # destination name is derived from MySourceString <Location><ModelID-xxx><shortName> e.g.QNAP-011_ea_astro_chrono_graph 
MyLogFilePostfix = "_LogFile"   # Name of Logfile <YYYYMMDD-HHMM>_<DestinationName><MyLogFilePostFix>.TXT
MyJournal =  ""           #Backup Scope - Name of Journal file: <YYYYMMDD-HHMM>_<DestinationName><MyJournal><MyJournalPostfix>.TXT
MyJournalPostfix = "_Journal" #
MyOutputFormat=[] #list of formats
# Developing Variables
Version = 'Demo' # Release, # this variable stands for controling the flow during development and release.
# ============================
#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose: read command to be performed - optional

# Init variables, paths to config file
def initBackup():

    print("\t\t\t>>>>>>>>> EA Backup Version =  {}  <<<<<<<<<<<<<<<<".format(Version).upper())
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
    global MySourcesList
    global MyOutputFormat
    global MyDestinationFolderEAPX 
    global MyDestinationFolderNATIVE
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
            for item1  in doc:
                MySourcesList.append(doc[item1]["ConnectionString"])
                if(Version=='Demo'):print("\ttype=",type(item),"###Source:",j,"=",item1)
                j=j+1
        elif (item=='Destinations'):
            MyDestinationFolderRoot=doc["DestinationFolderRoot"]
            MyDestinationFolderEAPX=MyDestinationFolderRoot+'\\'+'EAPX'
            MyDestinationFolderNATIVE=MyDestinationFolderRoot+'\\'+'NATIVE'
        elif (item=='Destination Type'):
            MyOutputFormat=doc

    l=0
    for s in MySourcesList:
        if(Version=='Demo'):print("#ListOfSources:",l,"=",s)
        l=l+1
    print("=======================Config File Has been red==================================")
    return

# =============================================
# ----------------------------------------------------

# send mail
#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def notification():
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
    return
#=============================================
# ----------------------------------------------------
#  perfoms command
# cmds:
# - backup to EAPs
# - backup to DBMS
# - notification
# - log of the all activities
def performActions():
    cmd='Backup2EAPX'
    if (cmd == 'Backup2EAPX'):
        exportAllSources2EAPX()
        
    elif (cmd == 'Backup2XML'):
        True
               
    else:
        return -1
    return
#==========================================
#-----------------------------------------------
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def closeApp(eaApp):
    #TODO - close repositories (destination, source)
    #TODO - close ea app reference?
    #eaApp.Close()
    # eaApp.Quit()
    if(Version == 'Release'):
       MyRepositor.Exit()
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
    True    
    if(Version=='Demo'):
        print("TransmitDBMS2EAPX",MySourceString, MyDestinationString, MyLogFile, MyJournal)  
    else:
        try:
            
            #REM Transfer Project based on connection string to target file (maybe another connection string)
            Repository = eaApp.Repository
            #Repository.Window()
            Project = Repository.GetProjectInterface()
            ret=Project.ProjectTransfer(SourceFilePath=MySourceString, TargetFilePath= MyDestinationString, LogFilePath=MyLogFile)
            #TODO here could be export to Native Format
            #ExportProjectXML (string DirectoryPath)
        except:
            #error log record to MyJournal file
            A=0
    
    return
    # ======================================
#-------------------------------------------------------------
# 
# name:
# Date:
# Purpose:
def exportAllSources2EAPX ( ):
    
    for  OneSource in MySourcesList:
        MySourceString, MyDestinationString, MyLogFile, MyJournal=prepareParametersForEAPX(OneSource)
        transmitDBMS2EAPX(MySourceString, MyDestinationString, MyLogFile, MyJournal)
    return True
# ======================================
#-------------------------------------------------------------
# 
# name: Export MOdel to XML folder
# Date:
# Purpose: just copy and pASTE if you need new function

def ExportProjectXML ( DirectoryPath) :
# TODO how to define source project - it is current project in memory. Open Project. than export to xml  
# Project,ExportProjectXML()
    return True
# ======================================

#-------------------------------------------------------------
# Template function
# name:
# Date:
# Purpose: just copy and pASTE if you need new function
def prepareParametersForEAPX(MyOneSource):

# MyDestination file
    #Preparing MyDestination Parameter <YYYYMMDD-HHMM>_<DestinationName>.EAPX
    #EnsureDir(Transfer_Directory)
        #  Transfer_Name = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_' + time.strftime('%Y%m%d%H%M') + '.eapx'
        # Transfer_Log = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_log_' + time.strftime('%Y%m%d%H%M') + '.log'
    global MyDestinationFolderRoot
    global MyDestinationFolderEAPX
    global MyDestinationFolderNATIVE
    a=MyOneSource.split(':')
    b=a[1].split('---')
    ModelName=b[0].strip()
    ExistDestinationDir(MyDestinationFolderEAPX)
    MyDestinationString=MyDestinationFolderEAPX+'\\'+ time.strftime('%Y%m%d-%H%M')+'_'+ ModelName + '.eapx'
    #returns   MySourceString, MyDestinationString, MyLogFile, MyJournal
    a=0
    return MyOneSource,'2', '3','4'
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
   
    initBackup()
    readConfigFile()
    readCmds()
    performActions()
    notification()
    closeApp(eaApp)
    return 


if __name__ == '__main__':
    myMain()