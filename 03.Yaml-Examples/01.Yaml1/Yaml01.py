import yaml
import pprint
MyQuiz="A:\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\03.Yaml-Examples\\01.Yaml1\\Quiz01.yml"
MyQuiz="A:\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\02.BackupEAP\\BackupConfig.yml"
def read_yaml():
    """ A function to read YAML file"""
    with open(MyQuiz) as f:
        config = yaml.safe_load(f)
 
    return config
 
if __name__ == "__main__":
 
    # read the config yaml
    my_config = read_yaml()
    MySourcesList=[]
    # pretty print my_config
    #pprint.pprint(my_config)
    # print raw data from yaml file
    print("------------------------------------------------")
    print("# Raw data:\n",my_config,"\n")
    i=0
    #go through all items at 1st level
    for item, doc in my_config.items():
        print("##Item, doc:\n",i,"=",item, ":", doc,"\n")
        #print("##i, type:\n",i,"type=",type(item))
        i=i+1
        #go trough all items in Source level
        if(item == 'Sources'):
            j=1
            for item1  in doc:
                MySourcesList.append(item1)
                print("\ttype=",type(item),"###Source:",j,"=",item1)
                j=j+1
    l=0
    for s in MySourcesList:
        print("#ListofSources:",l,"=",s)
        l=l+1
    print("==================================")