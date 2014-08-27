#!/usr/bin/env python

# aimlViewer.py
# a basic aiml file viewer

from AIMLParser import AIMLParser
import argparse
import wx
from wx.lib.mixins.listctrl import ColumnSorterMixin
import sys
import pprint

# Grab file name from the command line
parser = argparse.ArgumentParser(description="""A simple AIML file viewer""")
parser.add_argument("file",help="path to AIML file (or directory of files) to load")
args = parser.parse_args()

# Load AIML file and print categoryList
print "Loading "+args.file+"..."
AP = AIMLParser(args.file)
rules = AP.toCategoryList()
print str(len(rules)) + " rules loaded:"
pprint.pprint(rules)

class Viewer(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 230))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)

        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Pattern:', wx.LIST_FORMAT_RIGHT, width=250)
        self.list.InsertColumn(1, 'Response:', width=250)

        for i in rules:
            index = self.list.InsertStringItem(sys.maxint, i[0])
            self.list.SetStringItem(index, 1, i[1])

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

app = wx.App()
Viewer(None, -1, args.file)
app.MainLoop()
