#! /usr/bin/env python
# vtt_to_srt.py

""" Converts VTT subtitles to SRT format
"""

# Deal with arguments:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print 'Usage: vtt_to_srt.py inputfile.vtt'
        sys.exit(0)
    inputfile = sys.argv[1]

outputfile = inputfile + '.srt'


import re
import codecs

# Open input, output files
f = codecs.open(inputfile, "r", "utf-8")
o = codecs.open(outputfile, 'w', "utf-8")

# Loop through lines:
for line in f.readlines():

#    print type(line)
    #line.encode("utf-8")

    # Ignore certain crap:
    if line[0:6] == 'WEBVTT' or line[0:6] == 'Region':
        continue

    # Treat timing lines (which contain no UTF-8 characters):
    elif len(line) > 2 and line[2] == ':':
        # Dots to commas:
        line = re.sub('\.', ',', line)
        # Trim text beyond endtime:
        endtime = re.search('--> \d\d:\d\d:\d\d,\d\d\d', line)
        endtimepos = endtime.start() + 16
        line = line[:endtimepos] + '\n'
    
    # Treat text lines (respecting UTF-8 characters):
    elif line[0:2] == '<c':
        # Strip <c> tags by regex:
        line = re.sub('<c.*>(.*)<\/c>', r'\1', line, flags=re.U)
        # Try to discard music lyrics:
        if '#' in line[0:2]:
            continue
        # Try to add line break before second hyphen:
        line = re.sub(r'^(.+)-([A-Z])', r'\1\n-\2', line, flags=re.U)
        # Try to break on punctuation next to capital:
        line = re.sub(r'^(.+[\.,?!])([A-Z])', r'\1\n\2', line, flags=re.U)


    # Reproduce line:
#    line.encode("utf-8")
#    print type(line)
    o.write(line)	# still won't preserve UTF-8 characters!

f.close()
o.close()