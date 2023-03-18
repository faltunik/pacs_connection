import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.advance_button = wx.Button(self, label='Advanced Options')
        self.advance_button.Bind(wx.EVT_BUTTON, self.on_advance_button)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.advance_button, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)

    def on_advance_button(self, event):
        # Set the minimum size of the panel to expand it
        self.SetMinSize((self.GetSize()[0], self.GetSize()[0]+200))

        self.GetParent().Layout()

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        panel = MyPanel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
