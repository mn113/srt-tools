#! /usr/bin/env python
# srt_numberer.py

""" Renumbers from 1 the lines in an .srt file
"""

# Deal with arguments:
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print 'Usage: srt_numberer.py inputfile.srt'
        sys.exit(0)
    inputfile = sys.argv[1]

outputfile = 'srt_out.srt'

n = 1; # counter

f = open(inputfile)
o = open(outputfile, 'w')
for line in f:
	if line.strip().isdigit():
	    # Write n to new file
	    o.write(str(n))
	    o.write('\n')
	    n += 1
	else:
	    # Write the unchanged line to new file
	    o.write(line)
    	
f.close()
o.close()