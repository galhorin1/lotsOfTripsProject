import tkinter as tk
import cardinfo


class AfterLogin(tk.Frame):
    datasheet = cardinfo
    AREAS = ['North', 'Center', 'South']
    AREAS_PRICE = {'North': 25, 'Center': 40, 'South': 30}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        self.scale_entry_value = tk.IntVar()
        self.data = self.datasheet.read_file()
        self.card_info = self.data.split(',')
        self.card_label = tk.Label(self, text="")
        self.card_label.grid(row=0, column=1)
        self.clicked = tk.StringVar()
        self.ride = tk.StringVar()
        self.use_cont = tk.IntVar()
        self.use_cont.set(0)
        self.clicked.set("")
        self.ride.set("")

        errortext = ""
        self.error_msg = tk.Label(self, pady=20, text=errortext)
        self.bye = tk.Button(self, text='Logout', command=lambda: self.controller.up_frame('WelcomePage'))

        self.pay = tk.Button(self, text="Pay for a ride", padx=50, pady=20, command=self.payment)
        self.drop_rides = tk.OptionMenu(self, self.ride, *self.AREAS)
        self.change_con = tk.Button(self, text="Change contract", padx=50, pady=20, command=self.contract_update)
        self.add_wallet = tk.Button(self, text="Add money to wallet", padx=50, pady=20, command=self.add_wallet)
        self.drop_contracts = tk.OptionMenu(self, self.clicked, *self.AREAS, 'None')
        self.wallet = tk.Scale(self, from_=0, to=9999, orient=tk.HORIZONTAL, variable=self.scale_entry_value)
        self.wallet_entry = tk.Entry(self, width=4, borderwidth=5, textvariable=self.scale_entry_value)
        self.pay_with_cont = tk.Checkbutton(self, variable=self.use_cont, text='Pay with contract', offvalue=0, onvalue=1)

        self.pay.grid(row=1, column=0)
        self.drop_rides.grid(row=2, column=0)
        self.pay_with_cont.grid(row=3, column=0)
        self.change_con.grid(row=1, column=1)
        self.drop_contracts.grid(row=2, column=1)
        self.add_wallet.grid(row=1, column=2)
        self.wallet.grid(row=2, column=2)
        self.wallet_entry.grid(row=3, column=2)

        self.error_msg.grid(row=4, column=0, columnspan=3)
        self.bye.grid(row=5, column=1)

    def payment(self):
        ride_to = str(self.ride.get())
        wallet = int(self.card_info[2])
        if self.use_cont.get() == 1:
            if ride_to == self.card_info[1]:
                self.set_error_msg('Ride for free')
                return
            else:
                self.set_error_msg('Contract does not match requested travel area')
                return
        elif ride_to in self.AREAS_PRICE.keys():
            if wallet >= self.AREAS_PRICE[ride_to]:
                wallet = wallet - self.AREAS_PRICE[ride_to]
            else:
                self.no_money()
                return
        self.wallet_upt(wallet)
        self.set_error_msg("Thank you for paying, enjoy your trip")

    def wallet_upt(self, wallet):
        replay = self.controller.srv.server_upt('update', self.card_info[0], self.card_info[1], wallet)
        if replay == 'updated':
            d = str(f"{self.card_info[0]},{self.card_info[1]},{wallet}")
            self.datasheet.write_file(d)
            self.upt_label()
        else:
            self.set_error_msg(replay)

    def add_wallet(self):
        money = self.wallet.get()
        new_wallet = int(money)+int(self.card_info[2])
        self.wallet_upt(new_wallet)
        self.set_error_msg("Your wallet has been updated successfully")

    def no_money(self):
        self.set_error_msg("no enough money in your account please fill your wallet or change contract")

    def upt_label(self):
        self.data = self.datasheet.read_file()
        self.card_info = self.data.split(',')
        label_text = f"card number {self.card_info[0]},contract {self.card_info[1]},wallet {self.card_info[2]}"
        self.card_label.config(text=label_text)
        self.card_label.grid(row=0, column=1)

    def contract_update(self):
        self.data = self.datasheet.read_file()
        self.card_info = self.data.split(',')
        contract = str(self.clicked.get())
        replay = self.controller.srv.server_upt('update', self.card_info[0], contract, self.card_info[2])
        if replay == 'updated':
            d = str(f"{self.card_info[0]},{contract},{self.card_info[2]}")
            self.datasheet.write_file(d)
            self.upt_label()
            self.set_error_msg("Contract updated successfully")
        else:
            self.set_error_msg(replay)

    # refresh card data on screen
    def update(self):
        self.upt_label()
        self.clicked.set("")
        self.ride.set("")
        self.use_cont.set(0)

    def set_error_msg(self, error_text_value):
        self.error_msg.config(text=error_text_value)
        self.error_msg.grid(row=4, column=0, columnspan=3)
        self.error_msg.after(4000, lambda: {self.error_msg.config(text=""),
                                            self.error_msg.grid(row=4, column=0, columnspan=3)})
