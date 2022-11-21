from welcomepage import *
from afterlogin import *
import servermanager


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.srv = servermanager
        container = tk.Frame()
        container.pack()

        self.id = tk.StringVar()
        self.id.set("hello")
        self.listing = {}

        for p in (WelcomePage, AfterLogin):
            page_name = p.__name__
            frame = p(parent=container, controller=self)
            self.listing[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.up_frame('WelcomePage')

    def up_frame(self, page_name):
        print("up-frame being called")
        frame = self.listing[page_name]
        frame.tkraise()
        frame.update()
