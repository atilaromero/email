#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Based on maildir2mbox.py (Nathan R. Yergler)
"""
import mailbox
import sys
import glob, shutil
def main(inbox,outbox):
    # open the existing mdir and the target mbox file
    mbox = mailbox.UnixMailbox(file(inbox,'r'),factory=mailbox.mboxMessage)
    mdir = mailbox.Maildir(outbox)

    # iterate over messages in the mdir and add to the mbox
    count=0
    for msg in mbox:
        mdir.add(str(msg))
        count+=1

    # close and unlock
    mdir.close()
    for f in glob.glob(outbox+'/new/*'):
        shutil.move(f,outbox+'/cur/' )
    return count

if __name__=='__main__':
    print 'Message count:',main(*sys.argv[1:])
