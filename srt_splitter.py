#! /usr/bin/env python
# srt_splitter.py

""" Splits an .srt file into 2 parts each starting at 00:00:00,000
"""

import math


def subtract_timecode(tc1, tc2):
    # split timecode string into components:
    h1, h2 = int(tc1[0:2]), int(tc2[0:2])
    m1, m2 = int(tc1[3:5]), int(tc2[3:5])
    s1, s2 = int(tc1[6:8]), int(tc2[6:8])
    d1, d2 = int(tc1[9:12]), int(tc2[9:12])
    #print h1, m1, s1, d1, '...', h2, m2, s2, d2

    # convert timecode components to seconds:
    t1 = (3600*h1) + (60*m1) + s1 + (d1/1000.0)
    t2 = (3600*h2) + (60*m2) + s2 + (d2/1000.0)
    to = t1 - t2

    # convert seconds back to timecode components:
    ho = int(math.floor(to/3600))
    mo = int(math.floor(to/60 % 60))
    so = int(math.floor(to % 60))
    do = int((to*1000 % 1000))

    # reformat as string:
    return ''.join([`ho`.zfill(2),':',`mo`.zfill(2),':',`so`.zfill(2),',',`do`.zfill(3)])


# Deal with arguments:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print 'Usage: srt_splitter.py inputfile.srt timecode'
        sys.exit(0)
    inputfile = sys.argv[1]
    timedelay = sys.argv[2]

outputfile = 'new_' + inputfile

i, n = 0, 0

f = open(inputfile)
o = open(outputfile, 'w')
for line in f:
    i += 1
    # reset line numbers:
    if line.strip().isdigit():
        n += 1
        o.write(str(n))
        o.write('\n')
    # identify timecodes:
    elif ':' in line and line[2] == ':' and line[5] == ':':
        # discard middle arrow:
        tcp = line.split(' ')
        # calculate new times:
        a = subtract_timecode(tcp[0].strip(), timedelay)
        b = subtract_timecode(tcp[2].strip(), timedelay)
        # format line:
        newline = ''.join([a, ' --> ', b])
        print newline
        o.write(newline)
        o.write('\n')
    else:
        o.write(line)

f.close()
o.close()

# still need to automatically remove negative timecode blocks