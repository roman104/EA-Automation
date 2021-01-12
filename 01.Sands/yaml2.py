#!/usr/bin/env python3
import yaml

users = [{'name': 'John Doe', 'occupation': 'gardener'},
         {'name': 'Lucy Black', 'occupation': 'teacher'}]

#with open("M:\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\01.Sands\\users2.yaml", 'w') as f:
with open("M:\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\01.Sands\\users2.yaml") as f:
    
    #data = yaml.dump(users, f)
    #print (data,"\r",users)
    data = yaml.load(f,Loader=yaml.FullLoader)
    print(data)


#- name: John Doe
#  occupation: gardener
#- name: Lucy Black
#  occupation: teacher
