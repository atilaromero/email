#!/usr/bin/python

import os,sys

def choosefilename(filename):
  if os.path.exists(filename):
    for x in range(50):
      a,b=os.path.splitext(filename)
      mytry=''.join([a,'[',str(x),']',b])
      if not os.path.exists(mytry):
        return mytry
  return filename


if __name__ == "__main__":
  if (len(sys.argv) <> 2):
    print 'Utilize ' + sys.argv[0] + ' filename'
    print '   Escolhe um nome de arquivo que nao existe ainda.'
    sys.exit(1)
  filename=sys.argv[1]
  print choosefilename(filename)
