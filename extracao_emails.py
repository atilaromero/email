#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import shutil
import subprocess
import tempfile
#from entrypoint import entrypoint
import sys
sys.path.insert(0,'/git/spec')
import command

sh=command.exe.clone()
sh.choice='os.system'
sh.precall=[command.show]

cmd=command.exe.clone()
cmd.choice='subprocess.Popen'

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

def retiraacentos(s):
    mapa=[
          ['\xc3\xa1', 'a'],#'
          ['\xc3\xa2', 'a'],#^
          ['\xc3\xa3', 'a'],#~
          ['\xc3\xa9', 'e'],
          ['\xc3\xaa', 'e'],
          ['\xc3\xad', 'i'],
          ['\xc3\xae', 'i'],
          ['\xc3\xb3', 'o'],
          ['\xc3\xb4', 'o'],
          ['\xc3\xb5', 'o'],
          ['\xc3\xba', 'u'],
          ['\xc3\xbb', 'u'],
          ['\xc3\xbb', 'u'],#"
          ['\xc3\x81', 'A'],
          ['\xc3\x82', 'A'],
          ['\xc3\x83', 'A'],
          ['\xc3\x89', 'E'],
          ['\xc3\x8a', 'E'],
          ['\xc3\x8d', 'I'],
          ['\xc3\x8e', 'I'],
          ['\xc3\x93', 'O'],
          ['\xc3\x94', 'O'],
          ['\xc3\x95', 'O'],
          ['\xc3\x9a', 'U'],
          ['\xc3\x9b', 'U'],
          ['\xc3\x9c', 'U'],
          ['\xc3\xa7', 'c'],
          ['\xc3\x87', 'C'],
          ['@', '_']]
    for x,y in mapa:
        s=s.replace(x,y)
    return s

class ConvertEmail:
    def __init__(self,dirorig,dirdest):
        self.dirorig=dirorig
        self.dirdest=dirdest
        self.ignore=[]
        self.processed=[]
        self.roottasks=[]
        self.dirstasks=[]
        self.filetasks=[]
        self.postfiletasks=[]

    def __call__(self):
        for root, dirs, files in os.walk(self.dirorig):
            for task in self.roottasks:
                task((self,root),())
            for d in dirs:
                path='/'.join([root,d])
                for task in self.dirstasks:
                    task((self,root,dirs,d),(self,path))
            for name in files:
                path='/'.join([root.rstrip('/'),name])
                relative=path.split(self.dirorig,1)[-1]
                relative=retiraacentos(relative)
                newf='/'.join([self.dirdest.rstrip('/'),relative.lstrip('/')])
                didtask=False
                for task in self.filetasks:
                    didtask=task((self,path,newf),(self,path,newf)) or didtask
                if didtask:
                    for task in self.postfiletasks:
                        task((self,path,newf),(self,newf,None))

def chk_ignore(self,path,newf):
    return self.ignore and path in self.ignore
def chk_notignore(self,path,newf):
    return not chk_ignore(self,path,newf)
def chk_notprocessed(self,path,newf):
    return not path in self.processed
def chk_notlink(self,path,newf):
    return not os.path.islink(path)
def endswith(self,suffix):
    def f(self,path):
        return path.endswith(suffix)
    return f
def chk_thdb(self,path,newf):
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
def ft_pst_mbox(self,path,newf):
    preparadir(newf)
    sh("readpst -q -r -D '%s' -o '%s'"%(path,newf))
def ft_thdb_mbox(self,path,newf):
    preparadir(os.path.dirname(newf))
    shutil.copy(path,newf)

def readarq(fpath):
    result=[]
    if os.path.exists(fpath):
        with open(fpath,'r') as fproc:
            for line in fproc:
                if line.rstrip():
                    result.append(line.rstrip())
    return result

import re
def pft_mbox_mdir(dirorig,dirdestmbox,dirdestmdir):
    def convname(newd):
        newd=newd.replace('Documents and Settings','D_S')
        newd=newd.replace('Configuracoes locais','C_L')
        newd=newd.replace('Configurações locais','C_L')
        newd=newd.replace('Dados de aplicativos','D_A')
        newd=newd.replace('Local Settings','L_S')
        newd=newd.replace('Application Data','A_D')
        return retiraacentos(newd)
    def __xcall__(self,path,newf):
        relative=newf.split(dirdestmbox,1)[-1]
        newd=dirdestmdir+relative
        newd=convname(newd)
        found=re.search('{[^}]+}',newd)
        if found:
            foundstring=found.group()
            if len(foundstring)>5:
                newd=newd.replace(foundstring,foundstring[0:5])
        preparadir(newd)
        sh("/git/email/mb2md.py -i '%s' -o '%s'"%(newf,newd))
        if os.path.exists('%s/cur'%newd):
            if len(os.listdir('%s/cur'%newd))==0:
                os.rmdir('%s/new'%newd)
                os.rmdir('%s/tmp'%newd)
                os.removedirs('%s/cur'%newd)
        else:
            os.removedirs(newd)
        for root,dirnames,filenames in os.walk(dirdestmdir):
            for x in ['cur','new','tmp']:
                if x in dirnames:
                    dirnames.remove(x)
                else:
                    os.mkdir(os.path.join(root,x))
    def __call__(self,path,newf):
        if os.path.isdir(newf):
            for root,dirnames,filenames in os.walk(newf):
                for f in filenames:
                    __xcall__(self,path,os.path.join(root,f))
        else:
            __xcall__(self,path,newf)
    return __call__

#@entrypoint
def main(dirorig,dirdestmbox,dirdestmdir):
    obj=makeplan(dirorig,dirdestmbox,dirdestmdir)
    obj()

def makeplan(dirorig,dirdestmbox,dirdestmdir):
    readpst_version='v0.6.53'
    if not cmd(['readpst','-V']).find(readpst_version)>-1:
        print 'readpst version has to be %s. Download it or update sourcecode.'%readpst_version
    readdbx_version='v1.0.3'
    if not cmd(['readdbx','-V']).find(readdbx_version)>-1:
        print 'readdbx version has to be %s. Download it or update sourcecode.'%readdbx_version
    obj=ConvertEmail(dirorig,dirdestmbox)
    obj.roottasks=[]#Task(rt_printroot)]
    obj.dirstasks=[Task(dt_ignoredirs,chk_ignore)]
    obj.filetasks=[Task(ft_dbx_mbox,[chk_notprocessed,
                                     chk_notignore,
                                     chk_notlink,
                                     endswith(obj,'.dbx')]),
                   Task(ft_pst_mbox,[chk_notprocessed,
                                     chk_notignore,
                                     chk_notlink,
                                     endswith(obj,'.pst')]),
                   Task(ft_thdb_mbox,[chk_notprocessed,
                                      chk_notignore,
                                      chk_notlink,chk_thdb]),
                   ]
    obj.postfiletasks=[Task(ft_print),
                       Task(pft_mbox_mdir(dirorig,dirdestmbox,dirdestmdir)),
                       ]
    return obj

if __name__=='__main__':
    import sys
    main(sys.argv[1],sys.argv[2],sys.argv[3])
