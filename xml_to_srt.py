#! /usr/bin/env python
# xml_to_srt.py

""" Converts TTM XML subtitles to SRT format
"""

# Deal with arguments:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print 'Usage: xml_to_srt.py inputfile.xml'
        sys.exit(0)
    inputfile = sys.argv[1]

outputfile = inputfile + '.srt'


import re
import codecs
import xml.etree.ElementTree as ET

# Open input file,
f = codecs.open(inputfile, "r", "utf-8")
text_utf8 = f.read()
#print type(text_utf8) # <type 'unicode'>

# Perform removal of 'xml:' namespacing throughout:
cleaned1 = re.sub('xml:', '', text_utf8)
cleaned1.encode("utf-8")
#print type(cleaned1)  # <type 'unicode'>

# Perform removal of '<br />:
cleaned2 = re.sub('\s*(.*)\s*<br \/>\s*(.*)', r'\1\2', cleaned1)
cleaned2.encode("utf-8")
#print type(cleaned2)  # <type 'unicode'>
f.close()


# Parse cleaned XML:
root = ET.fromstring(cleaned2.encode('utf-8'))

# Prepare to output:
o = codecs.open(outputfile, 'w', "utf-8")

# Loop through all <p> elements:
prev_id = 0
for p in root.iter("p"):

    # Strip non-numeric characters:
    id = p.get('id')
#    print id
    curr_id = ''.join([c for c in id if c in '0123456789'])

    # If id is NOT "equal" to previous (e.g. 123a == 123b), start a new subtitle:
    if curr_id != prev_id:
        o.write(curr_id + '\n')

        # Timecodes:
        o.write(p.get('begin') + ' --> ' + p.get('end') + '\n')

    # Print the textual part:
    o.write(p.text.strip() + '\n')
    o.write('\n')

    curr_id = prev_id

o.close()