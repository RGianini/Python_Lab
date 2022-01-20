import datetime
import os
from tkinter import Tk, ttk, Frame, Button, Label, Entry, Text, Checkbutton, \
    Scale, Listbox, Menu, BOTH, RIGHT, RAISED, N, E, S, W, \
    HORIZONTAL, END, FALSE, IntVar, StringVar, messagebox as box
from tkinter import PhotoImage
filePath = '/Users/RODOLPHO.MELLO/Documents/Programming/python_/PCBAnalysis/'

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("Controle de Rejeitos")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.centreWindow()
        self.pack(fill=BOTH, expand=1)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        gif1 = PhotoImage(file = 'logo.gif')
        label1 = Label(self, image=gif1, background="white")
        label1.image = gif1
        label1.grid(row = 0, column = 2, columnspan = 1, sticky=N+E)

        lineLabel = Label(self, text="Linha:", background="white")
        lineLabel.grid(row=0, column=0, sticky=W+E)
        pnLabel = Label(self, text="Cód Produto:",background="white")
        pnLabel.grid(row=1, column=0, sticky=W+E)
        defectLabel = Label(self, text="Defeito:",background="white")
        defectLabel.grid(row=2, column=0, sticky=W+E)
        quantityLabel = Label(self, text="Qty:",background="white")
        quantityLabel.grid(row=3, column=0, sticky=W+E)		
        countryLabel = Label(self, text="Espec Defeito:",background="white")
        countryLabel.grid(row=4, column=0, sticky=W+E)
        ncLabel = Label(self, text="Núm. NC:",background="white")
        ncLabel.grid(row=5, column=0, sticky=W+E)
        dataInLabel = Label(self, text="Data Fail <DD/MM/AA>:",background="white")
        dataInLabel.grid(row=6, column=0, sticky=W+E)
        checkTypeLabel = Label(self, text="Destino:",background="white")
        checkTypeLabel.grid(row=10, column=0, sticky=W+E)

        self.fullTimeVar = IntVar()
        fullTimeCheck = Checkbutton(self, text="Reparo", variable=self.fullTimeVar,background="white")
        fullTimeCheck.grid(row=10, column=1, columnspan=2, sticky=W)
        #fullTimeCheck.select()
        self.fullTimeVar2 = IntVar()
        fullTimeCheck2 = Checkbutton(self, text="Scrap", variable=self.fullTimeVar2,background="white")
        fullTimeCheck2.grid(row=11, column=1, columnspan=2, sticky=W)

        self.lineVar = StringVar()
        self.lineCombo = ttk.Combobox(self, textvariable=self.lineVar)
        self.lineCombo['values'] = ('U1','U2','U3','U4','PGD','SMT')
        self.lineCombo.current(1)
        self.lineCombo.bind("<<ComboboxSelected>>", self.newCountry)
        self.lineCombo.grid(row=0, column=1, padx=5, pady=5, ipady=2, sticky=W)

        self.pnVar = StringVar()
        pnText = Entry(self, width=20, textvariable=self.pnVar)
        pnText.grid(row=1, column=1, padx=5, pady=5, ipady=2, sticky=W+E)

        self.regNC = StringVar()
        digNC = Entry(self, width=20, textvariable=self.regNC)
        digNC.grid(row=5, column=1, padx=5, pady=5, ipady=2, sticky=W+E)

        self.dataIn = StringVar()
        dataFIn = Entry(self, width=10, textvariable=self.dataIn)
        dataFIn.grid(row=6, column=1, padx=5, pady=5, ipady=2, sticky=W+E)
		
        self.salaryVar = StringVar()
        salaryScale = Scale(self, from_=0, to=10, orient=HORIZONTAL, resolution=1, background="white",command=self.onSalaryScale)
        salaryScale.grid(row=3, column=1, columnspan=1, sticky=W+E)

        self.failureVar = StringVar()
        self.failureCombo = ttk.Combobox(self, textvariable=self.failureVar)
        self.failureCombo['values'] = ('PTH: Falta Comp.', 'PTH: Mont. Errada', 'PTH: Curto Solda', 'PTH: Falta Solda', 'PTH: Placa Quebr.', 'PTH: Delaminação', 'PTH: Pad Danif.', 'PTH: NFF', 'SMT: Falta Comp.', 'SMT: Comp. Errado', 'SMT: Mal Posic.', 'SMT: Comp. Danif.', 'SMT: Falha Comp.', 'SMT: NFF')
        self.failureCombo.current(1)
        self.failureCombo.bind("<<ComboboxSelected>>", self.newCountry)
        self.failureCombo.grid(row=2, column=1, padx=5, pady=5, ipady=2, sticky=W)

        self.Text = StringVar()
        addressText = Entry(self,width=40,textvariable=self.Text)
        addressText.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        okBtn = Button(self, text="Salvar", width=10, command=self.onConfirm)
        okBtn.grid(row=13, column=0, padx=5, pady=3, sticky=S+E)
        closeBtn = Button(self, text="Close", width=10, command=self.onExit)
        closeBtn.grid(row=13, column=1, padx=5, pady=3, sticky=S+E) 		
        expBtn = Button(self, text="Abrir", width=10, command=self.onOpen)
        expBtn.grid(row=15, column=0, padx=5, pady=3, sticky=S+E)		
		

    def centreWindow(self):
        w = 530
        h = 375
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def onExit(self):
        self.quit()

    def onOpen(self):
        os.system('start C:\\Users/RODOLPHO.MELLO/Documents/Programming/python_/PCBAnalysis/')

		
    def newCountry(self, event):
        self.failureVar.get()

    def onSalaryScale(self, val):
        self.salaryVar.set(str(val))

	
    def onConfirm(self):
        flagPN = True
        flagNC = True
        flagExist = True
        typeForward = str()
        hourInfo = str()
        folderName = str()
        now = str(datetime.datetime.now())
        hourInfo = now[:19]
        folderName = now[:10]
        dirFile = filePath + folderName + '/'

        flagExist = os.path.exists(dirFile)
        print(flagExist)
        if flagExist == False:
           os.makedirs(dirFile)
           updtFil0 = open(dirFile+'logFile.csv', 'w')
           updtFil0.write('Linha'+';'+'Cod Produto'+';'+'Reg NC'+';'+'Defeito'+';'+'Quantidade'+';'+'Descricao Defeito'+';'+'Encaminhamento'+';'+'Hora Analise'+';'+'Data Falha'+'\n')
           updtFil0.close()

        if self.fullTimeVar.get() == 1:
           typeForward = "Reparo"
        elif self.fullTimeVar2.get() == 1:
           typeForward = "Scrap"
        if len(self.pnVar.get())!=10:
           flagPN = False
        if flagPN == True:
           if len(self.regNC.get())!=7:
               flagNC = False
           if flagNC ==True:
               updtFil = open(dirFile+'logFile.csv', 'a')
               updtFil.write(self.lineVar.get()+';'+self.pnVar.get()+';'+self.regNC.get()+';'+self.failureVar.get()+';'+self.salaryVar.get()+';'+self.Text.get()+';'+typeForward+';'+hourInfo+';'+self.dataIn.get() +'\n')
               updtFil.close()
               box.showinfo("Information", "Informações Gravadas!")
           else:
               box.showinfo("Information", "Registro NC incorreto <7 digitos>!")
        else:
           box.showinfo("Information", "PN Incorreto!")





def main():
    root = Tk()
    #root.geometry("250x150+300+300")    # width x height + x + y
    # we will use centreWindow instead
    root.resizable(width=FALSE, height=FALSE)
    # .. not resizable
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()