#!/usr/bin/env python

# aimlViewer.py
# a basic aiml file viewer

from AIMLParser import AIMLParser
import argparse
import wx
from wx.lib.mixins.listctrl import ColumnSorterMixin
import sys
import pprint
import os

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
COLUMN_WIDTH = FRAME_WIDTH / 2

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
        wx.Frame.__init__(self, parent, id, title, size=(FRAME_WIDTH, FRAME_HEIGHT))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)

        # Create List Schema
        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Pattern', wx.LIST_FORMAT_RIGHT, width=COLUMN_WIDTH)
        self.list.InsertColumn(1, 'Response', width=COLUMN_WIDTH)

        # Add Rules to List
        for i in rules:
            index = self.list.InsertStringItem(sys.maxint, i[0])
            self.list.SetStringItem(index, 1, i[1])

        # Event Bindings
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Put Together the Pieces...
        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        # ..and show them!
        self.Centre()
        self.Show(True)

    def OnSize(self, event):
        size = self.GetSize()
        patternColumnWidth = round(size.x*0.5)
        responseColumnWidth = size.x - patternColumnWidth
        self.list.SetColumnWidth(0, patternColumnWidth)
        self.list.SetColumnWidth(1, responseColumnWidth)
        event.Skip()

app = wx.App()
title = "aimlViewer: %s" % os.path.abspath(args.file)
Viewer(None, -1, title)
app.MainLoop()
