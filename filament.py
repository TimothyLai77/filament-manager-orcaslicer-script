import sys
import re
import requests
from datetime import datetime

gcodeFile = sys.argv[1]
# look for the name of the file, and the filament used.
# ; printing object 3dbenchy.stl id:3152 copy 0
# ; filament used [g] = 14.82

# match for gcode comment for '; printing object ' and capture on 'something.something'
printNameRegex = re.compile(r"; printing object (\w+\.\w+)")

# match for the gcode comment on 'filament used [g] = '
# with a capture on the xx.xx number at the end
filamentAmountRegex = re.compile(r"; filament used \[g\] = ([0-9]+\.?[0-9]+)")
printObject = None
filamentUsed = None
with open(gcodeFile, 'r') as file:
    for line in file:
        # read line by line through the file, if the regex matches, then extract the capture group
        # only write once. because there's multiple instances of that pattern, but all don't have the filename. kinda jank...
        if (printObject is None):
            if (re.search(printNameRegex, line)):
                printObject = re.search(printNameRegex, line).group(1) 

        # capture the filament Used comment
        if (re.search(filamentAmountRegex, line) != None):
            filamentUsed = re.search(filamentAmountRegex, line).group(1) 

# build the payload
payload = {
    "printObject" : printObject,
    "filamentUsed": float(filamentUsed),
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# send to API
requests.post('http://localhost:5000/api/receive', json=payload, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

