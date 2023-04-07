import wx
import wx.adv as wxadv
import wx.grid as gridlib

class DownloadHistory(wx.Frame):

    def __init__(self, title:str ="Download History", size:tuple=(500, 350)) -> None:
        wx.Frame.__init__(self, None, -1, title, size =size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.panel = wx.Panel(self, wx.ID_ANY, size=size)
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        self.create_ui()


    def create_ui(self):
        self.main_layout.Add(self.create_grid(), 1, wx.ALL|wx.EXPAND, 15)
        self.main_layout.Add(self.create_footer(), 0, wx.ALL|wx.EXPAND, 5)
        return
    
    def create_table(self, array:list, cols_list:list, size:tuple= (500,300)) -> gridlib.Grid:
        tmp_table = gridlib.Grid(self.panel, wx.ID_ANY, size= size)
        tmp_table.CreateGrid(len(array), len(cols_list))
        tmp_table.SetDefaultColSize(100)
        
        for i,col in enumerate(cols_list):
            tmp_table.SetColLabelValue(i, col)

        for i, row in enumerate(array):
            for j, val in enumerate(row):
                tmp_table.SetCellValue(i, j, str(val))
        tmp_table.HideRowLabels()

        tmp_table.SetScrollbars(100, 100, 10, 10)
        return tmp_table


    def create_grid(self):
        cols_list = ['Patient Name', 'Study Date', 'Size', 'Progress', 'Download Time', 'Bytes Transferred', 'PACS Location']
        array = [ ['John Doe', '2020-01-01', '1.2 MB', '100%', '2020-01-01 12:00:00', '1.2 MB', 'PACS Server 1'], ['Jane Doe', '2020-01-01', '1.2 MB', '100%', '2020-01-01 12:00:00', '1.2 MB', 'PACS Server 1'] ]
        self.grid_table = self.create_table(array, cols_list)

        box = wx.StaticBox(self.panel, label='')
        main_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        #self.result_table.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.on_selection)
        main_sizer.Add(self.grid_table, 1, wx.EXPAND | wx.ALL, 5)
        return main_sizer


    def create_footer(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #cancel button
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        #disable the button
        self.cancel_button.Disable()
        main_sizer.Add(self.cancel_button, 0, wx.ALL, 5)

        return main_sizer
    
    def on_cancel(self, event):
        # get row id of selected row
        #TODO: Cancel the download of selected file
        pass