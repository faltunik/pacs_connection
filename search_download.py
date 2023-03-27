import wx
import wx.adv as wxadv
import wx.grid as gridlib
from cfind import CFind
from pacs_config import  Configuration
from helpers import json_serial
from constants import COLS



pacs_config_data  = json_serial('pcv1_file.json')
CONFIGURED_PACS = pacs_config_data['configured_pacs']
CONFIGURED_PACS_MAPPER = {}
ALL_PACS =[]
for i, pacs_obj in enumerate(CONFIGURED_PACS):
    CONFIGURED_PACS_MAPPER[pacs_obj['AE TITLE']] = pacs_obj
    ALL_PACS.append(pacs_obj['AE TITLE'])

# Now help me in adding typing hints to the following code

class Browse(wx.Frame):
    
    def __init__(self, title:str ="Browse and Download", size:tuple=(800, 550)) -> None:
        wx.Frame.__init__(self, None, -1, title, size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER) 
        self.panel = wx.Panel(self, wx.ID_ANY, size=size)
        self.main_layout = wx.BoxSizer(wx.VERTICAL)
        self.create_ui()
        self.panel.SetSizer(self.main_layout)

    def create_line(self, horizontal=1):
        if horizontal:
            self.sl = wx.StaticLine(self.panel, 1, style=wx.LI_HORIZONTAL)
        else:
            self.sl = wx.StaticLine(self.panel, 2, style=wx.LI_VERTICAL)
        self.main_layout.Add(self.sl, 0, wx.EXPAND | wx.ALL, 1)

    def create_ui(self):
        self.main_layout.Add(self.create_header_1(), 0, wx.EXPAND | wx.ALL, 1)
        self.create_line()
        self.main_layout.Add(self.create_header_2(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_layout.Add(self.create_show_search_result([]), 1, wx.EXPAND | wx.ALL, 1)
        self.main_layout.Add(self.create_image_details(size = (-1,130)), 1, wx.EXPAND | wx.ALL, 1)
        self.main_layout.Add(self.create_footer(),1, wx.RIGHT, 1)


    def create_select_box(self, locations, cur_selection=0, **kwargs):
        combo = wx.ComboBox(self.panel, choices=locations, style =wx.CB_DROPDOWN | wx.CB_SORT)
        combo.SetSelection(cur_selection)
        combo.Bind(wx.EVT_COMBOBOX_CLOSEUP, lambda event: self.on_selection_X(event, combo, **kwargs))
        return combo
    
    def on_selection_X(self, event, obj, **kwargs):
        selected_text = obj.GetStringSelection()
        print(selected_text)
        idx = obj.FindString(selected_text)
        print(idx)
        if kwargs.get('reactors'):
            reactors = kwargs.get('reactors')
            on_option = kwargs.get('on_option')
            if selected_text == on_option or idx == on_option:
                for reactor in reactors:
                    reactor.Enable()
            else:
                for reactor in reactors:
                    reactor.Disable()


    def create_select_date(self):
        pass

    def popup(self, event):
        pop = Configuration()
        pop.Show()

    def on_close(self, event):
        self.Enable()
        event.Skip()

    def on_date_changed(self, event):
        # print("Date changed")
        # cur_date = obj.GetValue()
        # print(cur_date)
        # date = cur_date
        # print(date.FormatISODate())

        try:
            print(event.GetEventObject())
            print(dir (event.GetEventObject()) )
            print(event.GetEventObject().LabelText)
            print(f"cur_date is: {event.GetEventObject().GetValue()}")
        except Exception as e:
            print(f"ERROR IS: {e}")

    def search_result(self, event, **kwargs):
        # we want following information
        # Data Type User has entered: patient id, etc
        # Modalities Box Selections
        # Date Range
        # PACS Location
        # value user has typed in the search box


        self.searching_text.Show()
        print("searching....", self.searching_text.IsShown())
        # get the value of the search box
        search_value = kwargs.get('obj').GetValue()
        # find uner which it : Patient ID, Patient Name, Accession number
        search_type = self.search_type.GetStringSelection()

        # get the value of the modalities box
        modalities = self.modalities.GetTextSelection()

        # get the value of the date range
        start_date_range = self.start_date_range.GetValue()
        # format this in string of "YYYYMMDD"
        start_date_range = start_date_range.FormatISODate().replace('-', '')
        print("*****************************************", type(start_date_range), start_date_range)



        # get the value of the end date range
        end_date_range = self.end_date_range.GetValue().FormatISODate().replace('-', '')

        # get date_range
        print("self data range 241: {self.all_dates.GetValue()}", self.all_dates.GetValue())
        date_range = "19000101-99991231" if self.all_dates.GetValue() == 'ALL' else f"{start_date_range}-{end_date_range}"
        print("242: date_range", date_range)

        # get the value of the pacs location
        pacs_location = self.pacs_location.GetStringSelection()

        # get the value of the data type
        data_type = self.search_type.GetStringSelection()
        data_type = data_type.replace(' ', '')
        print(data_type)
        print("DATA TYPE: ", data_type)
        print("245", pacs_location)
        search_filter = {
            'PatientID': '*',
            'PatientName': '*',
            'AccessionNumber': '*',
        }
        search_filter[data_type] = search_value

        host, port = CONFIGURED_PACS_MAPPER.get(pacs_location).get('IP ADDRESS'), int(CONFIGURED_PACS_MAPPER.get(pacs_location).get('PORT'))

        cfind_obj = CFind(host=host, port = port)
        result = cfind_obj.make_request(aet='', aet_title='',StudyDate= date_range, pacs_location=pacs_location, PatientID= search_filter.get('PatientID', '*'), PatientName= search_filter.get('PatientName', '*'), AccessionNumber=search_filter.get('AccessionNumber', '*'))
        # now we wanna  clear the table
        search_img_table = self.result_table
        # tags = ["PatientName", "PatientID", "StudyInstanceUID", "SeriesInstanceUID"]
        # now we wanna delete existing rows
        if search_img_table.GetNumberRows() > 0:
            search_img_table.DeleteRows(0, numRows=search_img_table.GetNumberRows())
        # now let's add the value
        try:
            tables_data = result 
        except Exception as e:
            print(f"ERROR IS: {e}")
            tables_data = []
        for i in range(len(tables_data)):
            values = tables_data[i]
            search_img_table.AppendRows(numRows=1)
            for col_nu in range(search_img_table.GetNumberCols()):
                cols_name = search_img_table.GetColLabelValue(col_nu)
                cell_value = str(values.get(cols_name, ''))
                
                search_img_table.SetCellValue( max(0, search_img_table.GetNumberRows()-1), col_nu, cell_value )
                search_img_table.SetCellOverflow(max(0, search_img_table.GetNumberRows()-1), col_nu,True)
        self.searching_text.Hide()
                                
        



    def on_clear(self, event, obj):
        obj.SetValue("")

    def on_selection(self, event):
        obj = event.GetEventObject()
        print(obj)
        row_id = event.GetRow()
        print(row_id)
        obj.SelectRow(row_id)
        d = {}
        for col in range(obj.GetNumberCols()):
            # get label of column
            label = obj.GetColLabelValue(col)
            # get value of cell
            value = obj.GetCellValue(row_id, col)
            d[label] = value
            print(label, value)
        
        print(d)

        # so now we wanna clear the previous image details and wanna show this images detail

        # now we wanna show this to the image details panel
        # get the image details panel
        image_details_panel = self.img_details_table # self.main_layout.GetItem(3).GetWindow()
        # get the image details panel sizer
        # image_details_sizer = image_details_panel.GetSizer()
        # now enter the dictionary named d items into this table
        if image_details_panel.GetNumberRows() >0:
            image_details_panel.DeleteRows(0)
        image_details_panel.AppendRows(1)
        for col_nu in range(image_details_panel.GetNumberCols()):
            # get the label of the column
            col_label = image_details_panel.GetColLabelValue(col_nu)
            print(d.get(col_label, "TEST DATA"))
            image_details_panel.SetCellValue(image_details_panel.GetNumberRows()-1, col_nu, d.get(col_label, "TEST DATA"))
        self.download_image_btn.Enable()


    def create_header_1(self):
        """
        TODO:
        Add setting icon in the pacs config button
        Make UI better and response
        Show Pacs Config panel when selected pacs config button
        Let user select multiple options from pacs location and modalities
        Print the user selected options
        Enable the start and end data selection  only when custom date is selected
        Change dates of datebox accordingly when user select last dat, yesterdat etc
        """
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #pacs configuration button
        pacs_config_button = wx.Button(self.panel, label="PACS Config")
        pacs_config_button.Bind(wx.EVT_BUTTON, self.popup)
        main_sizer.Add(pacs_config_button, 0, wx.ALL, 5)

        # pacs location selector
        self.pacs_locations_list = ALL_PACS
        self.pacs_location = self.create_select_box(self.pacs_locations_list, 0)
        main_sizer.Add(self.pacs_location, 0, wx.ALL, 5)

        # modalitites
        # self.modalities_list = ["All Modalities", "CT", "MR", "US", "CR", "DX", "MG", "NM", "OT", "PT", "RF", "SC", "XA", "XC"]
        # self.modalities = self.create_select_box(self.modalities_list, 0)
        # main_sizer.Add(self.modalities, 0, wx.ALL, 5)



        #custom date range
        self.start_date_range = wxadv.DatePickerCtrl(self.panel, style=wxadv.DP_DROPDOWN)
        self.start_date_range.Bind(wxadv.EVT_DATE_CHANGED, self.on_date_changed)
        self.start_date_range.Disable()
        self.end_date_range = wxadv.DatePickerCtrl(self.panel, style=wxadv.DP_DROPDOWN)
        self.end_date_range.Bind(wxadv.EVT_DATE_CHANGED, self.on_date_changed)
        self.end_date_range.Disable()


        # all dates
        self.all_dates_list = ['ALL','Custom']
        self.all_dates = self.create_select_box(self.all_dates_list, 0, reactors=[self.start_date_range, self.end_date_range], on_option='Custom')
        
        main_sizer.Add(self.all_dates, 0, wx.ALL, 5)
        main_sizer.Add(self.start_date_range, 0, wx.ALL, 5)
        main_sizer.Add(self.end_date_range, 0, wx.ALL, 5)

        return main_sizer


    def create_header_2(self):

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #search type
        search_type_list = ["Patient ID", "Patient Name", "Accession Number"]
        self.search_type = self.create_select_box(search_type_list, 0)
        main_sizer.Add(self.search_type, 0, wx.ALL, 5)

        #textbox
        search_text = wx.TextCtrl(self.panel, size=(250, -1) ,style=wx.TE_PROCESS_ENTER)
        search_text.SetHint("Enter Search Text")
        search_text.Bind(wx.EVT_TEXT_ENTER, self.search_result)
        main_sizer.Add(search_text, 0, wx.ALL, 5)

        #search button
        search_button = wx.Button(self.panel, label="Search")
        search_button.Bind(wx.EVT_BUTTON, lambda event :self.search_result(event, obj= search_text))
        main_sizer.Add(search_button, 0, wx.ALL, 5)

        #clear button
        clear_button = wx.Button(self.panel, label="Clear")
        clear_button.Bind(wx.EVT_BUTTON, lambda event : self.on_clear(event, search_text))

        main_sizer.Add(clear_button, 0, wx.ALL, 5)

        return main_sizer
    
    def create_table(self, array, cols_list, size= (-1,200)):
        self.grid_table = gridlib.Grid(self.panel, wx.ID_ANY, size=size)
        self.grid_table.CreateGrid(len(array), len(cols_list))
        self.grid_table.SetDefaultColSize(150)
        
        for i,col in enumerate(cols_list):
            self.grid_table.SetColLabelValue(i, col)

        for i, row in enumerate(array):
            for j, val in enumerate(row):
                self.grid_table.SetCellValue(i, j, str(val))
        self.grid_table.HideRowLabels()

        self.grid_table.SetScrollbars(100, 100, 10, 10)
        return self.grid_table
    
    # def fill_table(self, )
    
    def create_show_search_result(self, arr):
        box = wx.StaticBox(self.panel, label='')
        main_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        cols_list = COLS
        self.result_table = self.create_table(arr, cols_list)
        self.result_table.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.on_selection)
        main_sizer.Add(self.result_table, 1, wx.EXPAND | wx.ALL, 5)
        return main_sizer
    
    def create_image_details(self, size= (-1,200)):
        box = wx.StaticBox(self.panel, label='')
        main_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        cols_list = COLS # ["Patient ID", "Patient Name", "Accession Number", "Modality", "Study Date", "Study Time", "Study Description"]
        self.img_details_table= self.create_table([], cols_list, size= size)
        main_sizer.Add(self.img_details_table, 1, wx.EXPAND | wx.ALL, 5)
        return main_sizer
    
    def create_footer(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #buttons
        #TODO: Shift the buttons to the right
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.download_image_btn = wx.Button(self.panel, label = 'Download')
        self.download_image_btn.Disable()
        button_sizer.Add(self.download_image_btn, 0, wx.ALL, 5)
        # Searching Text String, it will be disabled but will be enabled once user enter the search button
        self.searching_text = wx.StaticText(self.panel, label="Searching...")
        button_sizer.Add(self.searching_text, 0, wx.ALL, 5)
        self.searching_text.Hide()
 
        main_sizer.Add(button_sizer, 1, wx.RIGHT, 1)
        return main_sizer


if __name__ == '__main__':
    app = wx.App()
    frame = Browse()
    frame.Show()
    app.MainLoop()
