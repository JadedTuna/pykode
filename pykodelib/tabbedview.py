"""
Custom wx.aui.AuiNotebook class.
"""
import wx
import wx.lib.agw.aui as aui

from tab import Tab

PK_TV_STYLE = (aui.AUI_NB_TOP |
                aui.AUI_NB_TAB_MOVE |
                aui.AUI_NB_CLOSE_ON_ALL_TABS |
                aui.AUI_NB_TAB_FIXED_WIDTH |
                aui.AUI_NB_SCROLL_BUTTONS)


class TabbedView(aui.AuiNotebook):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = PK_TV_STYLE
        super(TabbedView, self).__init__(*args, **kwargs)
        self.SetArtProvider(aui.FF2TabArt())

    def CreateNewTab(self):
        page = Tab(self)
        self.AddPage(page, "Untitled", True)

    def OpenNewTab(self, path):
        page = Tab(self)
        if page.Load(path):
            self.AddPage(page, page.filename, True)

    def GetCurrentTab(self):
        index = self.GetSelection()
        if index == -1:
            return None
        else:
            return self.GetPage(index)

    def CloseCurrentTab(self):
        index = self.GetSelection()
        if index != -1:
            self.DeletePage(index)

    def CloseAllTabs(self):
        while self.GetPageCount():
            self.DeletePage(self.GetSelection())
