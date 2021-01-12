import yaml
import pprint
#MyQuiz="A:\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\03.Yaml-Examples\\01.Yaml1\\Quiz02.yml"
MyQuiz="A:\\26.PrehladModelov\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\02.BackupEAP\\BackupConfig.yml"
import yaml
import pprint
 
def read_yaml():
    """ A function to read YAML file"""
    with open(MyQuiz) as f:
        config = list(yaml.safe_load_all(f))
 
    return config
 
def write_yaml(data):
    """ A function to write YAML file"""
    with open('toyaml.yml', 'a') as f:
        yaml.dump_all(data, f, default_flow_style=False)
 
if __name__ == "__main__":
 
    # read the config yaml
    my_config = read_yaml()
 
    # pretty print my_config
    pprint.pprint(my_config)
 
    # write A python object to a file
    write_yaml(my_config)