"""
Custom wx.App class.
"""
import argparse
import string
import time
import sys
import os

import wx

from editor import PyKodeEditor

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true",
                        help="print PyKode version and exit")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="turn on debug mode")
    parser.add_argument("files", nargs="*", default=[],
                        metavar="FILE", help="files to open")

    args = parser.parse_args()
    if args.version:
        print "PyKode version %s" % PyKodeApp.__version__
        parser.exit()

    if args.debug:
        PyKodeApp.__DEBUG__ = True

    PyKodeApp.__files__ = args.files[::]


class PyKodeApp(wx.App):
    __DEBUG__ = False
    __version__ = "0.1 beta"
    __files__ = []

    def OnInit(self):
        self.frame = PyKodeEditor(None, -1, "PyKode")
        self.frame.SetSize((640, 480))
        if not self.frame.OnInit():
            return False
                
        for file in self.__files__:
            self.frame.tabbedview.OpenNewTab(os.path.abspath(file))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        
        return True

    def WriteLog(self, level, message):
        ctime = time.ctime()
        if level == "debug" and self.__DEBUG__:
            print >> sys.stdout, "[%s]: %s" % (ctime, message)
        elif level == "warning":
            print >> sys.stderr, "[%s]: %s" % (ctime, message)
        elif level == "error":
            print  >> sys.stderr, "[%s]: %s" % (ctime, message)
            err, msg = string.split(message, ":", maxsplit=1)
            err = err.rstrip()
            msg = msg.lstrip()
            wx.MessageBox(msg, err)
