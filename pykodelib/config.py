import json
import os

import wx

if wx.Platform == "__WXMSW__":
    _font = "Courier New"
    _size = 10
elif wx.Platform == "__WXMAC__":
    _font = "Monospace"
    _size = 12
else:
    _font = "Monospace"
    _size = 12

class Theme(object):
    def __init__(self, theme):
        self.theme = theme
        self.name = theme["name"]
        self.format = "fore:%s,back:%s,face:%s,size:%d"

    @staticmethod
    def Exists(theme):
        return Theme.GetTheme(theme) != None

    @staticmethod
    def GetTheme(theme):
        for themeobj in themes:
            if themeobj.name == theme:
                return themeobj

        return None

    def GetStyle(self, item):
        style = self.theme[item]
        string = self.format % tuple(style[:4])
        if style[4]:
            string += ",italic"
        if style[5]:
            string += ",bold"
        if style[6]:
            string += ",underline"
        if style[7]:
            string += ",eol"
        return string

DEFAULT_THEME = {
    "name": "PyKode Default",
    # item   :   [fore, back, font, size, italic, bold, underline, eol]
    "default":   ["#222222", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "comment1":  ["#7F7F7F", "#FFFFFF", _font, _size, 1, 0, 0, 0],
    "comment2":  ["#7F7F7F", "#FFFFFF", _font, _size, 1, 0, 0, 0],
    "number":    ["#8F0000", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "ssstr":     ["#237F23", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "dsstr":     ["#237F23", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "ststr":     ["#237F23", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "dtstr":     ["#237F23", "#FFFFFF", _font, _size, 1, 0, 0, 0],
    "keyword":   ["#12127F", "#FFFFFF", _font, _size, 0, 1, 0, 0],
    "clsname":   ["#3434FF", "#FFFFFF", _font, _size, 0, 1, 0, 0],
    "funcname":  ["#005FCF", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "operator":  ["#555555", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "id":        ["#222222", "#FFFFFF", _font, _size, 0, 0, 0, 0],
    "streol":    ["#000000", "#FFA0B0", _font, _size, 0, 0, 0, 1],
}

DEFAULT_CFG = {
    "linenumbers": True,
    "theme": "PyKode Default"
}

themes = []
themes.append(Theme(DEFAULT_THEME))

userdir = os.path.expanduser("~")
if userdir == "~":
    raise RuntimeError("not a user-based OS??")

homedir = os.path.join(userdir, ".pykode")
if not os.path.exists(homedir):
    os.mkdir(homedir)

config_fn = os.path.join(homedir, "pykode.json")
themes_fn = os.path.join(homedir, "themes.cfg")

if not os.path.exists(config_fn):
    with open(config_fn, "w") as fp:
        json.dump(DEFAULT_CFG, fp)

with open(config_fn, "r") as fp:
    settings = json.load(fp)

if os.path.exists(themes_fn):
    with open(themes_fn, "r") as fp:
        _themes = json.load(fp)

    for theme in _themes:
        themes.append(Theme(theme))

theme = Theme.GetTheme(settings["theme"])
if theme:
    settings["themeobj"] = theme
else:
    settings["themeobj"] = Theme.GetTheme("PyKode Default")
    wx.GetApp().WriteLog("warning",
        "Theme \"%s\" not found, falling back to \"PyKode Default\"" %
        theme)

supported_types = [
    "py"
]

__wildcard__ = (
    "Python source (*.py, *.pyw)|*.py;*.pyw|"
    "Plain text file (*.txt)|*.txt|"
    "All files (*.*)|*.*"
)