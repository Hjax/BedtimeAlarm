import wx, pyttsx, datetime, time



class BTA(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(BTA, self).__init__(*args, **kwargs) 
        self.InitUI()

        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 130)

        self.morning_alarm_enabled = True
        self.night_alarm_enabled = True

        self.morning_alarm = "00:00:00"
        self.night_alarm = "00:00:00"

        self.alarm_set = False
        self.running_demo = False

        self.pause_time = 0

        self.current_time = datetime.datetime.now().strftime('%H:%M:%S')

        
    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetDoubleBuffered(True)

        # Timer for updating the clock
        self.timer = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.timer.Start(1000)

        # The test button
        btn1 = wx.Button(panel, label='Try Me', size=(300, 300))
        btn1.Bind(wx.EVT_BUTTON, self.Nag)

        # The apply settings button
        apply_btn = wx.Button(panel, label='Apply')
        apply_btn.Bind(wx.EVT_BUTTON, self.Apply_Settings)

        # The text box that contains the current time
        self.clock = wx.StaticText(panel, label=datetime.datetime.now().strftime('%H:%M:%S'))
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
        inner_grid.Add(self.time_to_alarm)
        
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
        return time[0] in numbers and time[1] in numbers and time[2] == ':' and time[3] in numbers and time[4] in numbers

    def time_between(self, b, a):
        hours = int(a[0:2]) -  int(b[0:2])
        minutes = int(a[3:5]) - int(b[3:5])
        seconds = int(a[6:8]) - int(b[6:8])
        if seconds < 0:
            seconds += 60
            minutes -= 1
        if minutes < 0:
            minutes += 60
            hours -= 1
        if hours < 0:
            hours += 24
        return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    def pick_closest_time(self, a, b, c):
        time1 = self.time_between(a, b)
        time2 = self.time_between(a, c)

        if int(time1[0:2]) < int(time2[0:2]):
            return b
        elif int(time1[0:2]) > int(time2[0:2]):
            return c
        elif int(time1[3:5]) < int(time2[3:5]):
            return b
        elif int(time1[3:5]) > int(time2[3:5]):
            return c
        elif int(time1[6:8]) < int(time2[6:8]):
            return b
        elif int(time1[6:8]) > int(time2[6:8]):
            return c
        return b

    def add_times(self, a, b):
        hours = int(a[0:2]) +  int(b[0:2])
        minutes = int(a[3:5]) + int(b[3:5])
        seconds = int(a[6:8]) + int(b[6:8])
        if seconds >= 60:
            seconds -= 60
            minutes += 1
        if minutes >= 60:
            minutes -= 60
            hours += 1
        if hours >= 24:
            hours -= 24
        return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    def adjust_towards(self, a, b):
        if self.time_between(a, b)[0:2] == '00' and int(self.time_between(a, b)[3:5]) < 5:
            return b
        if self.time_between(b, a)[0:2] == '00' and int(self.time_between(b, a)[3:5]) < 5:
            return b                                              
        return self.add_times(a, "23:55:00")


    def Apply_Settings(self, e): 
        if self.time_is_valid(self.current_sleep_time.GetValue()) and self.time_is_valid(self.desired_sleep_time.GetValue()) and self.time_is_valid(self.wake_time.GetValue()):
            self.morning_alarm = self.add_times(self.wake_time.GetValue(), self.desired_sleep_time.GetValue())
            self.night_alarm = self.current_sleep_time.GetValue()
            self.alarm_set = True
        else:
             wx.MessageBox('Please Enter Times In The Format: "hh:mm"', 'Error', wx.OK | wx.ICON_ERROR)

    def Say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def Nag(self, e):
        self.timer.Stop()
        self.running_demo = True
        self.timer.Start(1)

    #   TODO have a fancy runthough animation for the test mode!


    def Update(self, e):
        if (time.time() - self.pause_time) > 2:
            if self.running_demo:
                if self.alarm_set:
                    next_event = self.pick_closest_time(self.current_time, datetime.datetime.now().strftime('%H:%M:%S'), self.pick_closest_time(self.current_time, self.night_alarm, self.morning_alarm))
                else:
                    next_event = datetime.datetime.now().strftime('%H:%M:%S')
                if int(self.time_between(self.current_time, next_event)[0:2]) >= 1:
                    self.current_time = self.add_times(self.current_time, "00:11:00")
                if int(self.time_between(self.current_time, next_event)[3:5]) >= 1:
                    self.current_time = self.add_times(self.current_time, "00:00:11")
                else:
                    self.current_time = self.add_times(self.current_time, "00:00:01")
                if self.current_time == datetime.datetime.now().strftime('%H:%M:%S'):
                    self.running_demo = False
                    self.timer.Stop()
                    self.timer.Start(1000)
            else: 
                self.current_time = datetime.datetime.now().strftime('%H:%M:%S')
            self.clock.SetLabel(self.current_time)

            if self.alarm_set:
                if self.current_time == self.night_alarm and self.night_alarm_enabled:
                    self.pause_time = time.time()
                    self.Say("It is time for you to go to bed")
                    self.night_alarm = self.adjust_towards(self.night_alarm, self.desired_sleep_time.GetValue())
                    self.current_sleep_time.SetValue(self.night_alarm[0:5])   
                if self.current_time == self.morning_alarm and self.morning_alarm_enabled:
                    self.pause_time = time.time()
                    self.Say("It is time for you to wake up")

                self.time_to_alarm.SetLabel(self.time_between(self.current_time, self.pick_closest_time(self.current_time, self.night_alarm, self.morning_alarm)))

            
def main():
    
    ex = wx.App()
    BTA(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
