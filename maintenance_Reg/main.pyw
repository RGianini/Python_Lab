import sys
import tkinter as tk
import datetime
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from datetime import date
from os.path import exists
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import subprocess


root = tk.Tk()
root.title('CBR - ENGINEERING ASSIST - vBeta')
root.geometry("600x680")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Maintenance App')
tabControl.add(tab2, text='KPI Report')
tabControl.pack(expand=1, fill="both")

listOfTech = ['', 'Tech1.', 'Tech2.', 'Tech3.']
listOfLine = ["", "PTHLINHA1", "PTHLINHA2", "PTHLINHA3", "PTHLINHA4", "SMRTBR01", "LINHAPGD", "LINHAVALV"]
list_of_errors = ['Invalid Date Entry (dd/mm/yyyy)!',
                  'Invalid duration entry (00h00)!',
                  'Resolution must be at least 20 characters!!']

filename = "Maintenance-Report.tsv"
file_max_size = 200  # file maximum size is 200kB

plot_type = ['MACHINE', 'LINE']


# Functions  ------------------------------------------------------------
def check_entries():
    date_maintenance = entry_4.get()
    duration_maintenance = entry_5.get()
    resolution_maintenance = entry_6.get("1.0", 'end-1c')

    date_ok = bool(re.match('[0-9][0-9]+/[0-9][0-9]+/[0-9][0-9][0-9][0-9]', date_maintenance))
    duration_ok = bool(re.match('[0-9][0-9]+h+[0-9][0-9]', duration_maintenance))
    resolution_ok = len(resolution_maintenance) > 20

    return [date_ok, duration_ok, resolution_ok]


def submit_form():
    cnt_entry_fail = 0
    err_vec = check_entries()
    err_msg = ""

    for aux in range(len(err_vec)):
        if not err_vec[aux]:
            tk.messagebox.showinfo('Return', list_of_errors[aux])
            cnt_entry_fail += 1

    if cnt_entry_fail == 0:
        msg_box = tk.messagebox.askquestion('Submit Report', 'Are you sure?', icon='warning')
        if msg_box == 'yes':
            write_file()
            techList.current(0)
            lineList.current(0)
            entry_2.delete(0, 'end')
            entry_5.delete(0, 'end')
            entry_4.delete(0, 'end')
            entry_6.delete('1.0', END)
            # root.destroy()
        else:
            tk.messagebox.showinfo('Return', 'Returning to the Main Page')


def write_file():
    string_to_write = ""
    today = date.today().strftime("%d-%b-%Y")

    duration_min = str(int(entry_5.get().split(sep='h')[0]) * 60 + int(entry_5.get().split(sep='h')[1]))

    flag_file_exists = file_exists(filename)
    flag_file_overflow = check_file_size(filename, flag_file_exists)

    if flag_file_overflow:
        new_name = filename[0:-4] + '_' + today + '.tsv'
        os.rename(filename, new_name)
        flag_file_exists = False

    if not flag_file_exists:
        string_to_write = "DATE\tTECHNICIAN\tLINE\tMACHINE\tDURATION(min)\tSOLVED\tRESOLUTION\tDATE REG\n"

    string_to_write = string_to_write + entry_4.get() + '\t' + techList.get() + '\t' + lineList.get() + '\t' + \
                      entry_2.get() + '\t' + duration_min + '\t' + str(var2.get()) + '\t' + \
                      entry_6.get("1.0", 'end-1c') + '\t' + today
    file = open(filename, 'a+')
    file.write(string_to_write + '\n')
    file.close()


def file_exists(file):
    return exists(file)


def check_file_size(file, flag_exists):
    if flag_exists:
        return (os.path.getsize(file) / 1024) > file_max_size
    else:
        return False


def get_data_interval():
    year_aux = int(year_list.get())
    month_aux = int(month_list.get())
    day_aux = int(day_list.get())

    return datetime.date(year=year_aux, month=month_aux, day=day_aux)


def plot_dwt_mach():
    err_msg = ""

    dwt_type = plot_type[int(var_dwt_type.get())]
    if not file_exists(filename):
        tk.messagebox.showinfo('Return', 'File \'Maintenance-Report.tsv\' not found!')
    else:

        first_date = get_data_interval()

        if first_date >= datetime.date.today():
            err_msg = "Chosen date is in the future!! Choose it again Carefully"
            sys.exit("Data invalida!")

        print(first_date >= datetime.date.today())
        maintenance_data = pd.read_csv(filename, sep="\t", parse_dates=True, encoding='latin-1')
        maintenance_data['DATE'] = pd.to_datetime(maintenance_data['DATE'], format='%d/%m/%Y') ###
        # maintenance_data['DATE'] = pd.to_datetime(maintenance_data['DATE']).dt.strftime('%Y-%d-%m')
        maintenance_data['DATE'] = pd.to_datetime(maintenance_data['DATE']).dt.date
        dwt_filtered = maintenance_data[((maintenance_data['DATE'] >= first_date) &
                                         (maintenance_data['DATE'] <= first_date + datetime.timedelta(days=3))
                                         )]

        dwt_pivot = dwt_filtered.reset_index().pivot_table(index=dwt_type,
                                                           columns='DATE',
                                                           values='DURATION(min)',
                                                           aggfunc='sum')
        dwt_pivot.fillna(0)
        graph_dwt = dwt_pivot.T.plot(kind='bar', ylabel='dwt duration [min]')
        plt.savefig('dwt.png')
        plt.title('DWT per ' + dwt_type)
        plt.show()


def print_pdf():
    if not file_exists('dwt.png'):
        tk.messagebox.showinfo('Return', 'File NOT found!! You have to PLOT the graph first!')
    else:
        today = date.today().strftime("%d-%b-%Y")
        pdf = FPDF()
        pdf.add_page(orientation='L')
        pdf.image('dwt.png', x=None, y=None, w=0, h=0, type='', link='')
        pdf.output('dwt-Report-' + today + '.pdf', 'F')
        os.remove('dwt.png')
        subprocess.Popen('dwt-Report-' + today + '.pdf', shell=True)


# End of Functions ----------------------------------------------------------

# TAB 1 ---------------------------------------------------------
label_0 = Label(tab1, text="Maintenance Report", width=30, font=("bold", 20))
label_0.place(x=20, y=60)

label_1 = Label(tab1, text="Tech:", width=20, font=("bold", 10), justify=LEFT)
label_1.place(x=80, y=130)
label_3 = Label(tab1, text="Line:", width=20, font=("bold", 10))
label_3.place(x=80, y=180)
label_2 = Label(tab1, text="Machine:", width=20, font=("bold", 10))
label_2.place(x=80, y=230)
label_4 = Label(tab1, text="Data [DD/MM/YYYY]:", width=15, font=("bold", 10))
label_4.place(x=80, y=280)
label_5 = Label(tab1, text="Duration [00h00]:", width=15, font=("bold", 10), justify=RIGHT)
label_5.place(x=80, y=330)
label_6 = Label(tab1, text="Solved:", width=10, font=("bold", 10), justify=RIGHT)
label_6.place(x=80, y=380)
label_5 = Label(tab1, text="Problem Description + resolution:", width=60, font=("bold", 10))
label_5.place(x=20, y=430)

techList = ttk.Combobox(tab1, values=listOfTech)
techList.config(width=20)
techList.place(x=240, y=130)

entry_2 = Entry(tab1)
entry_2.place(x=240, y=230)

lineList = ttk.Combobox(tab1, values=listOfLine)
lineList.config(width=20)
lineList.place(x=240, y=180)

entry_4 = Entry(tab1)
entry_4.place(x=240, y=280)
entry_5 = Entry(tab1)
entry_5.place(x=240, y=330)
var2 = IntVar()
Checkbutton(tab1, text="OK", variable=var2).place(x=290, y=380)
entry_6 = Text(tab1, height=3, width=50)
entry_6.place(x=80, y=460)

Button(tab1, text="Submit", command=submit_form, width=20, bg="black", fg='white').place(x=200, y=560)
# End of TAB 1 ---------------------------------------------------------

# TAB 2 ----------------------------------------------------------------
label_day_filter = Label(tab2, text="Day:", width=20, font=("bold", 10), justify=CENTER)
label_day_filter.place(x=30, y=130)
label_month_filter = Label(tab2, text="Month:", width=20, font=("bold", 10), justify=LEFT)
label_month_filter.place(x=30, y=90)
label_year_filter = Label(tab2, text="Year:", width=20, font=("bold", 10), justify=LEFT)
label_year_filter.place(x=30, y=50)

day_list = ttk.Combobox(tab2, values=list(range(1, 32)))
day_list.config(width=10)
day_list.place(x=180, y=130)
month_list = ttk.Combobox(tab2, values=list(range(1, 13)))
month_list.config(width=10)
month_list.place(x=180, y=90)
year_list = ttk.Combobox(tab2, values=list(range(2022, 2024)))
year_list.config(width=10)
year_list.place(x=180, y=50)

Button(tab2, text="plot DWT", command=plot_dwt_mach, width=20, bg="black", fg='white').place(x=300, y=140)
Button(tab2, text="Generate PDF", command=print_pdf, width=20, bg="black", fg='white').place(x=300, y=180)

var_dwt_type = IntVar()
R1 = Radiobutton(tab2, text="DWT per Machine", variable=var_dwt_type, value=0).place(x=300, y=60)
R2 = Radiobutton(tab2, text="DWT per Line", variable=var_dwt_type, value=1).place(x=300, y=80)

# End of TAB2 -----------------------------------------------------------


root.mainloop()
