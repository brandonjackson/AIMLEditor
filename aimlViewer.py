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


class TestModel(dv.PyDataViewIndexListModel):
    def __init__(self, data):
        dv.PyDataViewIndexListModel.__init__(self, len(data))
        self.data = data

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        return "string"

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        return self.data[row][col]

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        print("SetValue: (%d,%d) %s\n" % (row, col, value))
        self.data[row][col] = value

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return len(self.data[0])

    # Report the number of rows in the model
    def GetCount(self):
        #self.log.write('GetCount')
        return len(self.data)
    
    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        ##self.log.write('GetAttrByRow: (%d, %d)' % (row, col))
        #if col == 3:
        #    attr.SetColour('blue')
        #    attr.SetBold(True)
        #    return True
        return False


    # # This is called to assist with sorting the data in the view.  The
    # # first two args are instances of the DataViewItem class, so we
    # # need to convert them to row numbers with the GetRow method.
    # # Then it's just a matter of fetching the right values from our
    # # data set and comparing them.  The return value is -1, 0, or 1,
    # # just like Python's cmp() function.
    # def Compare(self, item1, item2, col, ascending):
    #     if not ascending: # swap sort order?
    #         item2, item1 = item1, item2
    #     row1 = self.GetRow(item1)
    #     row2 = self.GetRow(item2)
    #     if col == 0:
    #         return cmp(int(self.data[row1][col]), int(self.data[row2][col]))
    #     else:
    #         return cmp(self.data[row1][col], self.data[row2][col])

        
    def DeleteRows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)
        
        for row in rows:
            # remove it from our data structure
            del self.data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)
            
            
    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()

class Viewer(wx.Frame):

    def __init__(self, parent, id, title, data):
        wx.Frame.__init__(self, parent, id, title, size=(FRAME_WIDTH, FRAME_HEIGHT))

        panel = wx.Panel(self, -1)

        # create the listctrl
        self.model = TestModel(data)
        self.dvlc = dvlc = self.createDataView(panel, self.model)

        # Set the layout so the listctrl fills the panel
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(dvlc, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        panel.SetSizer(hbox)

        # Bind Events
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Show the frame
        self.Centre()
        self.Show(True)

    def createDataView(self, parent, model):
        dvlc = dv.DataViewListCtrl(parent,style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE)

        dvlc.AssociateModel(model)

        # Give it some columns.
        colWidth = self.computeColumnWidth()
        dvlc.AppendTextColumn('Pattern', 0, mode=dv.DATAVIEW_CELL_EDITABLE, width=colWidth)
        dvlc.AppendTextColumn('Response', 1, mode=dv.DATAVIEW_CELL_EDITABLE, width=colWidth)
        
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
