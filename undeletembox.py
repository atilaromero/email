#!/usr/bin/python
import fileinput
import re

def main(path):
    subs=[[hex(x)[-1],hex(x-8)[-1]] for x in range(9,16)]
    for line in fileinput.input(path,inplace=True):
        start='X-Mozilla-Status:'
        if line.startswith(start):
            digits=re.search('[0123456789abcdef]{4}',line)
            lastpos=digits.span()[1]-1
            if int(line[lastpos],16)>7:
                newl=list(line)
                newl[lastpos]=str(int(line[lastpos],16)-8)
                line=''.join(newl)
                #sys.stderr.write(line)
        sys.stdout.write(line)
        
if __name__=="__main__":
    import sys
    main(*sys.argv[1:])
