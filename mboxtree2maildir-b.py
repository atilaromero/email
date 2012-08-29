#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import subprocess
from retiraacentos import *
import renameeml

def preparadir(newd):
    os.path.exists(newd) or os.makedirs(newd,0750)

def cmd(*args):
    print args
    return subprocess.call(*args)

def main(dirmbox,dirmdir):
    def __xcall__(newf):
        relative=newf.split(dirmbox,1)[-1]
        newd=dirmdir+relative
        [preparadir(newd+i) for i in ['','/tmp/','/cur','/new']]
        cmd(['python',"/git/email/mbox2maildir.py",newf,newd])
        for x in os.listdir(newd+'/cur'):
            os.rename(os.path.join(newd,'cur',x),os.path.join(newd,x))
            renameeml.renameinplace(os.path.join(newd,x))
        [os.rmdir(newd+i) for i in ['/tmp/','/cur','/new']]
    newf=dirmbox
    if os.path.isdir(newf):
        for root,dirnames,filenames in os.walk(newf):
            for f in filenames:
                __xcall__(os.path.join(root,f))
    else:
        __xcall__(newf)

if __name__=='__main__':
    import sys
    main(*sys.argv[1:])
