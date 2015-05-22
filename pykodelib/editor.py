"""
Custom wx.Frame class.
"""
import os

import wx

from tabbedview import TabbedView
from config import __wildcard__, settings, Theme, themes

## Menu IDs
ID_SEPARATOR = wx.NewId()

# File menu
ID_NEW = wx.ID_NEW
ID_OPEN = wx.ID_OPEN
ID_SAVE = wx.ID_SAVE
ID_SAVEAS = wx.ID_SAVEAS
ID_CLOSE = wx.ID_CLOSE
ID_CLOSEALL = wx.ID_CLOSE_ALL
ID_QUIT = wx.ID_EXIT

# Edit menu
ID_UNDO = wx.ID_UNDO
ID_REDO = wx.ID_REDO
ID_CUT = wx.ID_CUT
ID_COPY = wx.ID_COPY
ID_PASTE = wx.ID_PASTE
ID_DELETE = wx.ID_DELETE
ID_SELECTALL = wx.ID_SELECTALL

# View menu
ID_STATUSBAR = wx.NewId()
ID_LINENUMBERS = wx.NewId()

# Document menu
ID_GOTO_LINE = wx.NewId()

# Help menu
ID_HELP = wx.NewId()
ID_ABOUT = wx.ID_ABOUT

__menus__ = (
    ("&File", (
        (ID_NEW, "&New\tCtrl+N", "Create a file"),
        (ID_OPEN, "&Open\tCtrl+O", "Open a file"),
        (ID_SAVE, "&Save\tCtrl+S", "Save current file"),
        (ID_SAVEAS, "Save &as...\tCtrl+Shift+S", "Save current file as"),
        (ID_SEPARATOR, None, None),
        (ID_CLOSE, "&Close\tCtrl+W", "Close current file"),
        (ID_CLOSEALL, "C&lose all\tCtrl+Shift+W", "Close all files"),
        (ID_SEPARATOR, None, None),
        (ID_QUIT, "&Quit\tCtrl+Q", "Quit the application")
    )),

    ("&Edit", (
        (ID_UNDO, "&Undo\tCtrl+Z", "Undo previous action"),
        (ID_REDO, "&Redo\tCtrl+Shift+Z", "Redo previous action"),
        (ID_SEPARATOR, None, None),
        (ID_CUT, "Cu&t\tCtrl+X", "Cut selected text"),
        (ID_COPY, "&Copy\tCtrl+C", "Copy selected text"),
        (ID_PASTE, "&Paste\tCtrl+V", "Paste text from clipboard"),
        (ID_DELETE, "&Delete", "Delete selected text"),
    )),

    ("&View", (
        (ID_LINENUMBERS, "xLinenumbers", "Toggle linenumbers visibility"),
    )),
    
    ("&Document", (
        (ID_GOTO_LINE, "Go to line...\tCtrl+G", "Go to a line in the file"),
    )),

    ("&Help", (
        (ID_HELP, "&Help", "Show help docs for PyKode"),
        (ID_SEPARATOR, None, None),
        (ID_ABOUT, "&About", "About PyKode")
    ))
)

# Other variables
__description__ = """PyKode is a lightweight Python IDE designed to be easy to use."""
__copyright__ = """(C) Victor Kindhart 2015 under GPL3"""
__license__ = """GPL3 License"""
__website__ = "http://www.victorkindhart.com/projects/pykode"


class PyKodeEditor(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(PyKodeEditor, self).__init__(*args, **kwargs)
        self.handlers = {
            # File
            ID_NEW:      self.HandleFileNew,
            ID_OPEN:     self.HandleFileOpen,
            ID_SAVE:     self.HandleFileSave,
            ID_SAVEAS:   self.HandleFileSaveAs,
            ID_CLOSE:    self.HandleFileClose,
            ID_CLOSEALL: self.HandleFileCloseAll,
            ID_QUIT:     self.HandleFileQuit,

            # Edit
            ID_UNDO:   self.HandleEditUndo,
            ID_REDO:   self.HandleEditRedo,
            ID_CUT:    self.HandleEditCut,
            ID_COPY:   self.HandleEditCopy,
            ID_PASTE:  self.HandleEditPaste,
            ID_DELETE: self.HandleEditDelete,

            # View
            ID_LINENUMBERS: self.HandleViewLinenumbers,
            
            # Document
            ID_GOTO_LINE: self.HandleDocumentGotoLine,

            # Help
            ID_HELP: self.HandleHelpHelp,
            ID_ABOUT: self.HandleHelpAbout
        }

    def OnInit(self):
        sizer = wx.BoxSizer()
        self.tabbedview = TabbedView(self)
        sizer.Add(self.tabbedview, 1, wx.EXPAND)

        self.SetSizer(sizer)

        self.createMenuBar()
        self.createStatusBar()

        self.about = wx.AboutDialogInfo()
        self.about.SetName("PyKode")
        self.about.SetVersion(wx.GetApp().__version__)
        self.about.SetDescription(__description__)
        self.about.SetCopyright(__copyright__)
        self.about.SetLicense(__license__)
        self.about.SetWebSite(__website__)
        self.about.AddDeveloper("Victor Kindhart")

        return True

    def SetupMenu(self, menu, items):
        for id, text, help in items:
            if id == ID_SEP:
                # Separator
                menu.AppendSeparator()
            elif text[0] == 'x':
                # Check item
                menu.AppendCheckItem(id, text[1:], help)
                self.Bind(wx.EVT_MENU, self.handlers[id], id=id)
            else:
                # Usual item
                menu.Append(id, text, help)
                self.Bind(wx.EVT_MENU, self.handlers[id], id=id)

    def createMenuBar(self):
        self.menubar = wx.MenuBar()

        # Creating menubar
        self.menubar = wx.MenuBar()
        for menu_name, menu_data in __menus__:
            menu = wx.Menu()
            for item in menu_data:
                if item[0] == ID_SEPARATOR:
                    menu.AppendSeparator()
                    continue
                elif item[1][0] == 'x':
                    menu.AppendCheckItem(item[0], item[1][1:], item[2])
                else:
                    menu.Append(item[0], item[1], item[2])

                self.Bind(wx.EVT_MENU, self.handlers[item[0]], id=item[0])
            self.menubar.Append(menu, menu_name)

        self.SetMenuBar(self.menubar)

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()


    # MenuBar event handlers
    # File menu
    def HandleFileNew(self, event):
        self.tabbedview.CreateNewTab()

    def HandleFileOpen(self, event):
        dlg = wx.FileDialog(
            self,
            message="Open file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=__wildcard__,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                self.tabbedview.OpenNewTab(path)

        dlg.Destroy()

    def HandleFileSave(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab.path: # Untitled file
            self.HandleFileSaveAs(event)
        else:
            tab.Save()

    def HandleFileSaveAs(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if tab.path:
            dir, file = os.path.split(tab.path)
        else:
            dir = os.getcwd()
            file = ""
        dlg = wx.FileDialog(
            self,
            message="Save file",
            defaultDir=dir,
            defaultFile=file,
            wildcard=__wildcard__,
            style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            tab.Save(path)
            self.tabbedview.SetPageText(self.tabbedview.GetSelection(),
                tab.filename)

        dlg.Destroy()

    def HandleFileClose(self, event):
        self.tabbedview.CloseCurrentTab()

    def HandleFileCloseAll(self, event):
        self.tabbedview.CloseAllTabs()

    def HandleFileQuit(self, event):
        self.tabbedview.CloseAllTabs()
        self.Destroy()

    # Edit
    def HandleEditUndo(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        tab.textctrl.Undo()

    def HandleEditRedo(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        tab.textctrl.Redo()

    def HandleEditCut(self, event):
        self.HandleEditCopy(event)
        self.HandleEditDelete(event)

    def HandleEditCopy(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        _from, _to = tab.textctrl.GetSelection()
        if _from == _to:
            # No selection
            return

        string = tab.textctrl.GetTextRange(_from, _to)
        self.ClipboardWrite(string)

    def HandleEditPaste(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        string = self.ClipboardRead()
        
        tab.textctrl.ReplaceSelection(string)
        #tab.textctrl.SetSelection(_from + len(string), _from + len(string))

    def HandleEditDelete(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        
        tab.textctrl.Clear()

    def HandleEditSelectAll(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        tab.textctrl.SetSelection(0, -1)

    # View
    def HandleViewLinenumbers(self, event):
        pass
    
    # Document
    def HandleDocumentGotoLine(self, event):
        tab = self.tabbedview.GetCurrentTab()
        if not tab:
            return
        
        dlg = wx.NumberEntryDialog(self,
                    "Enter line number",
                    "",
                    "Go to line...",
                    1, 1, tab.textctrl.GetLineCount())
        dlg.Center()
        
        if dlg.ShowModal() == wx.ID_OK:
            number = dlg.GetValue()
            tab.textctrl.GotoLine(number - 1)
        
        dlg.Destroy()


    # Help
    def HandleHelpHelp(self, event):
        pass

    def HandleHelpAbout(self, event):
        wx.AboutBox(self.about)

    # Other functions
    def ClipboardRead(self):
        if wx.TheClipboard.IsOpened():
            return ""

        data = wx.TextDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(data)
        wx.TheClipboard.Close()
        if success:
            return data.GetText()
        else:
            return ""

    def ClipboardWrite(self, string):
        if wx.TheClipboard.IsOpened():
            return

        data = wx.TextDataObject()
        data.SetText(string)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(data)
        wx.TheClipboard.Close()
