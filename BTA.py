import wx, pyttsx, datetime

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.InitUI()

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)
        
    def InitUI(self):

        self.timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.UpdateDisplay, self.timer)
        self.timer.Start(200)

        panel = wx.Panel(self)

        btn1 = wx.Button(panel, label='Nag', pos=(100, 250))

        self.clock = wx.StaticText(panel, label=datetime.datetime.now().strftime('%H:%M:%S'), pos=(50, 25))
        font = wx.Font(128, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.clock.SetFont(font)

        btn1.Bind(wx.EVT_BUTTON, self.Nag)
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.Quit, fitem)

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
