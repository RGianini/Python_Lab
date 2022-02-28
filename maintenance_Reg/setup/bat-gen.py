
myBat = open(r'../Maint-Support.bat','w+')
myBat.write('start "" main.pyw exitpython main.pyw')
myBat.close()