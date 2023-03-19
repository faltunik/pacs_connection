#TODO: Show Invesalius Icon in Frame

import time
import wx
import wx.grid as gridlib
import json
from constants import INV_PORT, INV_AET, INV_HOST



def json_serial(filename, mode='r'):
    try:
        with open(filename, mode) as file:
            return json.load(file)
    except Exception as e:
        print("Error: ", e)
        return []


pacs_config_data  = json_serial('pcv1_file.json')
CONFIGURED_PACS = pacs_config_data['configured_pacs']



class CustomDialog(wx.Dialog):
    def __init__(self, parent, message):
        super().__init__(parent, title="Confirmation", size=(250, 150))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        message_label = wx.StaticText(panel, label=message)
        sizer.Add(message_label, 0, wx.ALL | wx.CENTER, 5)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        yes_button = wx.Button(panel, label="Yes")
        no_button = wx.Button(panel, label="No")
        button_sizer.Add(yes_button, 0, wx.ALL | wx.CENTER, 5)
        button_sizer.Add(no_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(button_sizer, 0, wx.CENTER)
        panel.SetSizer(sizer)
        yes_button.Bind(wx.EVT_BUTTON, self.on_yes)
        no_button.Bind(wx.EVT_BUTTON, self.on_no)

    def on_yes(self, event):
        self.EndModal(wx.ID_YES)

    def on_no(self, event):
        self.EndModal(wx.ID_NO)

class Configuration(wx.Frame):
    def __init__(self, size= (600, 400)):
        wx.Frame.__init__(self, None, -1, "PACS Configuration", size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER) 
        self.panel = wx.Panel(self, wx.ID_ANY, size=size)
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        self.pacs_data = self.json_serial('pcv1_file.json')
        self.configured_pacs = self.pacs_data['configured_pacs']
        self.menu_options = self.pacs_data['menu_options']
        self.default_settings = self.pacs_data['default_settings']
        self.pacs_table = None
        self.panel.SetSizer(self.main_layout)
        self.create_ui()

    def create_line(self, horizontal=1):
        if horizontal:
            self.sl = wx.StaticLine(self.panel, 1, style=wx.LI_HORIZONTAL)
        else:
            self.sl = wx.StaticLine(self.panel, 2, style=wx.LI_VERTICAL)
        self.main_layout.Add(self.sl, 0, wx.EXPAND | wx.ALL, 1)

    @staticmethod
    def json_serial(filename, mode='r'):
        try:
            with open(filename, mode) as file:
                return json.load(file)
        except Exception as e:
            print("Error: ", e)
            return []


    
    def create_ui(self):
        self.create_client_info_sizer = self.create_client_info()
        self.main_layout.Add(self.create_client_info_sizer, 0, wx.EXPAND | wx.ALL, 1)
        self.create_line(horizontal=1)
        self.create_pacs_info_sizeer = self.create_pacs_info()
        self.main_layout.Add(self.create_pacs_info_sizeer, 0, wx.EXPAND | wx.ALL, 1)
        self.create_add_pacs_server_sizer = self.create_add_pacs_server()
        self.main_layout.Add(self.create_add_pacs_server_sizer, 0, wx.EXPAND | wx.ALL, 1)
        self.create_footer_sizer = self.create_footer()
        self.main_layout.Add(self.create_footer_sizer, 0, wx.RIGHT | wx.EXPAND | wx.ALL, 1)

        
        return

    def create_label_textbox(self, label='', text_box_value = '', enable=True, textbox_needed=1, horizontal=0, **kwargs):

        if horizontal:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
        else:
            sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self.panel, label=label)
        if kwargs.get('label_size'):
            label.SetSize(kwargs.get('label_size'))
        
        if horizontal:
            sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        else:
            sizer.Add(label, 0, wx.LEFT|wx.TOP|wx.BOTTOM, border=1)

        textbox = wx.TextCtrl(self.panel, value= text_box_value, style=wx.TE_LEFT | wx.TE_PROCESS_ENTER)
        textbox.Enable(enable)
        if kwargs.get('textbox_size'):
            textbox.SetSize(kwargs.get('textbox_size'))
        sizer.AddSpacer(10)  # Add spacer between label and text control
        sizer.Add(textbox, 1, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, border=1)

        #preparing response
        res = [sizer]
        if textbox_needed:
            res.append(textbox)
        return res
        
    def create_button(self, label='', enable=True):
        button = wx.Button(self.panel, label=label)
        button.Enable(enable)
        return button
    
    def create_menu(self,key):
        options = self.menu_options[key]
        menu = wx.Menu()
        for option in options:
            if self.menu_options.get(option, None):
                sub_menu = self.create_menu(option)
                # print(f"sub_menu and children is: {sub_menu.FindChildItem(sub_menu.GetId())}")
                menu.AppendSubMenu(sub_menu, option)
                if option in self.default_settings:
                    default_option = self.default_settings[option]
                    default_menu_item_id = sub_menu.FindItem(default_option)
                    default_menu_item = sub_menu.FindItemById(default_menu_item_id)
                    # default_menu_item.Check(True)
            else:
                menu_item = menu.Append(wx.ID_ANY, option)
                self.Bind(wx.EVT_MENU, self.on_menu_select, menu_item)
                print(option)
                if option == self.default_settings['Query Timeout']:
                    print(self.default_settings['Query Timeout'])
                    # menu_item.Check(True)
        return menu
    
    def on_menu_select(self, event):
        selected_item_id = event.GetId()
        menu = event.GetEventObject()
        selected_item = menu.FindItemById(selected_item_id)
        selected_item_label = selected_item.GetItemLabel()
        # selected_item.Check(True)

        print(f"Selected item: {selected_item_label} (ID: {selected_item_id})")
        event.Skip()

    
    @staticmethod
    def showmsg(t):
        import wx.lib.agw.pybusyinfo as PBI
        app = wx.App(redirect=False)
        msg = 'PACS Details are Deleted'
        title = 'Message!'
        d = PBI.PyBusyInfo(msg, title=title)
        time.sleep(t)
        return d  
    
    
    def on_advance_setting_click(self, event, obj):
        # get the button position and size
        print("event obj details: ", event.GetEventObject().__dict__)
        id_selected = event.GetId()
        event_obj = event.GetEventObject()
        print("Option =", id_selected)
        print(event_obj.GetLabel() )
        pos = self.advanced_settings_button.GetPosition()
        size = self.advanced_settings_button.GetSize()
        self.panel.PopupMenu(obj, pos + (0, size[1]))

    def create_client_info(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #port
        self.port_label, self.port_label_text = self.create_label_textbox(label= 'Listener Port: ', text_box_value = str(INV_PORT), enable=False, textbox_needed=1, horizontal=1)
        main_sizer.Add(self.port_label, 1, wx.EXPAND | wx.ALL, 3)

        # AE Title
        self.ae_title_label, self.ae_title_label_text = self.create_label_textbox(label= 'AE Title: ', text_box_value = INV_AET, enable=False, textbox_needed=1, horizontal=1)
        main_sizer.Add(self.ae_title_label, 1, wx.EXPAND | wx.ALL, 3)

        # Advanced Settings Button
        self.advanced_settings_button = self.create_button(label='Advanced Settings', enable=True)
        self.advanced_settings_button.Bind(wx.EVT_BUTTON, lambda event: self.on_advance_setting_click(event, self.create_menu('advanced_settings')))
        main_sizer.Add(self.advanced_settings_button, 0, wx.EXPAND | wx.ALL, 5)
        #TODO: Find which button is clicked and also mark earlier ticked option
        return main_sizer
    
    def create_header_label(self):
        main_header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer = wx.BoxSizer(wx.VERTICAL)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)


        self.pacs_label = wx.StaticText(self.panel, label='PACS Servers')
        label_sizer.Add(self.pacs_label, 0, wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        main_header_sizer.Add(label_sizer, 0, wx.EXPAND | wx.ALL, 3)

        self.spacer = wx.StaticText(self.panel, label='', size=(150, 10))
        header_sizer.Add(self.spacer, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, border=5)

        self.verify_pacs_button = self.create_button(label='Verify', enable=False)
        header_sizer.Add(self.verify_pacs_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        self.verify_pacs_button.Bind(wx.EVT_BUTTON, lambda event: self.verify_pacs(event, self.grid_table))

        self.delete_pacs_button = self.create_button(label='Delete', enable= False)
        header_sizer.Add(self.delete_pacs_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP|wx.BOTTOM, border=5)
        self.delete_pacs_button.Bind(wx.EVT_BUTTON, lambda event: self.delete_row(event, self.grid_table, self.delete_pacs_button))

        self.up_button = self.create_button(label='Up', enable=False)
        header_sizer.Add(self.up_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP|wx.BOTTOM, border=5)
        self.up_button.Bind(wx.EVT_BUTTON, lambda event: self.on_up(event, self.grid_table, self.up_button))

        self.down_button = self.create_button(label='Down', enable=False)
        header_sizer.Add(self.down_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP|wx.BOTTOM, border=5)
        self.down_button.Bind(wx.EVT_BUTTON, lambda event: self.on_down(event, self.grid_table, self.down_button))

        # now add head_sizer to main_head_sizer in right side
        main_header_sizer.Add(header_sizer, 1, wx.LEFT, 5)

        return main_header_sizer
    
    def create_table(self, array, cols_list):
        self.grid_table = gridlib.Grid(self.panel, wx.ID_ANY, size = (500, 100))
        self.grid_table.CreateGrid(len(array), len(cols_list))
        self.grid_table.AutoSizeColLabelSize(0)
        
        for i,col in enumerate(cols_list):
            self.grid_table.SetColLabelValue(i, col)
            self.grid_table.AutoSizeColLabelSize(i)
            self.grid_table.AutoSize()

        for i, row in enumerate(array):
            for j, val in enumerate(row):
                self.grid_table.SetCellValue(i, j, val)
        self.grid_table.HideRowLabels()
        
        return self.grid_table

    def on_select(self, event, initiator, reactor_list):
        # Enable the button if a row is selected
        row_id = event.GetRow()
        print(row_id)

        initiator.SelectRow(row_id)
        if row_id >= 0:
            for reactor in reactor_list:
                reactor.Enable()
        # fill the self.ip_add, self.port, self.ae_title of form with this data
        self.ip_address_textbox.SetValue(initiator.GetCellValue(row_id, 0))
        self.port_textbox.SetValue(initiator.GetCellValue(row_id, 1))
        self.ae_title_textbox.SetValue(initiator.GetCellValue(row_id, 2))
        self.description_textbox.SetValue(initiator.GetCellValue(row_id, 3))
        # enable all the buttons
        self.ip_add_button.Enable()
        self.ip_edit_button.Enable()

    def on_up(self, event, initiator, reactor):
        row_id = initiator.GetSelectedRows()[0]
        if row_id > 0:
            # initiator.MoveRow(row_id, row_id-1)
            initiator.MoveCursorDown(True)
            initiator.SelectRow(row_id-1)
            reactor.Enable()

        # else:
        #     reactor.Disable()

    def on_down(self, event, initiator, reactor):
        row_id = initiator.GetSelectedRows()[0]
        if row_id < initiator.GetNumberRows()-1:
            initiator.MoveCursorUp(True)
            initiator.SelectRow(row_id+1)
            reactor.Enable()

    def delete_row(self, event, initiator, reactor):
        try:
            row_id = initiator.GetSelectedRows()[0]
            dialog = CustomDialog(self, 'Are you sure you want to delete this IP configuration?')
            if dialog.ShowModal() == wx.ID_YES:
                self.showmsg(3)
                initiator.DeleteRows(row_id)
                self.configured_pacs.pop(row_id)
                with open('pcv1_file.json', 'w') as file:
                    print('Writing to json file')
                    json.dump(self.pacs_data , file)
            # now disable the delete button and empty the textboxes
            self.ip_address_textbox.SetValue('')
            self.port_textbox.SetValue('')
            self.ae_title_textbox.SetValue('')
            self.description_textbox.SetValue('')
        except Exception as e:
            self.show_error_message('Please Select a row to delete')
            print(e)

        self.deselect_rows_pacs(initiator)
        reactor.Disable()
        print(self.configured_pacs)

    def verify_pacs(self, event, initiator):
        #TODO: Write Program to verify pacs server details
        row_id = initiator.GetSelectedRows()[0]
        status = True
        if row_id%2:
            num_cols = initiator.GetNumberCols()
            for col in range(num_cols):
                initiator.SetCellBackgroundColour(row_id, col, wx.GREEN)
        else:
            status= False
            num_cols = initiator.GetNumberCols()
            for col in range(num_cols):
                initiator.SetCellBackgroundColour(row_id, col, wx.GREEN)
        self.deselect_rows_pacs(initiator)
        return status
        
    def deselect_rows(self, initiator, reactor_list):
        print('REACHED HERE 328')
        # initiator.ClearSelection()
        # for reactor in reactor_list:
        #         reactor.Disable()
    
    def deselect_rows_pacs(self, initiator):
        try:
            reactor_list = [self.delete_pacs_button, self.up_button, self.down_button, self.verify_pacs_button]
            self.deselect_rows(initiator, reactor_list)
        except Exception as e:
            print(e)

    def create_pacs_info(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)


        #Labels and Buttons
        main_header_sizer = self.create_header_label()
        main_sizer.Add(main_header_sizer, 0, wx.EXPAND | wx.ALL, 5)

        #grid
        box = wx.StaticBox(self.panel, label='')
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        configured_pacs_columns = ['IP ADDRESS', 'PORT', 'AE TITLE', 'Description', 'Retrievel Protocol', 'Preferred Transfer Syntax']
        self.pacs_table = self.create_table(self.configured_pacs, configured_pacs_columns)
        self.pacs_table.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, lambda event: self.on_select(event, self.pacs_table, [self.verify_pacs_button,self.delete_pacs_button, self.up_button, self.down_button]))
        box_sizer.Add(self.pacs_table, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(box_sizer, 1, wx.EXPAND | wx.ALL, 5)


        return main_sizer

    def create_add_pacs_server(self):
        box = wx.StaticBox(self.panel, label='Add PACS Server')
        main_sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        ip_address, self.ip_address_textbox = self.create_label_textbox(label='IP Address', enable=True, label_size=(10, -1), textbox_size=(30, -1))
        self.ip_address_textbox.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
        main_sizer.Add(ip_address, 0, wx.EXPAND | wx.ALL, 5)

        port, self.port_textbox = self.create_label_textbox(label='Port', enable=True)
        self.port_textbox.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
        main_sizer.Add(port, 0, wx.EXPAND | wx.ALL, 5)

        ae_title, self.ae_title_textbox = self.create_label_textbox(label='AE Title', enable=True)
        self.ae_title_textbox.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
        main_sizer.Add(ae_title, 0, wx.EXPAND | wx.ALL, 5)

        description, self.description_textbox = self.create_label_textbox(label='Description', enable=True)
        # bind description with the on_text_enter fucntion
        self.description_textbox.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
        main_sizer.Add(description, 0, wx.EXPAND | wx.ALL, 5)

        # add button
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ip_add_button = self.create_button(label='Add', enable=False)
        self.ip_add_button.Bind(wx.EVT_BUTTON, lambda event: self.add_pacs_server(event, self.ip_address_textbox, self.port_textbox, self.ae_title_textbox, self.description_textbox))

        self.ip_edit_button = self.create_button(label='Update', enable=False)

        button_sizer.Add(self.ip_add_button, 0, wx.EXPAND | wx.ALL, 5)
        button_sizer.Add(self.ip_edit_button, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)

        return main_sizer
    
    def add_pacs_server(self,evt,ip_address_textbox, port_textbox, ae_title_textbox, description_textbox):
        #TODO: Add Checker to verify if the data are valid or not
        dlg = CustomDialog(self, "Do you want to add this item?")
        result = dlg.ShowModal()
        valid = True  # need to create_function to verify if the data are valid
        if valid and  result == wx.ID_YES:
            #TODO: Add Checker to verify if the pacs server is already added
            try:
                ip_address_value = ip_address_textbox.GetValue()
                port_value = port_textbox.GetValue()
                ae_title_value = ae_title_textbox.GetValue()
                description_value = description_textbox.GetValue()
                configured_pacs_columns = ['IP ADDRESS', 'PORT', 'AE TITLE', 'Description', 'Retrievel Protocol', 'Preferred Transfer Syntax']
                new_data = [ip_address_value, port_value, ae_title_value, description_value, 'DICOM', 'Implicit VR Little Endian']
                self.configured_pacs.append(new_data)
                self.pacs_table.AppendRows(1)
                for col_nu in range(self.pacs_table.GetNumberCols()):
                    self.pacs_table.SetCellValue(self.pacs_table.GetNumberRows()-1, col_nu, new_data[col_nu])

                with open('pcv1_file.json', 'w') as file:
                    print('Writing to json file')
                    json.dump(self.pacs_data , file)

            except Exception as e:
                print(e)
        if not valid and result == wx.ID_YES:
            self.show_error_message('Invalid Data', 'Please check your data')
        
        dlg.Destroy()

        ip_address_textbox.SetValue('')
        port_textbox.SetValue('')
        ae_title_textbox.SetValue('')
        description_textbox.SetValue('')
        return 
    
    def create_footer(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #save button
        save_button = self.create_button(label='Save', enable=True)
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        main_sizer.Add(save_button, 0, wx.Right| wx.EXPAND | wx.ALL, 3)

        #cancel button
        cancel_button = self.create_button(label='Cancel', enable=True)
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        main_sizer.Add(cancel_button, 0, wx.Right| wx.EXPAND | wx.ALL, 3)

        return main_sizer

    def on_save(self, event):
        dlg = CustomDialog(self, "Do you want to save this item?")
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            print('save')
            self.Close()
        dlg.Destroy()
    
    def on_cancel(self, event):
        dlg = CustomDialog(self, "Do you want to cancel this item?")
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            print('cancel')
            self.Close()
        dlg.Destroy()

    def show_error_message(self, message= 'Some Error Occured'):
        msg_dlg = wx.MessageDialog(self, message, "Error", wx.OK | wx.ICON_ERROR)
        msg_dlg.ShowModal()
        msg_dlg.Destroy()

    def on_text_enter(self, event):
        print('enter')
        if self.ip_address_textbox.GetValue() != '' and self.port_textbox.GetValue() != '' and self.ae_title_textbox.GetValue() != '' :
            self.ip_add_button.Enable(True)
            self.ip_edit_button.Enable(True)



if __name__ == "__main__":
    app = wx.App()
    frame = Configuration()
    frame.Show()
    app.MainLoop()
