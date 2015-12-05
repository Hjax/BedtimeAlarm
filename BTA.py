import wx, pyttsx, datetime

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.InitUI()

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)
        
    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetDoubleBuffered(True)

        # Timer for updating the clock
        self.timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.UpdateDisplay, self.timer)
        self.timer.Start(50)

        # The test button
        btn1 = wx.Button(panel, label='Test')
        btn1.Bind(wx.EVT_BUTTON, self.Nag)

        # The text box that contains the current time
        self.clock = wx.StaticText(panel, label=datetime.datetime.now().strftime('%H:%M:%S'))
        font = wx.Font(128, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.clock.SetFont(font)

        vbox = wx.BoxSizer(wx.VERTICAL)
        outer_grid = wx.GridSizer(1, 2, 0, 0)
        inner_grid = wx.GridSizer(3, 2, 100, 100)

        inner_grid.AddMany([wx.StaticText(panel, label="bleh"), wx.StaticText(panel, label="bleh"),
                            wx.StaticText(panel, label="bleh"), wx.StaticText(panel, label="bleh"),
                            wx.StaticText(panel, label="bleh"), wx.StaticText(panel, label="bleh")])
        
        outer_grid.Add(inner_grid)
        outer_grid.Add(btn1, wx.ALIGN_CENTER)
        vbox.Add(self.clock, flag=wx.ALIGN_CENTER)
        vbox.Add(outer_grid, 1, wx.EXPAND | wx.ALL)

        panel.SetSizer(vbox)
        

        # Sets up the menus
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Quit, fitem)

        # Final Init Stuff
        self.SetSize((800, 600))
        self.SetTitle('Bed Time Alarm Pre-Alpha')
        self.Centre()
        self.Show(True)
        
    def Quit(self, e):
        self.Close()

    def Nag(self, e):
        self.engine.say("It is time for you to go to bed")
        self.engine.runAndWait()

    #   TODO have a fancy runthough animation for the test mode!

    def UpdateDisplay(self, e):
        self.clock.SetLabel(datetime.datetime.now().strftime('%H:%M:%S'))

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
