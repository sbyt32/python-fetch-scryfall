import re

# ? Why not build the entire search string with this script?
def sanitizeString(name):
    name = re.sub("[',]","",name)
    name = re.sub("['\s]","_", name)
    name = name.lower()[slice(9)]
    if re.search("$_",name):
        name = name.rstrip(name[-1])
    return name