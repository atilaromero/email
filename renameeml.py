#!/usr/bin/python
import rfc822
import os
from choosefilename import choosefilename
from retiraacentos import *

def stritem(obj,key):
    if obj.has_key(key):
        return obj[key]
    else:
        return ''

def renameinplace(path):
    with open(path) as f:
        msg=rfc822.Message(f)
    dirname,basename=os.path.split(path)
    basename='%s_%s.eml'%(stritem(msg,'date'),stritem(msg,'subject').split('\n')[0])
    basename=retirabarra(retiraacentos(basename))[:255]
    newf=choosefilename(os.path.join(dirname,basename))
    assert(newf and not os.path.exists(newf))
    try:
        os.rename(path,newf)
    except OSError as e:
        print path
        print newf
        raise e
    return newf
    
if __name__=='__main__':
    import sys
    for x in sys.argv[1:]:
        renameinplace(x)
    
