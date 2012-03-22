#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import subprocess

def preparadir(newd):
    os.path. exists(newd) or os.makedirs(newd,0750)

def cmd(*args):
    print args
    return subprocess.call(*args)

def main(dirmbox,dirmdir):
    def __xcall__(newf):
        relative=newf.split(dirmbox,1)[-1]
        #parts=relative.split('/',2)
        #relative='/'.join(parts[:-1]+[parts[-1].replace('/','\\')])
        relative=relative.replace('/','\\')
        newd=dirmdir+relative
        #newd=convname(newd)
        preparadir(newd)
        preparadir(newd+'/tmp')
        preparadir(newd+'/cur')
        preparadir(newd+'/new')
        cmd(['python',"/git/email/mbox2maildir.py",newf,newd])
        if os.path.exists('%s/cur'%newd):
            if len(os.listdir('%s/new'%newd))==0 and len(os.listdir('%s/cur'%newd))==0:
                os.rmdir('%s/new'%newd)
                os.rmdir('%s/tmp'%newd)
                os.removedirs('%s/cur'%newd)
        else:
            os.removedirs(newd)
        for root,dirnames,filenames in os.walk(dirmdir):
            for x in ['cur','new','tmp']:
                if x in dirnames:
                    dirnames.remove(x)
                else:
                    os.mkdir(os.path.join(root,x))
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
