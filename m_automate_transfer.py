# m_automation
# version 1.0
# author: Roman Kazicka  based on Maros Zvolensky
# Scope: automation script that will perform project transfer based on config file
# Sources: Sparxsystems, enterprise-architect-object-model.pdf

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
MY_ADDRESS = 'webadmin@agnicoli.org'
PASSWORD = '123456'

def ShoudTaskRun(config_date):
    # Function to check if the task should run
    # Parameters are 0 to 7 where 0 is Monday to 6 Sunday, 7 is each day and are passed in as string
    # Function will return 1 for yes, run, 0 for not to be run as integer
    # by default it will return 0
    # the parameter passed in is a
    shouldrun = False
    if config_date == '7': shouldrun = True
    elif Days_To_Run[int(config_date)] == time.strftime('%A'): shouldrun = True
    return shouldrun

def EnsureDir (directory):
    # Function to check if a given directory exists, if not, it will create it
    if not os.path.exists(directory):
        os.makedirs(directory)
def KillSparx():
    #function to get output from windows command line if the EA is runnung
    cmd = 'taskkill /FI "IMAGENAME eq EA.exe"'
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)



Mail_message1 = 'M_automation status for '+time.strftime('%A')+', '+time.strftime('%d %B %Y')+'\n\n\n'
Mail_Subject = Mail_message1
Mail_message = """Hello guys,
This is an automated message from the script providing information on the status of the automation script.

"""+Mail_message1
Days_To_Run = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','Everyday','Paused']
config = configparser.ConfigParser()
#-----------------------------------------------------------------EA 
eaApp = win32com.client.Dispatch("EA.App") #call EA application
MyConfigFile='A:\26.PrehladModelov\13.Automation\01.Backups\02.Roman\01.BAckup2EAPX\\m_auto_transfer.ini'
#config.read(r'd:\M_Automation\config\m_auto_transfer.ini')  # open cofing file
config.read(r'.\m_auto_transfer.ini')  # open cofing file
#REM read config file
for section in config.sections(): #for each section in the config file
    if config.get(section, 'Task_type') in ['backup']:
        #01.JUST BACKUP
         if ShoudTaskRun(config.get(section, 'Task_Schedule')) :
            print('Now transferring: ',section)
            Task_Schedule = config.get(section, 'Task_Schedule')
            Task_Run = ShoudTaskRun(Task_Schedule)
            Task_info = config.get(section, 'Task_Info')
            Connection_String = r''+config.get(section, 'Connection_String')+''
            Connection_String_Destination=r''+config.get(section, 'Connection_String_Destination')+''
            Transfer_Directory  = r''+config.get(section, 'Transfer_Directory')+''
            EnsureDir(Transfer_Directory)
            Transfer_Name = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_' + time.strftime('%Y%m%d%H%M') + '.eapx'
            Transfer_Log = Transfer_Directory+'\\'+config.get(section, "Transfer_Name") + '_log_' + time.strftime('%Y%m%d%H%M') + '.log'
            string1 = r''+Connection_String+''
            #REM export to File
            string2 = r''+Transfer_Name+''
            #REm Transfer to connection string
            #string2 = r''+Connection_String_Destination+''
            string3 = r''+Transfer_Log+''
            try:
                #REM Transfer Project based on connection string to target file (maybe another connection string)
                Repository = eaApp.Repository
               #Repository.Window()
                Project = Repository.GetProjectInterface()
                ret=Project.ProjectTransfer(SourceFilePath=string1, TargetFilePath= string2, LogFilePath=string3)
                #TODO here could be export to Native Format
                #ExportProjectXML (string DirectoryPath)
                Mail_message = Mail_message+'\nTask: ' + section + '\nRun : SUCCESS\n\nFiles stored in: '+Transfer_Directory+'\n\n'
            except:
                Mail_message = Mail_message+'\nTask: ' + section + '\nRun : Ended with ERROR\n'
                Mail_message = Mail_message+'Check your configruation:\nConnection String: '+Connection_String+'\nTransfer Name : '+Transfer_Name+'\nOutput Directory: '+Transfer_Directory+'\n\n'
         else:
            if (config.get(section, 'Task_Schedule')) == '8':
                Mail_message = Mail_message+'Task: ' + section + '\nRun : should not run today, the task is PAUSED\n\n'
            else:
                Mail_message = Mail_message+'Task: ' + section + '\nRun : should not run today, should run on '+ Days_To_Run[int(config.get(section, 'Task_Schedule'))]+'\n\n'
    else:
        #02.WEB AND BACKUP
        #INFO 
         if ShoudTaskRun(config.get(section, 'Task_Schedule')) :
            print('Now transferring: ',section)
            Task_Schedule = config.get(section, 'Task_Schedule')
            Task_Run = ShoudTaskRun(Task_Schedule)
            Task_info = config.get(section, 'Task_Info')
            Connection_String = r''+config.get(section, 'Connection_String')+''
            Transfer_Directory  = r''+config.get(section, 'Transfer_Directory')+''
            WEB_Directory = r''+config.get(section, 'WEB_Directory')+''
            Local_Dir = r''+config.get(section, 'Local_Dir')+''
            EnsureDir(Local_Dir)
            EnsureDir(Transfer_Directory)
            Transfer_Name = Local_Dir+'\\'+config.get(section, "Transfer_Name") + '_' + time.strftime('%Y%m%d%H%M') + '.eapx'
            ZIP_name = Local_Dir+'\\'+config.get(section, "Transfer_Name") + '.zip'
            Transfer_Log = Local_Dir+'\\'+config.get(section, "Transfer_Name") + '_log_' + time.strftime('%Y%m%d%H%M') + '.log'
            Remote_store = WEB_Directory+'\\'+config.get(section, "Transfer_Name") + '.zip'
            string1 = r''+Connection_String+''
            string2 = r''+Transfer_Name+''
            string3 = r''+Transfer_Log+''
            print('\nSource: '+string1)
            print('\nPath: '+string2)
            print('\nLog: '+string3)
            print('\nZip name: '+ZIP_name)
            print('\nRemote file: '+Remote_store)
            try:
                #REM 
                # trasnfer model 
                Repository = eaApp.Repository
                Project = Repository.GetProjectInterface()
                Project.ProjectTransfer(SourceFilePath=string1, TargetFilePath= string2, LogFilePath=string3)
                zip = r'"c:\Program Files\7-Zip\7z" a '+ZIP_name+' '+Transfer_Name
                print('\nDeleting archive')
                 # Delete destination
                try:
                   
                    delete = 'DEL '+Remote_store
                    os.system(delete)
                except:
                    print('\nCould not delete '+Remote_store)
                print(zip)
                print('\n Performing compression')
                os.system(zip)
                print('\n Copying zip file')
                  # Create copy
                try:
                    copy = 'COPY '+ZIP_name+' '+Remote_store
                    print('\nCopy :'+copy)
                    os.system(copy)
                    copy = 'COPY '+Transfer_Name+' '+Transfer_Directory
                    print('\nCopy :'+copy)
                    os.system(copy)
                    copy = 'COPY '+Transfer_Log+' '+Transfer_Directory
                    print('\nCopy :'+copy)
                    os.system(copy)
                except:
                    print('Could not copy file')
                Mail_message = Mail_message+'\nTask: ' + section + '\nRun : SUCCESS\n\nFiles stored in: '+Transfer_Directory+'\n\nZIP file uploaded to '+Remote_store
            except:
                Mail_message = Mail_message+'\nTask: ' + section + '\nRun : Ended with ERROR\n'
                Mail_message = Mail_message+'Check your configruation:\nConnection String: '+Connection_String+'\nTransfer Name : '+Transfer_Name+'\nOutput Directory: '+Transfer_Directory+'\n\n'
         else:
            if (config.get(section, 'Task_Schedule')) == '8':
                Mail_message = Mail_message+'Task: ' + section + '\nRun : should not run today, the task is PAUSED\n\n'
            else:
                Mail_message = Mail_message+'Task: ' + section + '\nRun : should not run today, should run on '+ Days_To_Run[int(config.get(section, 'Task_Schedule'))]+'\n\n'
#program.kill() #stop sparx

#print(Mail_message)
#os.system('taskkill /F /FI "IMAGENAME eq EA.exe"')

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
    s.login("webadmin@agnicoli.org", "J4.S0m.Webadmin")
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