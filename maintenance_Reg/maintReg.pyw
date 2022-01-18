import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from datetime import date

root = tk.Tk()
root.geometry("600x600")
root.title('ENGENHARIA ASSIST - vBeta')

def submitForm():
    MsgBox = tk.messagebox.askquestion ('Submit Report','Tem certeza que deseja enviar o relatório?',icon = 'warning')
    if MsgBox == 'yes':
       writeFile()
       root.destroy()
    else:
        tk.messagebox.showinfo('Return','Retornando para a página principal')

def writeFile():
    stringToWrite = techList.get() + ";" + lineList.get() + ";" + entry_2.get() + ";" + entry_4.get() + ";"+ entry_5.get() + ";" + str(var2.get()) +";"+entry_6.get("1.0",'end-1c')
    today = date.today()
    filename = today.strftime("%b-%d-%Y")+'.csv'
    file = open(filename,'a+')
    file.write(stringToWrite + '\n')
    file.close()

listOfTech=[ 'Tech 1','Tech 2', 'Tech 3']
listOfLine=["Line1","Line2","Line3","LineZ"]

label_0 =Label(root,text="Manutenção Corretiva", width=30,font=("bold",20))
label_0.place(x=20,y=60)

label_1 =Label(root,text="Técnico:", width=20,font=("bold",10), justify=LEFT)
label_1.place(x=80,y=130)
label_3 =Label(root,text="linha:", width=20,font=("bold",10))
label_3.place(x=80,y=180)
label_2 =Label(root,text="Máquina:", width=20,font=("bold",10))
label_2.place(x=80,y=230)
label_4 =Label(root,text="Data [DD/MM/AAAA]:", width=15,font=("bold",10))
label_4.place(x=80,y=280)
label_5 =Label(root,text="Duração [00h00]:", width=15,font=("bold",10), justify=RIGHT)
label_5.place(x=80,y=330)
label_6 =Label(root,text="Resolvido:", width=10,font=("bold",10), justify=RIGHT)
label_6.place(x=80,y=380)
label_5 =Label(root,text="Descrição do problema + resolução:", width=60,font=("bold",10))
label_5.place(x=20,y=430)

techList = ttk.Combobox(root,values= listOfTech)
techList.config(width=20)
techList.place(x=240,y=130)

entry_2=Entry(root)
entry_2.place(x=240,y=230)

lineList=ttk.Combobox(root,values= listOfLine)
lineList.config(width=20)
lineList.place(x=240,y=180)

entry_4=Entry(root)
entry_4.place(x=240,y=280)
entry_5=Entry(root)
entry_5.place(x=240,y=330)
var2=IntVar()
Checkbutton(root,text="OK", variable=var2).place(x=290,y=380)
entry_6=Text(root, height=3, width=50)
entry_6.place(x=80,y=460)

Button(root, text='Enviar', command = submitForm, width=20,bg="black",fg='white').place(x=200,y=560)


root.mainloop()