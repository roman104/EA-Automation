# m_automation
# version 1.0
# author: Maros Zvolensky
# Scope: automation script that will perform project transfer or HTML extract based on config file


import configparser  # call config parser
import time  # to get timestamp
import win32com.client #to be able to call sparx api
import os # to work with directories
import sys
import traceback
import subprocess #to be able to start sparx
import smtplib
import time


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
time_left = 15
endless_cycle = 0
while (endless_cycle == 0):
    Mail_message1 = 'M_automation status for '+time.strftime('%A')+', '+time.strftime('%d %B %Y')+'\n\n\n'
    Mail_Subject = Mail_message1
    Mail_message = """Hello guys,
    This is an message from the script providing information on the status of the automation script.
    !!! This script is initiated manually. !!!

    """+Mail_message1
    Days_To_Run = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','Everyday','Paused']
    config = configparser.ConfigParser()
    eaApp = win32com.client.Dispatch("EA.App") #call EA application
    config.read(r'd:\M_Automation\config\m_automation_html.ini')  # open cofing file
    for section in config.sections(): #for each section in the config file
         Task_Type = config.get(section, 'Task_Type') #decide what to da based on the task type
         if ShoudTaskRun(config.get(section, 'Task_Schedule')) :
            print('Running HTML extract task ',section)
            start_time = time.time()
            print (time.strftime('%X %x %Z'))
            Task_Schedule = config.get(section, 'Task_Schedule')
            Task_Run = ShoudTaskRun(Task_Schedule)
            Task_info = config.get(section, 'Task_Info')
            Connection_String = r''+config.get(section, 'Connection_String')+''
            SPARX_OID = r''+config.get(section, 'SPARX_OID')+''
            EnsureDir(config.get(section, 'HTML_To'))
            HTML_To = r''+config.get(section, 'HTML_To')+''
            Today = time.strftime('%A')
            #print('Task will run on', Days_To_Run[int(Task_Schedule)], ' and today is ', Today, ' Task will run?: ',Task_Run)
            #print('Task information: ', Task_info)
            #print('Connection String: ', Connection_String)
            #print('SPARX Object ID', SPARX_OID)
            #print('HTML output path', HTML_To)
            ImageFormat = 'PNG'
            Style = '<default>'
            Extension = '.htm'
            try:
                Repository = eaApp.Repository
                Repository.OpenFile(Connection_String)
                Project = Repository.GetProjectInterface()
                Project.RunHTMLReport(SPARX_OID, HTML_To, ImageFormat, Style, Extension)
                print ('It took '+str((time.time() - start_time))+' seconds\n')
                Mail_message = Mail_message+'\nTask: ' + section + '\nType: ' +Task_Type+ '\nRun : SUCCESS\nFiles stored in: '+HTML_To+'\n\n'+'It took '+str((time.time() - start_time))+' seconds\n\n'
            except:
                Mail_message = Mail_message+'\nTask: ' + section + '\nType: ' +Task_Type+ '\nRun : Ended with ERROR\n'
                Mail_message = Mail_message+'Check your configruation:\nConnection String: '+Connection_String+'\nGUID : '+SPARX_OID+'\nOutput Directory: '+HTML_To+'\n\n'
         else:
             Mail_message = Mail_message+'Task: ' + section + '\nType: ' +Task_Type+ '\nRun : should not run today, should run on '+ Days_To_Run[int(config.get(section, 'Task_Schedule'))]+'\n\n'

    #program.kill() #stop sparx
    KillSparx()
    print(Mail_message)
    #os.system('taskkill /F /FI "IMAGENAME eq EA.exe"')

    sender = 'maros.zvolensky@hpe.com'
    receiver = ['maros.zvolensky@hpe.com']

    message = """From: From Person <maros.zvolensky@hpe.com>
    To: To person <maros.zvolensky@hpe.com>
    Subject: """+Mail_Subject
    message = message + Mail_message
    try:
        smtpObj = smtplib.SMTP('smtp-emea.svcs.hpe.com')
        smtpObj.sendmail(sender, receiver, message)
        print('Successfully sent email')
    except:
        print('Error: Unable to send email')

    while (time_left >1 ):
        time.sleep(3600)
        print(time_left,' hours to next run')
        time_left -= 1
    time_left = 23