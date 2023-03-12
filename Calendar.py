import calendar
import csv
import datetime
import tkinter as tk


class Calendar:
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
        self.COLOR_OF_SELECTED_EVENT_DATE = "orange"
        self.COLOR_OF_SELECTED_EVENT_DATE_FG = "white"

        self.setup(self.year, self.month)

    # Resets the buttons
    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            # w.destroy()
            self.wid.remove(w)

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
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name

        # Obtaining data
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]

        self.clear()
        self.setup(self.year, self.month)

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

        bold_font = tk.font.Font(family="Helvetica", size=10, weight="bold")
        with open("appointments.txt", 'r') as appFile:
            reader = csv.reader(appFile)
            for row in reader:
                # removes empty list from loop
                if len(row) > 0:
                    # Parse the date into day,month,year
                    dayInt, monthInt, yearInt = row[1].split("/")
                    appointments.append((int(dayInt), int(monthInt), int(yearInt)))
                    bookingPeriod.append(row[3])

        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    allgood = 1
                    shouldBeDisabled = 0
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
                            shouldBeDisabled = 1

                        if indextocheck != actuallastindex:
                            allgood = 0 # Implies both Morning and Evening booked for same day
                    else:
                        color = self.COLOR_OF_DAY_BUTTONS

                    if allgood == 0:  # Both Morning and Evening booked separately for same day
                        b = tk.Button(self.parent, width=1, text=day, state=tk.DISABLED,
                                      bg=self.COLOR_OF_2BOOKINGS_DAY_BUTTONS, fg="black",
                                      command=lambda day=day: self.selection(day, calendar.day_name[day % 7]))
                    else:
                        if shouldBeDisabled == 1:  # Full Day booking
                            b = tk.Button(self.parent, text=day, state=tk.DISABLED, bg=color,
                                          command=lambda day=day: self.selection(day, calendar.day_name[day % 7]))
                        elif day == self.day_selected:
                            b = tk.Button(self.parent, text=day, bg=self.COLOR_OF_SELECTED_EVENT_DATE_FG, font=bold_font,
                                          command=lambda day=day: self.selection(day, calendar.day_name[day % 7]))
                        else:
                            b = tk.Button(self.parent, text=day, bg=color,
                                          command=lambda day=day: self.selection(day, calendar.day_name[day % 7]))

                    self.wid.append(b)
                    b.grid(row=w, column=d)
                else:
                    b = tk.Button(self.parent, text="", bg=self.COLOR_OF_DAY_BUTTONS, fg="black", state=tk.DISABLED)
                    self.wid.append(b)
                    b.grid(row=w, column=d)

        sel = BlinkingLabel(self.parent, height=2, bg=self.COLOR_OF_SELECTED_EVENT_DATE,
                            text='Selected Event date => {} {} {}'.format(
                                calendar.month_name[self.month_selected], self.day_selected, self.year_selected),
                            font=bold_font)
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)

    # Quit out of the calendar and terminate tkinter instance.
    def kill_and_save(self):
        self.parent.destroy()


class BlinkingLabel(tk.Label):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._blink = False
        self._blink_color = self['foreground']
        self.blink()

    def blink(self):
        self._blink = not self._blink
        color = self._blink_color if self._blink else "white"
        self.config(foreground=color)
        self.after(500, self.blink)
