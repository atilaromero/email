#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import shutil

def retirabarra(s):
    mapa=[
          ['\\', '_'],
          ['/', '_'],
         ]
    for x,y in mapa:
        s=s.replace(x,y)
    return s

def retiraacentosdir(path):
    opj=os.path.join
    for root,dirs,files in os.walk(path):
        for d in []+dirs+files:
            new=retiraacentos(d)
            if not new==d:
                shutil.move(opj(root,d),opj(root,new))
                if d in dirs:
                    dirs[dirs.index(d)]=new
    
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
          ['?','_'],
          ['<','_'],
          ['>','_'],
          [':','_'],
          ['*','_'],
          ['|','_'],
          [';','_'],
          ['\r','_'],
          ['\n','_'],
          ['@', '_']]
    for x,y in mapa:
        s=s.replace(x,y)
    return s

if __name__=='__main__':
    import sys
    retiraacentosdir(sys.argv[1])
