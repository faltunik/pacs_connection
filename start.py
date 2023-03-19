"""
So we wanna have a screen to let users seelect 3 ooptions
1. Configure PACS Connection
2. Search and Download DICOM
3. Upload DICOM to PACS
"""
import wx
from pacs_config import Configuration


class StartScreen(wx.Frame):
    def __init__(self, title = "Start Screen", size=(300, 200)):
        super().__init__(None, wx.ID_ANY,title= title, size=size)
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.AddStretchSpacer(1)    
        self.main_panel.SetSizer(self.main_sizer)
        self.Center()

        self.create_ui()

    def create_ui(self):
        self.start_ui()

    def create_button(self, label, event= None, **kwargs):
        button = wx.Button(self.main_panel, label=label)
        if event:
            button.Bind(wx.EVT_BUTTON, event)
        return button
    
    def start_ui(self):
        self.pacs_connection_button = self.create_button('PACS Configuration', self.on_pacs_configuration)
        self.search_and_download_button = self.create_button('Search and Download DICOM', self.on_search_and_download)
        self.upload_dicom_button = self.create_button('Upload DICOM to PACS', self.on_upload_dicom)

        self.main_sizer.Add(self.pacs_connection_button, 0, wx.ALIGN_CENTER_HORIZONTAL, border =10)
        self.main_sizer.Add(self.search_and_download_button, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)
        self.main_sizer.Add(self.upload_dicom_button, 0, wx.ALIGN_CENTER_HORIZONTAL, border=10)

        self.main_sizer.AddStretchSpacer(1)

        return 
    

    def on_pacs_configuration(self, event):
        print('PACS Connection')
        self.pacs_config = Configuration()
        self.pacs_config.Show()


    def on_search_and_download(self, event):
        print('Search and Download DICOM')

    def on_upload_dicom(self, event):
        print('Upload DICOM to PACS')

if __name__ == "__main__":
    app = wx.App()
    frame = StartScreen()
    frame.Show()
    app.MainLoop()

