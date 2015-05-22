"""
Custom wx.Panel class.
"""

import os
import codecs

import wx

from textctrl import TextCtrl
from config import supported_types


class Tab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.filename = None
        self.filetype = None
        self.path = None

        self.OnInit()

    def OnInit(self):
        sizer = wx.BoxSizer()
        self.textctrl = TextCtrl(self)
        self.textctrl.Colourise(0, -1)
        sizer.Add(self.textctrl, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def Load(self, path):
        try:
            with codecs.open(path, "rb", "utf-8") as fp:
                data = fp.read()
            self.textctrl.SetText(data)
            wx.GetApp().WriteLog("debug", "Opened file: %s" % path)

        except IOError as exc:
            self.Destroy()
            wx.GetApp().WriteLog("error", "Failed to open file: %s" % str(exc))

            return False

        except ValueError as exc:
            self.Destroy()
            wx.GetApp().WriteLog("error", "Encoding error: %s" % str(exc))

            return False

        self.SetPath(path)
        self.textctrl.EmptyUndoBuffer()

        return True

    def GuessType(self):
        """Guess file type by extesion."""
        _, ext = os.path.splitext(self.filename)
        ext = ext[1:]

        for supported in supported_types:
            if supported == ext:
                self.filetype = ext
                getattr(self.textctrl, "HandleFile_%s" % ext)()
                break

    def Save(self, path=None):
        if path is not None:
            self.SetPath(path)

        data = self.textctrl.GetText()
        try:
            with codecs.open(self.path, "wb", "utf-8") as fp:
                fp.write(data)

            wx.GetApp().WriteLog("debug", "Saved file: %s" % self.path)
        except IOError as exc:
            wx.GetApp().WriteLog("error",
                "Failed to save file: %s" % str(exc))

    def SetPath(self, path):
        self.path = path
        self.filename = os.path.split(path)[1]


        self.GuessType()

