#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from retiraacentos import *
import os
import re
import shutil
import subprocess
import tempfile
import undeletembox
import mboxtree2maildir
#from entrypoint import entrypoint
import sys
sys.path.insert(0,'/git/spec')
import command

sh=command.exe.clone()
sh.choice='os.system'
sh.precall=[command.show]

cmd=command.exe.clone()
cmd.choice='subprocess.Popen'
cmd.precall=[command.show]

def mkprintsome(s):
    n=[0]
    def f():
        print ' '+s[n[0]]+'\r',
        n[0]=(n[0]+1)%len(s)
    return f
printbar=mkprintsome('-\\|/')
printO=mkprintsome('.oOo')

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
                #print f.func_name
                f(*fparams)
            return True
        return False

def convname(newd):
    newd=retiraacentos(newd)
    newd=newd.replace('Documents and Settings','D_S')
    newd=newd.replace('Configuracoes locais','C_L')
    newd=newd.replace('Dados de aplicativos','D_A')
    newd=newd.replace('Local Settings','L_S')
    newd=newd.replace('Application Data','A_D')
    found=re.search('{[^}]+}',newd)
    if found:
        foundstring=found.group()
        if len(foundstring)>5:
            newd=newd.replace(foundstring,foundstring[0:5])
    return newd

class ConvertEmail:
    def __init__(self,dirorig,dirdest):
        self.dirorig=dirorig
        self.dirdest=dirdest
        self.ignore=readarq('/storage1/mnt/config/ignoredir')
        self.roottasks=[]
        self.dirstasks=[]
        self.filetasks=[]
        self.postfiletasks=[]

    def __call__(self):
        for root, dirs, files in os.walk(self.dirorig):
            for task in self.roottasks:
                task((self,root),())
            for d in dirs:
                printO()
                path='/'.join([root,d])
                for task in self.dirstasks:
                    task((self,root,dirs,d),(self,path,None))
            for name in files:
                printbar()
                path='/'.join([root.rstrip('/'),name])
                relative=path.split(self.dirorig,1)[-1]
                relative=convname(relative)
                newf='/'.join([self.dirdest.rstrip('/'),relative.lstrip('/')])
                didtask=False
                for task in self.filetasks:
                    didtask=task((self,path,newf),(self,path,newf)) or didtask
                if didtask:
                    for task in self.postfiletasks:
                        task((self,path,newf),(self,newf,None))

def chk_ignore(self,path,newf):
    return self.ignore and (path in self.ignore)
def chk_notignore(self,path,newf):
    return not chk_ignore(self,path,newf)
def chk_notprocessed(dirdestmbox,dirdestmdir):
    ope=os.path.exists
    def __call__(self,path,newf):
        return (not ope(newf)) and (not ope(mbpath2mdpath(dirdestmbox,dirdestmdir,newf)))
    return __call__
def chk_notlink(self,path,newf):
    return not os.path.islink(path)
def endswith(self,suffix):
    def f(self,path,*args):
        return path.endswith(suffix)
    return f
def chk_thdb(self,path,newf):
    return os.path.exists(path+'.msf')
def rt_printroot(self,root):
        print 'root:',root
def dt_ignoredirs(self,root,dirs,d):
    dirs.remove(d)
def ft_print(self,path,newf):
    print 'ft_print:',path
def preparadir(newd):
    os.path.exists(newd) or os.makedirs(newd)
def ft_dbx_mbox(self,path,newf):
    print 'ft_dbx_mbox:',path
    preparadir(os.path.dirname(newf))
    cmd(['/git/email/readdbx','-q','-f',path,'-o',newf])
def ft_pst_mbox(self,path,newf):
    print 'ft_pst_mbox:',path
    preparadir(newf)
    cmd(["readpst",'-q','-r','-D',path,'-o',newf])
def ft_thdb_mbox(self,path,newf):
    print 'ft_thdb_mbox',path
    preparadir(os.path.dirname(newf))
    shutil.copy(path,newf)
    undeletembox.main(newf)

def ft_dbx_eml(dirorig,dirdestmbox,dirdestmdir):
    def __call__(self,path,newf):
        print 'undbx:',path
        newd=mbpath2mdpath(dirdestmbox,dirdestmdir,newf)
        preparadir(os.path.dirname(newd))
        cmd(['undbx','--recover',path,newd])
    return __call__

def readarq(fpath):
    result=[]
    if os.path.exists(fpath):
        with open(fpath,'r') as fproc:
            for line in fproc:
                if line.rstrip():
                    result.append(line.rstrip().rstrip('/'))
    return result

def mbpath2mdpath(dirdestmbox,dirdestmdir,newf):
    relative=newf.split(dirdestmbox,1)[-1]
    newd=dirdestmdir+relative.replace('/','\\')
    return newd

def pft_mbox_mdir(dirorig,dirdestmbox,dirdestmdir):
    def __call__(self,path,newf):
        newd=mbpath2mdpath(dirdestmbox,dirdestmdir,newf)
        mboxtree2maildir.main(newf,newd)
    return __call__

#@entrypoint
def main(dirorig,dirdestmbox,dirdestmdir):
    obj=makeplan(dirorig,dirdestmbox,dirdestmdir)
    obj()

def makeplan(dirorig,dirdestmbox,dirdestmdir):
    readpst_version='v0.6.54'
    if not cmd(['readpst','-V']).find(readpst_version)>-1:
        print 'readpst version has to be %s. Download it or update sourcecode.'%readpst_version
    undbx_version='v0.20'
    if not cmd(['undbx','--version']).find(undbx_version)>-1:
        print 'undbx version has to be %s. Download it or update sourcecode.'%undbx_version
    obj=ConvertEmail(dirorig,dirdestmbox)
    obj.roottasks=[Task(rt_printroot)]
    obj.dirstasks=[Task(dt_ignoredirs,chk_ignore)]
    obj.filetasks=[Task(ft_dbx_mbox,[
                                     endswith(obj,'.dbx'),
                                     chk_notlink,
                                     chk_notprocessed(dirdestmbox,dirdestmdir),
                                     chk_notignore,
                                     ]),
                   Task(ft_pst_mbox,[
                                     endswith(obj,'.pst'),
                                     chk_notlink,
                                     chk_notprocessed(dirdestmbox,dirdestmdir),
                                     chk_notignore,
                                     ]),
                   Task(ft_thdb_mbox,[
                                      chk_thdb,
                                      chk_notlink,
                                      chk_notprocessed(dirdestmbox,dirdestmdir),
                                      chk_notignore,
                                      ]),
                   ]
    obj.postfiletasks=[Task(ft_print),
                       Task(pft_mbox_mdir(dirorig,dirdestmbox,dirdestmdir)),
                       ]
    return obj

if __name__=='__main__':
    import sys
    main(sys.argv[1],sys.argv[2],sys.argv[3])
