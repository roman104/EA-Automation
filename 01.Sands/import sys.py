import sys
import yaml

inp = """\
# example
name:
  # details
  family: Smith   # very common
  given: Alice    # one of the siblings
"""

yaml1 = YAML()
code = yaml1.load(inp)
code['name']['given'] = 'Bob'

yaml1.dump(code, sys.stdout)