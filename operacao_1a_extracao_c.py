#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import tempfile
from entrypoint import entrypoint

def sh(cmd):
    #print cmd
    os.system(cmd)

def cmd(x):
    output,err=subprocess.Popen(x,stdout=subprocess.PIPE).communicate()
    return output

class Task:
    def always(*args,**kwargs):
        return True
    def __init__(self,function,condition=always):
        self.function=function
        self.condition=condition
        
    def __call__(self,fparams,cparams):
        lc=[[self.condition],self.condition][isinstance(self.condition,list)]
        lf=[[self.function],self.function][isinstance(self.function,list)]
        if all(c(*cparams) for c in lc):
            for f in lf:
                f(*fparams)
            return True
        return False

class ConvertEmail:
    def __call__(self):
        for root, dirs, files in os.walk(self.dirorig):
            for task in self.roottasks:
                task((self,root),())
            for d in dirs:
                path='/'.join([root,d])
                for task in self.dirstasks:
                    task((self,root,dirs,d),(self,path))
            for name in files:
                path='/'.join([root,name])
                relative=path.split(self.dirorig,1)[-1]
                for x,y in zip(['ã','õ','á','é','í','ó','ú','Á','É','Í','Ó','Ú','ç','Ç','@',],
                               ['a','o','a','e','i','o','u','A','E','I','O','U','c','C','_',]):
                    print x
                    relative=relative.replace(x,y)
                newf='/'.join([dirdest,relative])
                didtask=False
                for task in self.filetasks:
                    didtask=task((self,path,newf),(self,path)) or didtask
                if didtask:
                    for task in self.postfiletasks:
                        task((self,path,newf),(self,path))

    def __init__(self,dirorig,dirdest):
        self.dirorig=dirorig
        self.dirdest=dirdest
        self.ignore=[]
        self.processed=[]
        self.roottasks=[Task(rt_printroot)]
        self.dirstasks=[Task(dt_ignoredirs,chk_ignore)]
        self.filetasks=[Task(ft_dbx_mdir,[chk_notprocessed,chk_notignore,chk_notlink,endswith(self,'.dbx')]),
                        Task(ft_pst_mdir,[chk_notprocessed,chk_notignore,chk_notlink,endswith(self,'.pst')]),
                        Task(ft_thdb_mdir,[chk_notprocessed,chk_notignore,chk_notlink,chk_thdb]),
                        ]
        self.postfiletasks=[Task(ft_print,[chk_notprocessed,chk_notignore,chk_notlink,chk_thdb]),
                            #Task(ft_perms,[chk_notprocessed,chk_notignore,chk_notlink]),
                            ]

def chk_ignore(self,path):
    return self.ignore and path in self.ignore
def chk_notignore(self,path):
    return not self.chk_ignore(path)
def chk_notprocessed(self,path):
    return not path in self.processed
def chk_notlink(self,path):
    return not os.path.islink(path)
def endswith(self,suffix):
    def f(self,path):
        return path.endswith(suffix)
    return f
def chk_thdb(self,path):
    return all([path.find('/Thunderbird/Profiles/')>-1,
                any([path.find('/Mail/')>-1,
                     path.find('/ImapMail/')>-1]),
                not path.endswith('.msf')])
def rt_printroot(self,root):
        print root
def dt_ignoredirs(self,root,dirs,d):
    dirs.remove(d)
def ft_print(self,path,newf):
    print path
def preparadir(newd):
    os.path.exists(newd) or os.makedirs(newd)
def ft_dbx_mbox(self,path,newf): 
    preparadir(os.path.dirname(newf))
    sh("readdbx -q -f '%s' -o '%s'"%(path,newf))
def ft_dbx_mdir(self,path,newf):
    newmdir=[preparadir(os.path.dirname(newf)+'/'+x) for x in ['cur','new','tmp']][0]
    with tempfile.NamedTemporaryFile(mode='r') as tempf:
        sh("readdbx -q -f '%s' -o '%s'"%(path,tempf))
        sh("./mb2md.py -i '%s' -o '%s'"%(tempf,newmdir))
def ft_pst_mbox(self,path,newf):
    preparadir(os.path.dirname(newf))
    sh("readpst -q -r '%s' -o '%s'"%(path,newf))
def ft_pst_mdir(self,path,newf):
    newmdir=[preparadir(os.path.dirname(newf)+'/'+x) for x in ['cur','new','tmp']][0]
    sh("readpst -q -r '%s' -S -o '%s'"%(path,newf))
def ft_thdb_mbox(self,path,newf):
    preparadir(os.path.dirname(newf))
    shutil.copy(path,newf)
def ft_thdb_mdir(self,path,newf):
    newmdir=[preparadir(os.path.dirname(newf)+'/'+x) for x in ['cur','new','tmp']][0]
    sh("./mb2md.py -i '%s' -o '%s'"%(path,newmdir))
#    def ft_perms(self,newd)
#        sh("chown root:%s '%s' -R "%(group,newd))
#        sh("chmod u=rwX,g=rX,o-rwx '%s' -R "%(newd))

def readarq(fpath):
    result=[]
    if os.path.exists(fpath):
        with open(fpath,'r') as fproc:
            for line in fproc:
                if line.rstrip():
                    result.append(line.rstrip())
    return result

@entrypoint
def main(dirorig,dirdest):
    readpst_version='v0.6.53'
    if not cmd(['readpst','-V']).find(readpst_version)>-1:
        print 'readpst version has to be %s. Download it or update sourcecode.'%readpst_version
    readdbx_version='v1.0.3'
    if not cmd(['readdbx','-V']).find(readdbx_version)>-1:
        print 'readdbx version has to be %s. Download it or update sourcecode.'%readdbx_version
    obj=ConvertEmail(dirorig,dirdest)
    obj()
