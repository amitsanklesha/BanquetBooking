import tkinter as tk
import csv
import os.path
from tkinter import messagebox
from tkinter.ttk import Combobox

import docx
import win32api
from PIL import Image, ImageTk
from Calendar import Calendar
from CalendarView import CalendarView
from datetime import date
from tkcalendar import DateEntry


root = tk.Tk()
root.title("Kalash Banquet Booking")
# Tkinter Vars
username = tk.StringVar()
password = tk.StringVar()
name = tk.StringVar()
loggedInLabel = tk.StringVar()


# Functions
def setup():
    # Used to make the two textfiles if they don't already exist
    file_exists = os.path.isfile("users.txt")
    if file_exists:
        pass
    else:
        file = open("users.txt", "w+")
        file.close()
    file_exists = os.path.isfile("appointments.txt")
    if file_exists:
        pass
    else:
        file = open("appointments.txt", "w+")
        file.close()


def raiseFrame(frame):
    frame.tkraise()


def moveToReg():
    raiseFrame(regFrame)


def moveToLogin():
    raiseFrame(start)


def moveToPrint():
    for widget in printAppointmentFrame.winfo_children():
        widget.destroy()
    create_and_print_word_document()
    raiseFrame(printAppointmentFrame)


def moveToBook():
    for widget in bookAppointmentFrame.winfo_children():
        widget.destroy()
    bookAppointmentCall()
    raiseFrame(bookAppointmentFrame)


def moveToUpdate():
    for widget in updateAppointmentFrame.winfo_children():
        widget.destroy()
    updateButtonClick()
    raiseFrame(updateAppointmentFrame)


def moveToCancelByPartyName():
    for widget in cancelAppointmentFrameByPartyName.winfo_children():
        widget.destroy()
    cancelFrameWorkByPartyName()
    raiseFrame(cancelAppointmentFrameByPartyName)


def moveToCancelByDate():
    for widget in cancelAppointmentFrameByDate.winfo_children():
        widget.destroy()
    cancelFrameWorkByDate()
    raiseFrame(cancelAppointmentFrameByDate)


# Calendar
def moveToUser():
    for widget in userFrame.winfo_children():
        widget.destroy()
    createUserFrame()
    raiseFrame(userFrame)


def register():
    entries = []
    with open("users.txt", 'a', newline="") as userFile:
        writer = csv.writer(userFile)
        writeList = [name.get(), username.get(), password.get()]
        writer.writerow(writeList)
        userFile.close()
    # Clear entry boxes
    username.set("")
    password.set("")
    raiseFrame(start)


def create_and_print_word_document():
    # Create a new Word document
    doc = docx.Document()

    # Add some text to the document
    doc.add_paragraph('Hello, World!')

    # Save the document to a file
    doc.save('D:\Ashok\my_word_document.docx')

    # Print the document using the default printer
    win32api.ShellExecute(0, "print", "D:\Ashok\my_word_document.docx", None, ".", 0)


def createUserFrame():
    # Set welcome message
    loggedInLabel.set("Kalash Banquet Appointment")

    # Calendar View
    global calendarViewFrame
    calendarViewFrame = tk.Frame(userFrame, borderwidth=5, bg="lightblue")
    calendarViewFrame.grid(row=2, column=1, columnspan=5)
    viewCalendar = CalendarView(calendarViewFrame, {name.get()})

    tk.Label(userFrame, image=bookingimagePH, bg='lightblue').grid(row=2, column=5)

    tk.Label(userFrame, textvariable=loggedInLabel, font=("Courier", 44), bg='lightblue', fg="blue").grid(row=1,
                                                                                                          column=1,
                                                                                                          columnspan=5)
    tk.Button(userFrame, font=("Courier", 18), bg='cyan', padx=15, pady=8, text="Book",
              command=moveToBook).grid(row=3, column=2)
    tk.Button(userFrame, font=("Courier", 18), bg='cyan', padx=15, pady=8, text="Cancel (By Party name)",
              command=moveToCancelByPartyName).grid(row=3, column=3)
    tk.Button(userFrame, font=("Courier", 18), bg='cyan', padx=15, pady=8, text="Update",
              command=moveToUpdate).grid(row=3, column=4)
    tk.Button(userFrame, font=("Courier", 18), bg='cyan', padx=15, pady=8, text="Print",
              command=moveToPrint).grid(row=3, column=5)
    tk.Button(userFrame, font=("Courier", 18), bg='cyan', padx=15, pady=8, text="Cancel (By date)",
              command=moveToCancelByDate).grid(row=4, column=3)
    tk.Button(userFrame, font=("Courier", 18), bg='cyan', padx=15, pady=8, text="Log Out", command=logOut).grid(row=4,
                                                                                                                column=4)


def validate_input(new_text):
    if "," in new_text:
        return False
    return True


def bookAppointmentCall():
    tk.Label(bookAppointmentFrame, text="Book an Appointment", font=("Courier", 44), bg='lightblue').grid(row=1, column=1,
                                                                                                          columnspan=5)
    tk.Label(bookAppointmentFrame, text="Party Name:", font=("Courier", 18), bg='lightblue').grid(row=2, column=1)
    tk.Label(bookAppointmentFrame, text="Select Event Date: ", font=("Courier", 18), bg='lightblue').grid(row=3, column=1)
    tk.Label(bookAppointmentFrame, text="Select Booking period: ", font=("Courier", 18), bg='lightblue').grid(row=4,
                                                                                                              column=1)
    tk.Label(bookAppointmentFrame, text="Agreed Final Price", font=("Courier", 18), bg='lightblue').grid(row=5, column=1)
    tk.Label(bookAppointmentFrame, text="Booking Amount", font=("Courier", 18), bg='lightblue').grid(row=6, column=1)
    tk.Label(bookAppointmentFrame, text="Booking Date (defaulted to today)", font=("Courier", 18), bg='lightblue').grid(
        row=7, column=1)

    # Book Appointment frame/window starts
    # Party Name
    validate_cmd = bookAppointmentFrame.register(validate_input)
    partyName = tk.Entry(bookAppointmentFrame, borderwidth=5, background="white", width=35, validate='key', validatecommand=(validate_cmd, "%P"))
    partyName.grid(row=2, column=2, columnspan=35)

    calendarFrame = tk.Frame(bookAppointmentFrame, borderwidth=5, bg="lightblue")
    calendarFrame.grid(row=3, column=2, columnspan=5)
    datePickercalendar = Calendar(calendarFrame, {})

    tk.Label(bookAppointmentFrame, image=bookingimagePH, bg='lightblue').grid(row=3, column=8)

    # Booking Period Selector
    bookingPeriodFrame = tk.Frame(bookAppointmentFrame, borderwidth=5, bg="lightblue")
    bookingPeriodFrame.grid(row=4, column=2)
    bookingPeriodComboBox = Combobox(bookingPeriodFrame, background="lightblue",
                                     values=("Morning", "Evening", "Full Day"))
    bookingPeriodComboBox.grid(row=4, column=2)

    # Agreed Final Price
    validateInt = (bookAppointmentFrame.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    agreedFinalPrice = tk.Entry(bookAppointmentFrame, borderwidth=5, background="white", width=15, validate='key',
                                validatecommand=validateInt)
    agreedFinalPrice.grid(row=5, column=2)

    # Booking Amount
    validateInt1 = (bookAppointmentFrame.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    bookingAmount = tk.Entry(bookAppointmentFrame, borderwidth=5, background="white", width=15, validate='key',
                             validatecommand=validateInt1)
    bookingAmount.grid(row=6, column=2)

    # Booking Date (defaulted to today)
    date_var = tk.StringVar()
    date_var.set(date.today().strftime("%d/%m/%Y"))
    date_entry_when_booked = DateEntry(bookAppointmentFrame, width=12, textvariable=date_var, date_pattern="dd/mm/yyyy")
    date_entry_when_booked.grid(row=7, column=2)

    # Book Appointment screen buttons
    tk.Button(bookAppointmentFrame, font=("Courier", 18), bg='cyan', text="Make Appointment",
              command=lambda: makeAppointment(calendarViewFrame, datePickercalendar, partyName, bookingPeriodComboBox, agreedFinalPrice, bookingAmount, date_entry_when_booked)).grid(row=8, column=2)
    tk.Button(bookAppointmentFrame, font=("Courier", 18), bg='cyan', text="Back", command=moveToUser).grid(row=8, column=1)
    # Book Appointment frame/window ends


def makeAppointment(calendarViewFrame, datePickercalendar, partyName, bookingPeriodComboBox, agreedFinalPrice, bookingAmount, date_entry_when_booked):
    # Format date
    bookingDate = str(datePickercalendar.day_selected) + "/" + str(datePickercalendar.month_selected) + "/" + str(
        datePickercalendar.year_selected)

    with open("appointments.txt", 'a', newline="") as appFile:
        writer = csv.writer(appFile)
        writeList = [name.get(), bookingDate, partyName.get(), bookingPeriodComboBox.get(), agreedFinalPrice.get(), bookingAmount.get(), date_entry_when_booked.get()]
        writer.writerow(writeList)
        appFile.close()
    messagebox.showinfo("Success!", "Appointment made!")
    moveToUser()


def cancelAppointmentByName(optionmenu_var):
    entry = optionmenu_var.get()
    with open("appointments.txt", 'r') as f:
        lines = f.readlines()
    with open("appointments.txt", 'w') as f:
        for line in lines:
            if len(line) > 4 and line.strip().split(',')[2] != entry:
                f.write(line)

    messagebox.showinfo("Success!", "{} booking deleted!".format(str(entry)))
    calendarViewFrame = tk.Frame(userFrame, borderwidth=5, bg="lightblue")
    calendarViewFrame.grid(row=2, column=1, columnspan=5)
    viewCalendar = CalendarView(calendarViewFrame, {name.get()})
    moveToUser()


def cancelAppointmentByDate(optionmenu_var):
    entry = optionmenu_var.get()
    with open("appointments.txt", 'r') as f:
        lines = f.readlines()
    with open("appointments.txt", 'w') as f:
        for line in lines:
            if len(line) > 4 and line.strip().split(',')[1] != entry.split('|')[0]:
                f.write(line)
            elif len(line) > 4 and line.strip().split(',')[3] != entry.split('|')[1]:
                f.write(line)

    messagebox.showinfo("Success!", "{} booking deleted!".format(str(entry)))
    calendarViewFrame = tk.Frame(userFrame, borderwidth=5, bg="lightblue")
    calendarViewFrame.grid(row=2, column=1, columnspan=5)
    viewCalendar = CalendarView(calendarViewFrame, {name.get()})
    moveToUser()


def cancelFrameWorkByPartyName():
    # Cancel Appointment by Party Name frame/window starts
    tk.Label(cancelAppointmentFrameByPartyName, text="By Party Name:", font=("Courier", 18), bg='lightblue').grid(row=3, column=3)

    values = readAppointmentsForPartyName()

    cancelFrame = tk.Frame(cancelAppointmentFrameByPartyName, borderwidth=5, bg="lightblue")
    cancelFrame.grid(row=4, column=3)

    optionmenu_var = tk.StringVar(cancelAppointmentFrameByPartyName)
    optionmenu_var.set(values[0])

    optionmenu = tk.OptionMenu(cancelFrame, optionmenu_var, *values)
    optionmenu.grid(row=4, column=3, columnspan=75)

    # Cancel Appointment by Party Name screen buttons
    tk.Button(cancelAppointmentFrameByPartyName, font=("Courier", 18), bg='cyan', text="Cancel Appointment",
              command=lambda: cancelAppointmentByName(optionmenu_var)).grid(row=8, column=3)
    tk.Button(cancelAppointmentFrameByPartyName, font=("Courier", 18), bg='cyan', text="Back", command=moveToUser).grid(row=8, column=4)
    # Cancel Appointment by Party Name frame/window ends


def cancelFrameWorkByDate():
    # Cancel Appointment by Date frame/window starts
    tk.Label(cancelAppointmentFrameByDate, text="By Date:", font=("Courier", 18), bg='lightblue').grid(row=3, column=3)

    values = readAppointmentsForBookingPeriod()

    cancelFrameByDate = tk.Frame(cancelAppointmentFrameByDate, borderwidth=5, bg="lightblue")
    cancelFrameByDate.grid(row=4, column=3)

    optionmenu_var = tk.StringVar(cancelAppointmentFrameByDate)
    optionmenu_var.set(values[0])

    optionmenu = tk.OptionMenu(cancelFrameByDate, optionmenu_var, *values)
    optionmenu.grid(row=4, column=3, columnspan=75)

    # Cancel Appointment by Date screen buttons
    tk.Button(cancelAppointmentFrameByDate, font=("Courier", 18), bg='cyan', text="Cancel Appointment",
              command=lambda: cancelAppointmentByDate(optionmenu_var)).grid(row=8, column=3)
    tk.Button(cancelAppointmentFrameByDate, font=("Courier", 18), bg='cyan', text="Back", command=moveToUser).grid(row=8, column=4)
    # Cancel Appointment by Date frame/window ends


# Define a function to update the labels
def update_values_with_data(*args):
    updateindex = updatePartyNameArray.index(update_optionmenu_var.get())
    booking_amount_entry_var.set(updatePaymentDoneArray[updateindex])
    event_date_entry_var.set(updateEventDateArray[updateindex])
    booked_period_entry_var.set(updateBookingPeriodArray[updateindex])
    booking_date_entry_var.set(updateBookingDateArray[updateindex])
    final_price_entry_var.set(updateFinalFullPriceArray[updateindex])


def updateButtonClick():
    tk.Label(updateAppointmentFrame, text="Update an Appointment", font=("Courier", 44), bg='lightblue').grid(row=1, column=1,
                                                                                                          columnspan=5)
    tk.Label(updateAppointmentFrame, text="Party Name:", font=("Courier", 18), bg='lightblue').grid(row=2, column=1)
    tk.Label(updateAppointmentFrame, text="Booked Event Details: ", font=("Courier", 18), bg='lightblue').grid(row=3,
                                                                                                            column=1)
    tk.Label(updateAppointmentFrame, text="Select Event Date: ", font=("Courier", 18), bg='lightblue').grid(row=4, column=1)
    tk.Label(updateAppointmentFrame, text="Select Booking period: ", font=("Courier", 18), bg='lightblue').grid(row=5,
                                                                                                              column=1)
    tk.Label(updateAppointmentFrame, text="Agreed Final Price:", font=("Courier", 18), bg='lightblue').grid(row=6, column=1)
    tk.Label(updateAppointmentFrame, text="Booking Amount:", font=("Courier", 18), bg='lightblue').grid(row=7, column=1)
    tk.Label(updateAppointmentFrame, text="Re-Booking Date (defaulted to today):", font=("Courier", 18), bg='lightblue').grid(
        row=8, column=1)

    values = readAppointmentsAllData()

    updatePartyNameArray.clear()
    updateEventDateArray.clear()
    updateBookingPeriodArray.clear()
    updatePaymentDoneArray.clear()
    updateBookingDateArray.clear()
    updateFinalFullPriceArray.clear()

    for item in values:
        if len(item) > 4:
            updatePartyNameArray.append(item.split(',')[2])
            updateEventDateArray.append(item.split(',')[1])
            updateBookingPeriodArray.append(item.split(',')[3])
            updatePaymentDoneArray.append(item.split(',')[5])
            updateBookingDateArray.append(item.split(',')[6])
            updateFinalFullPriceArray.append(item.split(',')[4])

    # Current booking details to be displayed
    tk.Label(updateAppointmentFrame, textvariable=event_date_entry_var, font=("Courier", 12), bg='lightblue').grid(row=3, column=2)

    # Event Date
    # Create a variable to hold the state of the checkbox
    checkbox_state = tk.BooleanVar()

    # Create a Checkbutton and associate it with the variable
    checkbox = tk.Checkbutton(updateAppointmentFrame, text="Select if change of date\n and/or booking period", variable=checkbox_state, bg="lightblue")
    checkbox.grid(row=4, column=2)

    updatecalendarFrame = tk.Frame(updateAppointmentFrame, borderwidth=5, bg="lightblue")
    updatecalendarFrame.grid(row=4, column=3, columnspan=5)
    updatePickercalendar = Calendar(updatecalendarFrame, {})

    tk.Label(updateAppointmentFrame, image=bookingimagePH, bg='lightblue').grid(row=4, column=9)

    # Booking Period
    updatebookingPeriodFrame = tk.Frame(updateAppointmentFrame, borderwidth=5, bg="lightblue")
    updatebookingPeriodFrame.grid(row=5, column=2)
    updatebookingPeriodComboBox = Combobox(updateAppointmentFrame, background="lightblue", values=("Morning", "Evening", "Full Day"), textvariable=booked_period_entry_var)
    updatebookingPeriodComboBox.grid(row=5, column=2)

    # Option menu for Party Name
    update_optionmenu_var.set("")
    optionmenu = tk.OptionMenu(updateAppointmentFrame, update_optionmenu_var, *updatePartyNameArray,
                               command=update_values_with_data)
    optionmenu.grid(row=2, column=2, columnspan=45)

    # Agreed final Price
    validateUpdateInt1 = (updateAppointmentFrame.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    agreedUpdateFinalPrice = tk.Entry(updateAppointmentFrame, borderwidth=5, background="white", width=15, validate='key',
                                      validatecommand=validateUpdateInt1, textvariable=final_price_entry_var)
    agreedUpdateFinalPrice.grid(row=6, column=2)

    # Booking Amount
    updatebookingAmount = tk.Entry(updateAppointmentFrame, borderwidth=5, background="white", width=15, textvariable=booking_amount_entry_var, validate='key', validatecommand=validateUpdateInt1)
    updatebookingAmount.grid(row=7, column=2)

    update_date_var = tk.StringVar()
    update_date_var.set(date.today().strftime("%d/%m/%Y"))
    update_date_entry_when_booked = DateEntry(updateAppointmentFrame, width=12, textvariable=booking_date_entry_var, date_pattern="dd/mm/yyyy")
    update_date_entry_when_booked.grid(row=8, column=2)

    # Update Appointment screen buttons
    tk.Button(updateAppointmentFrame, font=("Courier", 18), bg='cyan', text="Update Appointment",
              command=lambda: updateAppointment(updatecalendarFrame, updatePickercalendar, update_optionmenu_var,
                                              updatebookingPeriodComboBox, agreedUpdateFinalPrice, updatebookingAmount,
                                              update_date_entry_when_booked, checkbox_state)).grid(row=9, column=2)
    tk.Button(updateAppointmentFrame, font=("Courier", 18), bg='cyan', text="Back", command=gobackfromupdate).grid(row=9, column=1)
    # Update Appointment frame/window ends


def gobackfromupdate():
    booking_amount_entry_var.set("")
    event_date_entry_var.set("")
    booked_period_entry_var.set("")
    booking_date_entry_var.set("")
    final_price_entry_var.set("")
    moveToUser()


def updateAppointment(calendarViewFrame, datePickercalendar, partyName, bookingPeriodComboBox, agreedFinalPrice, bookingAmount, date_entry_when_booked, checkbox_state):
    # Format date
    if checkbox_state.get():
        bookingDate = str(datePickercalendar.day_selected) + "/" + str(datePickercalendar.month_selected) + "/" + str(
            datePickercalendar.year_selected)
        bookingPeriod = bookingPeriodComboBox.get()

    with open("appointments.txt", 'r') as f:
        lines = f.readlines()
        if not checkbox_state.get():
            for line in lines:
                if len(line) > 4 and line.strip().split(',')[2] == partyName.get():
                    bookingDate = line.strip().split(',')[1]
                    bookingPeriod = line.strip().split(',')[3]
                    break

    with open("appointments.txt", 'w') as f:
        for line in lines:
            if len(line) > 4 and line.strip().split(',')[2] != partyName.get():
                f.write(line)
        writer = csv.writer(f)
        writeList = [name.get(), bookingDate, partyName.get(), bookingPeriod, agreedFinalPrice.get(), bookingAmount.get(), date_entry_when_booked.get()]
        writer.writerow(writeList)
        f.close()

    messagebox.showinfo("Success!", "{} booking updated!".format(partyName.get()))
    booking_amount_entry_var.set("")
    event_date_entry_var.set("")
    booked_period_entry_var.set("")
    booking_date_entry_var.set("")
    final_price_entry_var.set("")
    moveToUser()


def login():
    successfullogin = 0
    for widget in userFrame.winfo_children():
        widget.destroy()

    with open("users.txt", 'r') as userFile:
        reader = csv.reader(userFile)
        for row in reader:
            # removes empty list from loop
            if len(row) > 0:
                if username.get() == row[1] and password.get() == row[2]:
                    successfullogin = 1
                    name.set(row[0])
                    moveToUser()

    if successfullogin == 0:
        messagebox.showinfo("Error", "Incorrect credentials. Please re-login or register")


def logOut():
    # Clear Entry boxes
    name.set("")
    username.set("")
    password.set("")
    raiseFrame(start)


def highlight_dates(bookedDates, cal):
    for date in bookedDates:
        cal.tag_config(date, background='red')


def readAppointmentsAllData():
    availableAppts = []
    with open('appointments.txt', 'r') as f:
        for line in f:
            if len(line) > 4:
                availableAppts.append(line.strip())
    return availableAppts


def readAppointmentsForPartyName():
    availableAppts = []
    with open('appointments.txt', 'r') as f:
        for line in f:
            if len(line) > 4:
                availableAppts.append(line.strip().split(',')[2])
    return availableAppts


def readAppointmentsForBookingPeriod():
    availableAppts = []
    with open('appointments.txt', 'r') as f:
        for line in f:
            if len(line) > 4:
                bookingdateFetched = line.strip().split(',')[1]
                bookingperiodFetched = line.strip().split(',')[3]
                availableAppts.append(bookingdateFetched + "|" + bookingperiodFetched)
    return availableAppts


def validate(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if action == '1' and text in '0123456789':
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    elif action == '0':
        return True
    else:
        return False


# Call setup
setup()
# Define Frame
start = tk.Frame(root)
regFrame = tk.Frame(root)
userFrame = tk.Frame(root)
bookAppointmentFrame = tk.Frame(root)
cancelAppointmentFrameByPartyName = tk.Frame(root)
cancelAppointmentFrameByDate = tk.Frame(root)
updateAppointmentFrame = tk.Frame(root)
printAppointmentFrame = tk.Frame(root)

# Start Global Variable holders for Update operation
update_optionmenu_var = tk.StringVar(updateAppointmentFrame)

booking_amount_entry_var = tk.StringVar()
booking_amount_entry_var.set("")

final_price_entry_var = tk.StringVar()
final_price_entry_var.set("")

event_date_entry_var = tk.StringVar()
event_date_entry_var.set("")

booked_period_entry_var = tk.StringVar()
booked_period_entry_var.set("")

booking_date_entry_var = tk.StringVar()
booking_date_entry_var.set("")
# End

updatePartyNameArray = []
updateEventDateArray = []
updateBookingPeriodArray = []
updatePaymentDoneArray = []
updateBookingDateArray = []
updateFinalFullPriceArray = []

frameList = [start, regFrame, userFrame, bookAppointmentFrame, cancelAppointmentFrameByPartyName, cancelAppointmentFrameByDate, updateAppointmentFrame, printAppointmentFrame]
# Configure all (main) Frames
for frame in frameList:
    frame.grid(row=0, column=0, sticky='news')
    frame.configure(bg='lightblue')

# Define Image
kalashimage = Image.open("KalashLogo.png")
kalashimagePH = ImageTk.PhotoImage(kalashimage)

bookingimage = Image.open("BookingImage.png")
bookingimagePH = ImageTk.PhotoImage(bookingimage)

# Labels
tk.Label(start, text="Kalash Banquet Booking", font=("Courier", 60), bg='lightblue').grid(row=0, column=1, columnspan=5)
tk.Label(start, image=kalashimagePH, bg='lightblue').grid(row=1, column=1, columnspan=5)
tk.Label(start, text="Username: ", padx=20, pady=10, font=("Courier", 18), bg='lightblue').grid(row=2, column=1)
tk.Label(start, text="Password: ", padx=20, pady=10, font=("Courier", 18), bg='lightblue').grid(row=3, column=1)

tk.Label(regFrame, text="Register", font=("Courier", 44), bg='lightblue').grid(row=1, column=1, columnspan=5)
tk.Label(regFrame, text="Name: ", font=("Courier", 18), bg='lightblue').grid(row=2, column=1)
tk.Label(regFrame, text="Username: ", font=("Courier", 18), bg='lightblue').grid(row=3, column=1)
tk.Label(regFrame, text="Password: ", font=("Courier", 18), bg='lightblue').grid(row=4, column=1)

# Entry Boxes
tk.Entry(start, textvariable=username, font=("Courier", 18), bg='lightblue').grid(row=2, column=2)
tk.Entry(start, textvariable=password, font=("Courier", 18), bg='lightblue', show="*").grid(row=3, column=2)

tk.Entry(regFrame, textvariable=name, font=("Courier", 18), bg='lightblue').grid(row=2, column=2)
tk.Entry(regFrame, textvariable=username, font=("Courier", 18), bg='lightblue').grid(row=3, column=2)
tk.Entry(regFrame, textvariable=password, font=("Courier", 18), bg='lightblue', show="*").grid(row=4, column=2)
# Buttons
tk.Button(start, font=("Courier", 18), padx=20, pady=10, bg='cyan', text="Login", command=login).grid(row=4, column=2)
tk.Button(start, font=("Courier", 18), padx=20, pady=10, bg='cyan', text="Register", command=moveToReg).grid(row=4,
                                                                                                             column=1)
tk.Button(regFrame, font=("Courier", 18), bg='cyan', text="Register", command=register).grid(row=5, column=2)
tk.Button(regFrame, font=("Courier", 18), bg='cyan', text="Back", command=moveToLogin).grid(row=5, column=1)

# Raise Initial Frame
raiseFrame(start)
root.mainloop()
