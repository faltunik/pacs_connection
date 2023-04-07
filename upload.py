import wx
from components import BasicCompo

class ExportFiles(wx.Frame):

    def __init__(self, label='Export', title='Upload', size= (-1, -1), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER):
        wx.Frame.__init__(self, None, -1, title, size =size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER) 
        self.main_panel = wx.Panel(self, wx.ID_ANY, size=size)
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(self.main_layout)
        self.create_gui()
   
    def create_gui(self):
        self.main_layout.Add(self.default_screen(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_layout.Add(self.file_settings(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_layout.Add(self.export_location(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_layout.Add(self.footer_ui(), 0, wx.EXPAND | wx.ALL, 1)
        #self.main_panel.Layout()

    def default_screen(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        #create components
        self.export_options = wx.RadioBox(self.main_panel, label='Export type:', choices=['Selected Series', 'Selected study'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.file_format_options = wx.RadioBox(self.main_panel, label='File format:', choices=['DICOM', 'NIFTI', 'JPEG', 'MP4', 'BMP'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        
        #bind components with event
        self.file_format_options.Bind(wx.EVT_RADIOBOX, self.on_file_format_options)

        # add components to sizer
        sizer.Add(self.export_options, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.file_format_options, 0, wx.EXPAND | wx.ALL, 5)

        return sizer

    def on_file_format_options(self, event):
        # if user select JPEG, then JPEG Quality slider gets enabled, image size get enabled and annotation gets enabled
        print('CLicking 33')
        evt_obj = event.GetEventObject()
        print(evt_obj.GetSelection(), type(evt_obj.GetSelection()))
        if evt_obj.GetSelection() == 2:
            print('HERE WE ARe')
            self.jpeg_quality.Enable()
            self.image_size_options.Enable()
            self.annotation_options.Enable()
            #others get diabled
            self.frame_rate.Disable()
            print('DONE SIDE EFECT 43')

        # on mp4, frame rate gets enabled and others get disabled
        elif evt_obj.GetSelection() == 3:
            self.frame_rate.Enable()
            self.jpeg_quality.Disable()
            self.image_size_options.Disable()
            self.annotation_options.Disable()
        
        else:
            self.jpeg_quality.Disable()
            self.image_size_options.Disable()
            self.annotation_options.Disable()
            self.frame_rate.Disable()


    def export_location(self):
        box = wx.StaticBox(self.main_panel, label='Export Location')
        export_location_sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        #self.main_sizer.Add(export_location_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.folder_path = wx.TextCtrl(self.main_panel, size=(200,-1))
        export_location_sizer.Add(self.folder_path, 0, wx.ALL, 5)
        self.btn_browse = wx.Button(self.main_panel, wx.ID_OK, "Browse") 
        self.btn_browse.Bind(wx.EVT_BUTTON, self.handle_import)
        export_location_sizer.Add(self.btn_browse, 0, wx.ALL, 5)
        return export_location_sizer

    def file_settings(self):
        box = wx.StaticBox(self.main_panel, label='File Settings')
        file_settings_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        # image size: Radio Box
        self.image_size_options = wx.RadioBox(self.main_panel, label='Image size:', choices=['Default(1:1)', 'Fit' 'Custom'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        file_settings_sizer.Add(self.image_size_options, 0, wx.EXPAND | wx.ALL, 5)
        self.image_size_options.Disable()

        # Annotation: Radio Box
        self.annotation_options = wx.RadioBox(self.main_panel, label='Annotation:', choices=['None', 'Basic', 'Full'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        file_settings_sizer.Add(self.annotation_options, 0, wx.EXPAND | wx.ALL, 5)
        self.annotation_options.Disable()

        # JPEG Quality: Slider
        # I wanna add label for JPEG Quality slider
        jpeg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_label = wx.StaticText(self.main_panel, label='JPEG Quality')
        jpeg_sizer.Add(text_label, 0, wx.ALL, 5)
        self.jpeg_quality = wx.Slider(self.main_panel, value=100, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.jpeg_quality.Disable()
        jpeg_sizer.Add(self.jpeg_quality, 0, wx.ALL, 5)
        # self.jpeg_quality.SetTick(0, 'Small')
        # self.jpeg_quality.SetTick(100, 'Large')
        # self.jpeg_quality.SetTickFreq(100)
        file_settings_sizer.Add(jpeg_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Frame Rate : Radio but also a customize option where user can input the numberical value and that box gets active only when radio option is custom. IN default, it will be disabled
        self.frame_rate = wx.RadioBox(self.main_panel, label='Frame rate', choices=['DEFAULT', 'CUSTOM'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)      
        self.frame_rate.Disable()  
        self.custom_box = wx.SpinCtrl(self.main_panel, value='30', min=1, max=1000)
        self.custom_box.Disable() 
        # bind event to radio box, so that when user select custom, the custom box gets enabled
        self.frame_rate.Bind(wx.EVT_RADIOBOX, self.on_radio_box) 
        file_settings_sizer.Add(self.frame_rate, 0, wx.EXPAND | wx.ALL, 5) 
        file_settings_sizer.Add(self.custom_box, 0, wx.EXPAND | wx.ALL, 5)
        return file_settings_sizer


    def on_radio_box(self, event):
        if self.frame_rate.GetSelection() == 1:
            self.custom_box.Enable()
        else:
            self.custom_box.Disable()
   

    def footer_ui(self):
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_export = wx.Button(self.main_panel, wx.ID_OK, "EXPORT") 
        button_sizer.Add(self.btn_export, 0, wx.ALL, 5)
        self.btn_cancel = wx.Button(self.main_panel, wx.ID_CANCEL)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        button_sizer.Add(self.btn_cancel, 0, wx.ALL, 5)

        # button_sizer.Add(self.btn_cancel, 0, wx.ALL, 5)
        # btnsizer = wx.StdDialogButtonSizer()
        # btnsizer.AddButton(self.btn_export)
        # btnsizer.AddButton(self.btn_cancel)
        return button_sizer

    
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
    



class UploadFiles(wx.Frame):
    
    def __init__(self):
        super().__init__(parent=None, size= (-1, 620), title='Upload Files')
        self.panel = wx.Panel(self)
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.main_layout)
        self.create_gui()

    def create_gui(self):
        self.main_layout.Add(self.create_export_option(), 0, wx.EXPAND | wx.ALL, 5)
        self.main_layout.Add(self.create_file_format_option(), 0, wx.EXPAND | wx.ALL, 5)
        self.main_layout.Add(self.create_export_location(), 0, wx.EXPAND | wx.ALL, 5)
        self.main_layout.Add(self.create_file_settings(), 0, wx.EXPAND | wx.ALL, 5)
        self.main_layout.Add(self.create_footer(), 0, wx.EXPAND | wx.ALL, 5)
        pass

    def create_export_option(self):
        self.export_options = wx.RadioBox(self.panel, label='Export', choices=['Selected series', 'Selected Studies'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        
        return self.export_options
    
    def create_file_format_option(self):
        self.file_format_options = wx.RadioBox(self.panel,label='File Format', choices=['DICOM', 'NIFTI', 'JPEG', 'MP4', 'BMP'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        #bind with on_file_format_selection
        self.file_format_options.Bind(wx.EVT_RADIOBOX, self.on_file_format_selection)
        return self.file_format_options
    
    def create_export_location(self):
        border = wx.StaticBox(self.panel, label='Export Location')
        box = wx.StaticBoxSizer(border, wx.VERTICAL)
        browse_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.folder_form, self.folder_form_textbox= BasicCompo.create_label_textbox(self.panel, 'Folder Name', '', True,horizontal=1 )
        self.folder_browse_button = BasicCompo.create_button(self.panel, 'Browse', True)

        self.filename_form, self.filename_textbox = BasicCompo.create_label_textbox(self.panel, 'File Name', '', True,horizontal=1 )

        browse_sizer.Add(self.folder_form, 0, wx.EXPAND | wx.ALL, 5)
        browse_sizer.Add(self.folder_browse_button, 0, wx.EXPAND | wx.ALL, 5)

        box.Add(browse_sizer, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(self.filename_form, 0, wx.EXPAND | wx.ALL, 5)
        return box

    def create_file_settings(self):
        #TODO: Create Form for customiziing the image_size and frame_rate
        border = wx.StaticBox(self.panel, label='File Settings')
        sizer= wx.StaticBoxSizer(border, wx.VERTICAL)
        self.image_size = wx.RadioBox(self.panel, label='image size', choices=['Original', 'Default(1:1)', 'Custom'], majorDimension=2, style=wx.RA_SPECIFY_ROWS)
        self.annotations = wx.RadioBox(self.panel, label='Annotations', choices=['None', 'Default', 'Custom'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.frame_rate = wx.RadioBox(self.panel, label='Frame Rate', choices=['Default', 'Custom'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.jpeg_conf = wx.BoxSizer(wx.HORIZONTAL)
        self.jpeg_label = wx.StaticText(self.panel, label='JPEG Quality')
        self.jpeg_quality = BasicCompo.create_slider(self.panel, 'JPEG Quality',100, 0, 100)
        self.jpeg_quality.Disable()
        self.jpeg_conf.Add(self.jpeg_label, 0, wx.EXPAND | wx.ALL, 5)
        self.jpeg_conf.Add(self.jpeg_quality, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.image_size, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.annotations, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.frame_rate, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.jpeg_conf, 0, wx.EXPAND | wx.ALL, 5)

        return sizer

    def create_footer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = BasicCompo.create_button(self.panel, 'Cancel', True)
        self.cancel_button.SetPosition((self.GetSize().GetWidth() - self.cancel_button.GetSize().GetWidth(), 50))
        self.export_button = BasicCompo.create_button(self.panel, 'Export', True)
        self.export_button.SetPosition((self.GetSize().GetWidth() - self.export_button.GetSize().GetWidth(), 0))


        sizer.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.export_button, 0, wx.EXPAND | wx.ALL, 5)
        return sizer

    def on_cancel(self, event):
        self.Close()
    
    def on_export(self, event):
        pass

    def on_file_format_selection(self, event):
        event = event.GetEventObject()
        file_format = event.GetStringSelection()
        print(file_format)

        if file_format  in  ['JPEG', 'BITMAP']:
            print('HERE 290')
            self.jpeg_quality.Enable()
        
        return








if __name__ == '__main__':
    app = wx.App()
    frame = UploadFiles()
    frame.Show()
    app.MainLoop()





