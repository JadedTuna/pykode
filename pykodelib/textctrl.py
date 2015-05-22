"""
Custom wx.stc.StyledTextCtrl class.
"""
import os
import re
import keyword

import wx
import wx.stc

from config import settings

removeSingleStrings = re.compile("'.*?'").sub
removeDoubleStrings = re.compile("\".*?\"").sub
removeComments = re.compile("#.+").sub


class TextCtrl(wx.stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        wx.stc.StyledTextCtrl.__init__(self, *args, **kwargs)
        self._tab = "    "
        self.OnInit()

    def OnInit(self):
        self.SetDefaultStyle()
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)

    def SetDefaultStyle(self):
        theme = settings["themeobj"]

        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, theme.GetStyle("default"))
        self.StyleClearAll()

        # Default styles for all languages
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, theme.GetStyle("default"))

        #self.SetProperty("fold", "1")
        self.SetMargins(0, 0)
        self.SetMarginWidth(0, 34)

        self.SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        
        self.SetCaretLineBackground("#EEEEEE")
        self.SetCaretLineVisible(True)

    def HandleFile_py(self):
        theme = settings["themeobj"]

        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        # Python styles
        # Default
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, theme.GetStyle("default"))
        # Single comment
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, theme.GetStyle("comment1"))
        # Double comment (comment block)
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, theme.GetStyle("comment2"))
        # Number
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, theme.GetStyle("number"))
        # Single quoted string
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, theme.GetStyle("ssstr"))
        # Double quoted string
        self.StyleSetSpec(wx.stc.STC_P_STRING, theme.GetStyle("dsstr"))
        # Single quoted string (triple)
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, theme.GetStyle("ststr"))
        # Double quoted string (triple)
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, theme.GetStyle("dtstr"))
        # Keyword
        self.StyleSetSpec(wx.stc.STC_P_WORD, theme.GetStyle("keyword"))
        # Class name definition
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, theme.GetStyle("clsname"))
        # Function or method name definition
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, theme.GetStyle("funcname"))
        # Operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, theme.GetStyle("operator"))
        # Identifiers
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, theme.GetStyle("id"))
        # EOL
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL, theme.GetStyle("streol"))
    
    def PythonEndsWithColon(self, line):
        line = removeSingleStrings("", line)
        line = removeDoubleStrings("", line)
        line = removeComments("", line)
        
        return line.rstrip().endswith(':')

    def OnKeyPressed(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_TAB:
            self.AddText(self._tab)
        elif key == wx.WXK_RETURN:
            index = self.GetCurrentLine()
            line = self.GetLine(index)
            self.AddText(os.linesep + " " * self.GetLineIndentation(index))
            if self.PythonEndsWithColon(line):
                self.AddText(self._tab)
        else:
            event.Skip()
