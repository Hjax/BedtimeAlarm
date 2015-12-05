import wx, pyttsx, datetime

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.InitUI()

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)

        self.morning_alarm_enabled = False
        self.night_alarm_enabled = True


        
    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetDoubleBuffered(True)

        # Timer for updating the clock
        self.timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.UpdateDisplay, self.timer)
        self.timer.Start(50)

        # The test button
        btn1 = wx.Button(panel, label='Test', size=(300, 300))
        btn1.Bind(wx.EVT_BUTTON, self.Nag)

        # The apply settings button
        apply_btn = wx.Button(panel, label='Apply')
        apply_btn.Bind(wx.EVT_BUTTON, self.Apply_Settings)

        # The text box that contains the current time
        self.clock = wx.StaticText(panel, label=datetime.datetime.now().strftime('%I:%M:%S %p'))
        font = wx.Font(100, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.clock.SetFont(font)

        vbox = wx.BoxSizer(wx.VERTICAL)
        outer_grid = wx.GridSizer(1, 2, 0, 0)
        inner_grid = wx.GridSizer(3, 3, 100, 25)
        
        # checkboxes to enable / disable alarms
        self.night_alarm = wx.CheckBox(panel, label='Night Alarm')
        self.morning_alarm = wx.CheckBox(panel, label='Morning Alarm')
        self.night_alarm.Bind(wx.EVT_CHECKBOX, self.Toggle_Alarm)
        self.morning_alarm.Bind(wx.EVT_CHECKBOX, self.Toggle_Alarm)

        # these are the text input fields for the times 
        self.wake_time = wx.TextCtrl(panel, -1, size=(140,-1))
        self.wake_time.SetValue('Wake Up Time')

        self.current_sleep_time = wx.TextCtrl(panel, -1, size=(140,-1))
        self.current_sleep_time.SetValue('Current Bed Time')

        self.desired_sleep_time = wx.TextCtrl(panel, -1, size=(140,-1))
        self.desired_sleep_time.SetValue('Desired Bed Time')
        
        # set up the UI layout
        inner_grid.Add(self.night_alarm, flag=wx.ALIGN_CENTER)
        inner_grid.Add(self.current_sleep_time)
        inner_grid.Add(self.desired_sleep_time)
        inner_grid.Add(self.morning_alarm, flag=wx.ALIGN_CENTER)
        inner_grid.Add(self.wake_time)
        inner_grid.Add(wx.StaticText(panel, label=""))
        inner_grid.Add(apply_btn, flag=wx.ALIGN_CENTER)
        inner_grid.Add(wx.StaticText(panel, label="Time Until Next Alarm:"))
        inner_grid.Add(wx.StaticText(panel, label="bleh"))
        
        outer_grid.Add(inner_grid)
        outer_grid.Add(btn1, flag=wx.ALIGN_CENTER)
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
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Centre()
        self.Show(True)
        
    def Quit(self, e):
        self.Close()

    def Toggle_Alarm(self, e):
        sender = e.GetEventObject()
        if sender == self.morning_alarm:
            self.morning_alarm_enabled = sender.GetValue()
        else:
            self.night_alarm_enabled = sender.GetValue()

    def Apply_Settings(self, e):
        pass

    def Nag(self, e):
        self.engine.say("How dare you press the button")
        self.engine.runAndWait()

    #   TODO have a fancy runthough animation for the test mode!

    def UpdateDisplay(self, e):
        self.clock.SetLabel(datetime.datetime.now().strftime('%I:%M:%S %p'))
        
            

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
