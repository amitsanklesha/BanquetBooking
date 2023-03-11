import calendar
import csv
import datetime
import sys

# imports correct version of tkinter based on python version
if sys.version[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk


class CalendarView:
    # Instantiation
    def __init__(self, parent, values):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
        self.COLOR_OF_CALENDAR_ARROWS = "lightblue"
        self.COLOR_OF_CALENDAR_LABEL = "lightblue"
        self.COLOR_OF_DAY_BUTTONS = "lightblue"
        self.COLOR_OF_APP_FULLDAY_BUTTONS = "red"
        self.COLOR_OF_MORNING_DAY_BUTTONS = "yellow"
        self.COLOR_OF_EVENING_DAY_BUTTONS = "green"
        self.COLOR_OF_2BOOKINGS_DAY_BUTTONS = "blue"

        self.setup(self.year, self.month)

    # Resets the buttons
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            # w.destroy()
            self.wid.remove(w)
        self.wid = []

    # Moves to previous month/year on calendar
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        # self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    # Moves to next month/year on calendar
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        # self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    # Called on date button press
    def selection(self, day, name):
        # Code goes here when user selects a day button.
        pass

    def setup(self, y, m):
        # Tkinter creation
        left = tk.Button(self.parent, text='<', command=self.go_prev, bg=self.COLOR_OF_CALENDAR_ARROWS)
        self.wid.append(left)
        left.grid(row=0, column=1)

        header = tk.Label(self.parent, height=2, bg=self.COLOR_OF_CALENDAR_LABEL,
                          text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)

        right = tk.Button(self.parent, text='>', command=self.go_next, bg=self.COLOR_OF_CALENDAR_ARROWS)
        self.wid.append(right)
        right.grid(row=0, column=5)

        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3], bg=self.COLOR_OF_CALENDAR_LABEL)
            self.wid.append(t)
            t.grid(row=1, column=num)

        # Read Appointments
        appointments = []
        bookingPeriod = []
        with open("appointments.txt", 'r') as appFile:
            reader = csv.reader(appFile)
            for row in reader:
                # removes empty list from loop
                if len(row) > 0:
                    # Parse the date into day,month,year
                    dayInt, monthInt, yearInt = row[1].split("/")
                    appointments.append((int(dayInt), int(monthInt), int(yearInt)))
                    bookingPeriod.append(row[3])

        print("appointments:" + str(appointments))
        monthdayscal = self.cal.monthdayscalendar(y, m)

        if len(monthdayscal) == 5:
            monthdayscal.append([0, 0, 0, 0, 0, 0, 0])
        for w, week in enumerate(monthdayscal, 2):
            for d, day in enumerate(week):
                if day:
                    allgood = 1
                    # determine the color of current calendar day
                    if (day, m, y) in appointments:
                        indextocheck = appointments.index((day, m, y))
                        lastindextocheck = appointments[::-1].index((day, m, y))
                        actuallastindex = len(appointments) - lastindextocheck - 1
                        if bookingPeriod[indextocheck] == "Morning" and indextocheck == actuallastindex:
                            color = self.COLOR_OF_MORNING_DAY_BUTTONS
                        elif bookingPeriod[indextocheck] == "Evening" and indextocheck == actuallastindex:
                            color = self.COLOR_OF_EVENING_DAY_BUTTONS
                        else:
                            color = self.COLOR_OF_APP_FULLDAY_BUTTONS

                        if indextocheck != actuallastindex:
                            allgood = 0
                    else:
                        color = self.COLOR_OF_DAY_BUTTONS

                    if allgood == 0:
                        btn = tk.Button(self.parent, text=day, bg=self.COLOR_OF_2BOOKINGS_DAY_BUTTONS, fg="black",
                                        command=lambda day=day: self.selection(day, calendar.day_name[day % 7]))
                    else:
                        btn = tk.Button(self.parent, text=day, bg=color,
                                        command=lambda day=day: self.selection(day, calendar.day_name[day % 7]))

                    btn.grid(row=w, column=d, sticky='nsew')
                else:
                    btn = tk.Button(self.parent, text="", bg=self.COLOR_OF_DAY_BUTTONS, fg="black", state=tk.DISABLED)
                    btn.grid(row=w, column=d, sticky='nsew')

    # Quit out of the calendar and terminate tkinter instance.
    def kill_and_save(self):
        self.parent.destroy()
