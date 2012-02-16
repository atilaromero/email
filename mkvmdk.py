#!/usr/bin/python
def mkvmdk(blocks,path):
    return """# Disk Descriptor File
version=1
CID=fffffffe
parentCID=ffffffff
createType="monolithicFlat"

# Extent description
RW %s FLAT "%s" 0

#DDB - Disk Data Base
ddb.adapterType = "ide"
ddb.virtualHWVersion = "3"
"""%(blocks,path)

def main(path):
    import os
    blocks=os.stat(path).st_size/512
    print mkvmdk(blocks,path)

if __name__=='__main__':
    import sys
    main(*sys.argv[1:])
