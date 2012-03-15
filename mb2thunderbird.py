#!/usr/bin/python                                                                       
# -*- coding: utf-8 -*-
import os,sys
sys.path.insert(0,'/git/spec')
import command

cmd=command.exe.clone()
cmd.choice='subprocess.call'

def main(dirorig,dirdest):
    os.chdir(dirorig)
    for (dirpath,dirnames,filenames) in os.walk('./'):
        for filename in filenames:
            arq=os.path.join(dirpath, filename)
            if not (os.stat(arq).st_size == 0):
                arqdest=dirdest
                arqdest=arqdest.decode('utf_8').encode('iso8859_1')
                os.path.exists(arqdest) or os.makedirs(arqdest)
                for middir in arq.split('/')[1:-1]:
                    if middir[0]=='{':
                        middir=middir[0:4]
                    if middir=='Documents and Settings':
                        middir='D_S'
                    file('%s/%s'%(arqdest,middir),'a').close()
                    arqdest='%s/%s.sbd'%(arqdest,middir)
                    os.path.exists(arqdest) or os.makedirs(arqdest)
                os.chmod(os.path.join(dirorig,arq),0550)
                cmd(["ln", "-sf",os.path.join(dirorig,arq),arqdest])

if __name__ == "__main__":
    main(*sys.argv[1:])
