import tkinter as tk
from tkinter import ttk
import cardinfo


class WelcomePage(tk.Frame):
    # saved card datasheet
    datasheet = cardinfo

    # init self objects
    def __init__(self, parent, controller, ):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        self.cards_layout = tk.Frame(self, width=500, height=50, pady=15)

        self.cards = ['----']
        self.all_cards = tk.StringVar(self)
        self.all_cards.set(self.cards[0])

        self.data = self.datasheet.read_file()
        self.card_number = self.data.split(',')
        errortext = "The last card number used is "+self.card_number[0]

        # Creating widgets
        self.login_button = tk.Button(self, text="connect", padx=50, pady=20, command=self.connect)
        self.new_card_button = tk.Button(self, text="create new card", padx=50, pady=20, command=self.reg_card)
        self.label = tk.Label(self, pady=20, text="Enter your card number below:")
        self.error = tk.Label(self, pady=20, text=errortext)
        self.loader = tk.Button(self, text="Load all cards", padx=50, pady=20, command=self.load)
        # put the following widgets in a sub-layout
        self.combo_box = ttk.Combobox(self.cards_layout, width=4, height=10, textvariable=self.all_cards)
        self.e = tk.Entry(self.cards_layout, width=4, borderwidth=5, textvariable=self.all_cards)
        # set the combobox inactive due to no data
        self.combo_box.config(state='disabled')

        # adding widget to screen
        self.label.pack()
        self.cards_layout.pack()
        self.e.grid(row=0, column=0)
        self.login_button.pack()
        self.new_card_button.pack()
        self.combo_box.grid(row=0, column=1)
        self.loader.pack()
        self.error.pack()

    def load(self):
        received = self.controller.srv.check_server('load', "")
        if received == "No cards exist":
            self.error.config(text=received)
            self.error.pack()
            return
        self.cards.clear()
        self.cards += received.split(',')
        # combo box should have cards numbers you can now activate to select from
        self.combo_box.config(state='normal')
        self.update_option_menu()

    def update_option_menu(self):
        self.combo_box['values'] = self.cards

    # func for when connect button is clicked
    def connect(self):
        print("connecting to server")
        card = self.e.get()
        # disable input field
        self.e.config(state="disabled")
        # wait 2 sec and then enable input field again
        self.e.after(2000, lambda: self.e.config(state="normal"))
        errortext2 = ""
        try:
            number = int(card)
            if 0 <= number <= 9999:
                print("sending request to the server")
                flag = self.controller.srv.check_server('exist', card)
                print(flag)
                if flag == "yes":
                    d = self.controller.srv.check_server('getinfo', card)
                    print(d)
                    self.datasheet.write_file(d)
                    self.controller.up_frame('AfterLogin')
                else:
                    errortext2 = "card does not exist in the server"
            else:
                errortext2 = "card number does not exist"
        except ValueError:
            errortext2 = "card number is not a valid numeric number"
        self.error.config(text=errortext2)
        self.error.pack()

    # register new card for the client
    def reg_card(self):
        self.error.config(text="new card number being created...")
        # disable input field
        self.e.config(state="disabled")
        new_card = self.controller.srv.check_server("create", "")
        # wait 2 sec and then enable input field again
        self.e.after(2000, lambda: self.e.config(state="normal"))
        self.error.config(text="the new card created is :" + new_card)
        self.error.pack()
        self.all_cards.set(new_card)

    def update(self):
        self.data = self.datasheet.read_file()
        self.card_number = self.data.split(',')
        if self.card_number[0] == "":
            errortext = ""
        else:
            errortext = "The last card number used is " + self.card_number[0]
        self.error.config(text=errortext)
        self.error.pack()
