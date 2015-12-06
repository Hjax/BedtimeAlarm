import wx, pyttsx, datetime

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
        self.InitUI()

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)

        self.morning_alarm_enabled = False
        self.night_alarm_enabled = True

        self.alarm_set = False

        self.alarms = []
        
    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetDoubleBuffered(True)

        # Timer for updating the clock
        self.timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.timer.Start(1000)

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

        # This Text Box is the time until the next alarm
        self.time_to_alarm = wx.StaticText(panel, label="Alarm not set!")
        
        # checkboxes to enable / disable alarms
        self.night_alarm = wx.CheckBox(panel, label='Night Alarm')
        self.morning_alarm = wx.CheckBox(panel, label='Morning Alarm')
        self.night_alarm.Bind(wx.EVT_CHECKBOX, self.Toggle_Alarm)
        self.morning_alarm.Bind(wx.EVT_CHECKBOX, self.Toggle_Alarm)

        # these are the text input fields for the times 
        self.wake_time = wx.TextCtrl(panel, -1, size=(140,-1))
        self.wake_time.SetValue('Hours of Sleep')

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

    def time_is_valid(self, time):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return time[0] in numbers and time[1] in numbers and time[2] == ':' and time[3] in numbers and time[4] in numbers and time[6:8] in ['AM', 'PM']

    def time_between(self, a, b):
        hours = int(a[0:2]) -  int(b[0:2)])
        minutes = int(a[3:5]) - int(b[3:5)])
        seconds = int(a[6:8]) - int(b[6:8])
        if seconds < 0:
            seconds += 60
            minutes -= 1
        if minutes < 0:
            minutes += 60
            hours -= 1
        if hours < 0:
            hours += 24
        return hours + ":" + minutes + ":" + seconds

    def pick_closest_time(self, a, b, c):
        time1 = self.time_between(a, b)
        time2 = self.time_between(a, c)
        if time1[0:2] > time2[0:2]:
            return time1
        elif time1[0:2] < time2[0:2]:
            return time2
        elif time1[3:5] > time2[3:5]:
            return time1
        elif time1[3:5] < time2[3:5]:
            return time2
        elif time1[6:8] > time2[6:8]:
            return time1
        elif time1[6:8] < time2[6:8]:
            return time2
        return time1

    def Apply_Settings(self, e):
        if self.time_is_valid(self.current_sleep_time.GetValue()) and self.time_is_valid(self.desired_sleep_time.GetValue()) and self.time_is_valid(self.wake_time.GetValue()):
            if self.current_sleep_time.GetValue()[6:8].lower = 'am':
                self.alarms.append(self.current_sleep_time.GetValue())
            else:
                self.alarms.append(self.current_sleep_time.GetValue()[0:2]+12 + self.current_sleep_time.GetValue()[2:6])
            self.alarms = [self.current_sleep_time.GetValue(), self.wake_time.GetValue()]
            self.alarm_set = True
        else:
             wx.MessageBox('Please Enter Times In The Format: "hh:mm am/pm"', 'Error', wx.OK | wx.ICON_ERROR)

    def Say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def Nag(self, e):
        self.Say("Blah blah blah")

    #   TODO have a fancy runthough animation for the test mode!


    def Update(self, e):
        self.clock.SetLabel(datetime.datetime.now().strftime('%I:%M:%S %p'))

        if self.alarm_set:
            if datetime.datetime.now().strftime('%I:%M:%S %p') == ":00 ".join(self.alarms[0].split(" ")):
                self.Say("Hello World")
            elif datetime.datetime.now().strftime('%I:%M:%S %p') == ":00 ".join(self.alarms[1].split(" ")):
                pass
            if self.pick_closest_time()
            self.time
        
            

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
