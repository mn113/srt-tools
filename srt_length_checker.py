#! /usr/bin/env python
# srt_length_checker.py

""" Checks line lengths in an .srt file
"""

# Deal with arguments:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print 'Usage: srt_numberer.py inputfile.srt'
        sys.exit(0)
    inputfile = sys.argv[1]

i = 0

f = open(inputfile)
for line in f:
    i += 1
    if len(line.strip()) > 40:
        print i, line
f.close()