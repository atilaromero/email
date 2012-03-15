# -*- coding: utf-8 -*-

"""
Based on maildir2mbox.py (Nathan R. Yergler)

This file does not contain sufficient creative expression to invoke
assertion of copyright.  No warranty is expressed or implied; use at
your own risk.

---

Uses Python's included mailbox library to convert mail archives from
mbox [http://en.wikipedia.org/wiki/Mbox] format.
maildir [http://en.wikipedia.org/wiki/Maildir] to 

---

To run, save as mbox2maildir.py and run:

$ python mbox2maildir.py [mbox_filename] [maildir_path] 

"""

import mailbox
import sys


def main(inbox,outbox):
    # open the existing mdir and the target mbox file
    mbox = mailbox.UnixMailbox(file(inbox,'r'))
    mdir = mailbox.Maildir(outbox)

    # iterate over messages in the mdir and add to the mbox
    count=0
    for msg in mbox:
        mdir.add(str(msg))
        count+=1

    # close and unlock
    mdir.close()
    return count

if __name__=='__main__':
    print 'Message count:',main(*sys.argv[1:])
