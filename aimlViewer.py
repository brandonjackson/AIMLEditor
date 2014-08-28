#!/usr/bin/env python

# aimlViewer.py
# a basic aiml file viewer

from AIMLParser import AIMLParser
import argparse
import wx
import wx.dataview as dv
from wx.lib.mixins.listctrl import ColumnSorterMixin
import sys
import pprint
import os

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

class Viewer(wx.Frame):

    def __init__(self, parent, id, title, data):
        wx.Frame.__init__(self, parent, id, title, size=(FRAME_WIDTH, FRAME_HEIGHT))

        panel = wx.Panel(self, -1)

        # create the listctrl
        self.dvlc = dvlc = self.createDataView(panel, data)

        # Set the layout so the listctrl fills the panel
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(dvlc, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        panel.SetSizer(hbox)

        # Bind Events
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Show the frame
        self.Centre()
        self.Show(True)

    def createDataView(self, parent, data):
        dvlc = dv.DataViewListCtrl(parent,style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE)

        # Give it some columns.
        dvlc.AppendTextColumn('Pattern', width=self.computeColumnWidth(), mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Response', width=self.computeColumnWidth(), mode=dv.DATAVIEW_CELL_EDITABLE)
        
        # Load the data. Each item (row) is added as a sequence of values
        # whose order matches the columns
        for itemvalues in data:
            dvlc.AppendItem(itemvalues)

        return dvlc

    def computeColumnWidth(self):
        size = self.GetSize()
        return round(size.x*0.5) - 5

    def OnSize(self, event):
        for i in range(0,2):
            col = self.dvlc.GetColumn(i)
            col.SetWidth(self.computeColumnWidth())
        event.Skip()

if __name__ == '__main__':

    # Grab file name from the command line
    parser = argparse.ArgumentParser(description="""A simple AIML file viewer""")
    parser.add_argument("file",help="path to AIML file (or directory of files) to load")
    args = parser.parse_args()

    # Load AIML file and print categoryList
    print "Loading "+args.file+"..."
    AP = AIMLParser(args.file)
    rulesTuples = AP.toCategoryList()
    rules = [list(rule) for rule in rulesTuples] # convert to nested lists for dataview
    print str(len(rules)) + " rules loaded:"
    pprint.pprint(rules)

    app = wx.App()
    title = "aimlViewer: %s" % os.path.abspath(args.file)
    Viewer(None, -1, title, data=rules)
    app.MainLoop()
