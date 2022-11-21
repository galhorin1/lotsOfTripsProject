from pagemanager import *

if __name__ == '__main__':
    app = MainFrame()
    app.title("Lots Of Trips Client")
    app.geometry('700x500')
    app.eval('tk::PlaceWindow . center')
    app.mainloop()

