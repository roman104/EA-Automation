import sys
import yaml

inp = """\
# example
name:
  # details
  family: Smith   # very common
  given: Alice    # one of the siblings
"""
stream = file('M:\\13.Automation\\01.Backups\\02.Roman\\01.BAckup2EAPX\\01.Sands/document.yaml', 'w')
yaml.dump(data, stream) 

#yaml1 = YAML()
code = yaml.load(inp)
code['name']['given'] = 'Bob'

yaml.dump(code, sys.stdout)