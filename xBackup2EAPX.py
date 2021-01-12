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
import backupUtils

# -----------------------------------------
#00. Init application
# definition of global variables
# ============================
# -----------------------------------
# Init variables, paths to config file
def initBackup():
    return
 
 # ==============================================
# ---------------------------------------------------
#01. Read Config file
# read the models to be backuped

def readConfigFile():
    return
# ================================================
# ----------------------------------------------------
# read command to be performed - optional
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
    return
# =============================================
# ----------------------------------------------------

# send mail
def notification():
    return
# =====================================
# close


# -------------------------------------------- main
def myMain():
    initBackup()
    readConfigFile()
    readCmds()
    performActions()
    notification()
    return 


if __name__ == '__main__':
    myMain()