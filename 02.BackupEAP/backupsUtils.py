# Backup Automation-
# version 1.0
# author: Roman Kazicka  inspired by Maros Zvolensky
# Scope: automation script that will perform project transfer based on config file
# Sources: Sparxsystems, enterprise-architect-object-model.pdf
# Name: Utilities for Backup EA model into EAPX files
# Description: Automate routine backups from client side into EAPX files, Native Format, other DBMS repository
# Inputs:  Configuration file
# Date: 20201201
# change log

# Last change: 20210107
# Descrition of last change
# - creation the app stucture - function definition 
import os

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

# -------------------------------------------- main
def myMain():
    FolderName="M:\\77.Backup\\2021\\NATIVE\\20210207"
    FolderSize=getFolderSize(FolderName)
    print("FolderSize=",FolderSize)

    return 


if __name__ == '__main__':
    myMain()
