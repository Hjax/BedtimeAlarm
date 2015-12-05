import wx, pyttsx,time

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.InitUI()

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)
        
    def InitUI(self):    

        panel = wx.Panel(self)

        hbox = wx.BoxSizer()
        sizer = wx.GridSizer(2, 2, 2, 2)

        btn1 = wx.Button(panel, label='Nag')
        btn2 = wx.Button(panel, label='2')
        btn3 = wx.Button(panel, label='3')
        btn4 = wx.Button(panel, label='4')

        sizer.AddMany([btn1, btn2, btn3, btn4])

        hbox.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizer(hbox)

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

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
