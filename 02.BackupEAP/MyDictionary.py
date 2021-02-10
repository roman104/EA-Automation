import numpy as np
import os
import yaml
# Save
dictionary = {'hello':'world'}
Statistics ={
"Header": {
    "Date": "YYYYMMDD,MMHH",
    "Report Name": "Report - Backup Summary"
},
"List Of Data": {
  "All Items In Config": 10,
  "All Items To be backed up": 2,
  "All EAPX Items to be Backuped": 2,
  "All XML Items to be Backeuped": 2
 },

"Results":{
  "All Items Overview":{
    "All Items": 1,
    "ALL BAckups succeeded": 1,
    "All FAILED Backups": 1
  }
 },
 "EAPX":{ 
    "All Items to be backuped": 1,
    "Number of OK": 1,
    "Number of FAILED": 1
 },

"NAtive XML":{
    "All Items to be backuped": 1,
    "Number of OK": 1,
    "Number for FAILED": 1
 },
 
"Time information": {
  "Start date Time": "" ,
  "End Date, Time": "",
  "Duration": 1.5,
  "Total size in MB": 10 
 },
 
"Details about all Items":{
  "item ID":  {
   "id":1,
  "Repo ID": "REPO",
  "Format": "EAPX",
  "Start time": "",
  "End Time": "",
  "Duration": 1.1,
  "Size": 1.2,
  "Result": "OK",
  "Comment": ""
  },
  "item ID":  {
      "id":2,
  "Repo ID": "REPO",
  "Format": "EAPX",
  "Start time": "",
  "End Time": "",
  "Duration": 1.1,
  "Size": 1.2,
  "Result": "OK",
  "Comment": ""
  },
  

}  
}

np.save('my_file.npy', dictionary) 

# Load
read_dictionary = np.load('my_file.npy',allow_pickle='TRUE').item()
print(read_dictionary['hello']) # displays "world"
absolute_path = os.path.abspath('my_file.npy')
print("Full path: " + absolute_path)

with open('data.yml', 'w') as outfile:
    #yaml.dump(dictionary, outfile, default_flow_style=False)
    yaml.dump(Statistics, outfile, default_flow_style=False)

print(Statistics)