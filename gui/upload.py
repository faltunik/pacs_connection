import wx

class ExportFiles(wx.Frame):

    def __init__(self, size=(600, 400), label='Export', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER):
        wx.Frame.__init__(self, None, -1, title= label)# size=size, style= style) 

        self.main_panel = wx.Panel(self, -1)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_panel.SetSizer(self.main_sizer)

        self.main_sizer.Fit(self.main_panel)
        self.main_panel.Layout()
        self.Update()
        self.SetAutoLayout(0)

   
    def create_gui(self):
        self.default_screen()
        self.export_location()
        self.footer_ui()


    def default_screen(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(sizer, 1, wx.EXPAND)


        self.export_options = wx.RadioBox(self.main_panel, label='Export type:', choices=['Selected series', 'Selected study'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        sizer.Add(self.export_options, 0, wx.EXPAND | wx.ALL, 5)

        self.file_format_options = wx.RadioBox(self.main_panel, label='File format:', choices=['DICOM', 'NIFTI', 'JPEG', 'MP4', 'BMP'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        sizer.Add(self.file_format_options, 0, wx.EXPAND | wx.ALL, 5)


    def export_location(self):
        box = wx.StaticBox(self.main_panel, label='Export Location')
        export_location_sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        self.folder_path = wx.TextCtrl(self.main_panel, size=(200,-1))
        export_location_sizer.Add(self.folder_path, 0, wx.ALL, 5)
        self.btn_browse = wx.Button(self.main_panel, wx.ID_OK, "Browse") 
        self.btn_browse.Bind(wx.EVT_BUTTON, self.handle_import)
        export_location_sizer.Add(self.btn_browse, 0, wx.ALL, 5)

        self.main_sizer.Add(export_location_sizer, 0, wx.EXPAND | wx.ALL, 5)

    def footer_ui(self):
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(button_sizer, 0, wx.RIGHT, 5)

        self.btn_export = wx.Button(self.main_panel, wx.ID_OK, "EXPORT") 
        self.btn_cancel = wx.Button(self.main_panel, wx.ID_CANCEL)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

        # button_sizer.Add(self.btn_cancel, 0, wx.ALL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(self.btn_export)
        btnsizer.AddButton(self.btn_cancel)
        btnsizer.Realize()



        


    
    def handle_import(self, event):

        # get event obj
        evt_obj = event.GetEventObject()
        # now we wanna see the selected Export Type
        export_type = self.export_options.GetStringSelection()
        # now we wanna see the selected File Format
        file_format = self.file_format_options.GetStringSelection()

        print(f'export_type: {export_type} and file_format: {file_format}')
        # now we wann opent the windows files to let users select users with the selected file format
        # "DICOM files (*.dcm)|*.dcm|NIFTI files (*.nii)|*.nii|JPEG files (*.jpg)|*.jpg|MP4 files (*.mp4)|*.mp4|BMP files (*.bmp)|*.bmp"
        wildcard = self.wild_card_mapper(file_format)
        if export_type == 'Selected series':
            dialog = wx.FileDialog(None, "Choose a file",
                                wildcard=wildcard,
                                style=wx.FD_OPEN | wx.FD_MULTIPLE)
            if dialog.ShowModal() == wx.ID_OK:
                paths = dialog.GetPaths()
                print("Selected files:")
                self.folder_path.SetValue(paths[0])
                for path in paths:
                    print(path)
            dialog.Destroy()

        else:
            dialog = wx.DirDialog(None, "Choose a directory:",
                                style=wx.DD_DEFAULT_STYLE
                                )
            if dialog.ShowModal() == wx.ID_OK:
                folder_path = dialog.GetPath()
                import os
                files = os.listdir(folder_path)
                # print the names of any files in the folder
                self.folder_path.SetValue(folder_path)
                for file in files:
                    if os.path.isfile(os.path.join(folder_path, file)):
                        print(file)
            dialog.Destroy()

        # TODO: WE NEED TO SELECT SET OF REQUIRED FILES, so let users select folders
        return
    

    def on_cancel(self, event):
        self.Destroy()

    def on_more_option(self, event):

        pass
    

    @staticmethod
    def wild_card_mapper(file_format):
        if file_format == 'DICOM':
            return "DICOM files (*.dcm)|*.dcm"
        elif file_format == 'NIFTI':
            return "NIFTI files (*.nii)|*.nii"
        elif file_format == 'JPEG':
            return "JPEG files (*.jpg)|*.jpg"
        elif file_format == 'MP4':
            return "MP4 files (*.mp4)|*.mp4"
        elif file_format == 'BMP':
            return "BMP files (*.bmp)|*.bmp"
        else:
            return "All files (*.*)|*.*"
    






if __name__ == '__main__':
    app = wx.App()
    frame = ExportFiles()
    frame.create_gui()
    frame.Show()
    app.MainLoop()





