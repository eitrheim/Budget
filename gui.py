import tkinter
import datetime


##############################################################################
# show balances for 15 days into future
##############################################################################
class ShowBalances:

    def __init__(self, master, df, isapp=True):
        self.master = master
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Account Balances', font=('helvetica 16 bold'))
        self.title.grid(row=0, columnspan=8, sticky='ew')

        self.frame = tkinter.Frame(master, bg='gray95')
        self.frame.grid(row=1, columnspan=8)

        c = 0
        widths = [11, 30, 11, 11, 11, 8, 8, 8]
        for i in df.columns:
            tkinter.Label(self.frame, text=i, font='helvetica 14', width=widths[c]).grid(row=1, column=c, pady=1, padx=1)
            c = c + 1

        ###################################################################
        # adding the results to the results table
        ###################################################################
        start_date = int(df[df.Date == str(datetime.date.today())].index.values)

        r = 2
        for y in range(start_date, start_date + 15):
            tkinter.Label(self.frame, background='white', width=11, text=df['Date'].iloc[y]).grid(row=r, column=0, pady=1, padx=1)
            r = r + 1

        r = 3
        for y in range(start_date + 1, start_date + 15):
            tkinter.Label(self.frame, background='white', width=30, text=df['Transaction'].iloc[y]).grid(row=r, column=1, pady=1, padx=1)
            r = r + 1


        c = 2
        for x in ['WF Amount', 'Citi Amount', 'Uber Amount']:
            r = 3
            for y in range(start_date + 1, start_date + 15):
                if df[x].iloc[y] == 0:
                    tkinter.Label(self.frame, background='white', width=11, text='').grid(row=r, column=c, pady=1, padx=1)
                else:
                    tkinter.Label(self.frame, background='white', width=11, text=df[x].iloc[y]).grid(row=r, column=c, pady=1, padx=1)
                r = r + 1
            c = c + 1

        c = 5
        for x in ['WF']:
            r = 2
            for y in range(start_date, start_date + 15):
                tkinter.Label(self.frame, text=df[x].iloc[y], font = 'helvetica 14 bold',
                              background='white', width=8).grid(row=r, column=c, pady=1, padx=1)
                r = r + 1
            c = c + 1

        c = 6
        for x in ['Citi', 'Uber']:
            r = 2
            for y in range(start_date, start_date + 15):
                tkinter.Label(self.frame, text=df[x].iloc[y], background='white', width=8).grid(row=r, column=c, pady=1, padx=1)
                r = r + 1
            c = c + 1

        run_model_button = tkinter.Button(master, text='Okay', command=master.destroy)
        run_model_button.grid(row=17, columnspan=12, pady=10)


##############################################################################
# update account balances
##############################################################################
class EnterBalances:
    balances = {}

    def __init__(self, master, df):
        self.master = master
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Enter Account Balances', font='helvetica 16 bold')
        self.title.grid(row=0, columnspan=5, sticky='ew')

        tkinter.Label(master, text="").grid(row=1, column=0, padx=10)
        tkinter.Label(master, text="Wells Fargo").grid(row=1, column=1, padx=10)
        tkinter.Label(master, text="Citi").grid(row=1, column=2, padx=10)
        tkinter.Label(master, text="Uber").grid(row=1, column=3, padx=10)
        tkinter.Label(master, text="").grid(row=1, column=4, padx=10)

        current_date = int(df[df.Date == str(datetime.date.today())].index.values)

        self.wf_entry = tkinter.Entry(master, justify='center')
        self.wf_entry.grid(row=2, column=1)
        self.wf_entry.insert(tkinter.END, df.loc[current_date, "WF"])
        self.citi_entry = tkinter.Entry(master, justify='center')
        self.citi_entry.grid(row=2, column=2)
        self.citi_entry.insert(tkinter.END, df.loc[current_date, "Citi"])
        self.uber_entry = tkinter.Entry(master, justify='center')
        self.uber_entry.grid(row=2, column=3)
        self.uber_entry.insert(tkinter.END, df.loc[current_date, "Uber"])

        tkinter.Label(master, text="").grid(row=3, columnspan=3)
        self.continue_button = tkinter.Button(master, text='Continue',
                                              command=self.save_and_continue)
        self.continue_button.grid(row=4, column=2, sticky='ew')
        tkinter.Label(master, text="").grid(row=5, columnspan=3)

    def save_and_continue(self):
        self.balances['wf'] = self.wf_entry.get()
        self.balances['citi'] = self.citi_entry.get()
        self.balances['uber'] = self.uber_entry.get()
        self.master.destroy()
        
        
##############################################################################
# add transactions
##############################################################################
class EnterTransactions:
    transactions = {}

    def __init__(self, master):
        self.master = master
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Enter Transactions', font='helvetica 16 bold')
        self.title.grid(row=0, columnspan=8, sticky='ew', pady=10)

        tkinter.Label(master, text="").grid(row=1, column=0, padx=10)
        tkinter.Label(master, text="Date").grid(row=1, column=1, padx=10)
        tkinter.Label(master, text="Transaction").grid(row=1, column=2, padx=10)
        tkinter.Label(master, text="Amount").grid(row=1, column=3, padx=10)
        tkinter.Label(master, text="Wells Fargo").grid(row=1, column=4, padx=10)
        tkinter.Label(master, text="Citi").grid(row=1, column=5, padx=10)
        tkinter.Label(master, text="Uber").grid(row=1, column=6, padx=10)
        tkinter.Label(master, text="").grid(row=1, column=7, padx=10)

        self.date_entry1 = tkinter.Entry(master, width=12, justify='center')
        self.date_entry1.grid(row=2, column=1)
        self.date_entry1.insert(tkinter.END, datetime.date.today() + datetime.timedelta(days=1))
        self.transaction_entry1 = tkinter.Entry(master, justify='center')
        self.transaction_entry1.grid(row=2, column=2)
        self.amount_entry1 = tkinter.Entry(master, width=12, justify='center')
        self.amount_entry1.grid(row=2, column=3)
        self.v_wf1 = tkinter.IntVar()
        self.v_citi1 = tkinter.IntVar()
        self.v_uber1 = tkinter.IntVar()
        self.wf_box1 = tkinter.Checkbutton(master, variable=self.v_wf1)
        self.wf_box1.grid(row=2, column=4)
        self.citi_box1 = tkinter.Checkbutton(master, variable=self.v_citi1)
        self.citi_box1.grid(row=2, column=5)
        self.uber_box1 = tkinter.Checkbutton(master, variable=self.v_uber1)
        self.uber_box1.grid(row=2, column=6)

        self.date_entry2 = tkinter.Entry(master, width=12, justify='center')
        self.date_entry2.grid(row=3, column=1)
        self.date_entry2.insert(tkinter.END, datetime.date.today() + datetime.timedelta(days=1))
        self.transaction_entry2 = tkinter.Entry(master, justify='center')
        self.transaction_entry2.grid(row=3, column=2)
        self.amount_entry2 = tkinter.Entry(master, width=12, justify='center')
        self.amount_entry2.grid(row=3, column=3)
        self.v_wf2 = tkinter.IntVar()
        self.v_citi2 = tkinter.IntVar()
        self.v_uber2 = tkinter.IntVar()
        self.wf_box2 = tkinter.Checkbutton(master, variable=self.v_wf2)
        self.wf_box2.grid(row=3, column=4)
        self.citi_box2 = tkinter.Checkbutton(master, variable=self.v_citi2)
        self.citi_box2.grid(row=3, column=5)
        self.uber_box2 = tkinter.Checkbutton(master, variable=self.v_uber2)
        self.uber_box2.grid(row=3, column=6)

        self.date_entry3 = tkinter.Entry(master, width=12, justify='center')
        self.date_entry3.grid(row=4, column=1)
        self.date_entry3.insert(tkinter.END, datetime.date.today() + datetime.timedelta(days=1))
        self.transaction_entry3 = tkinter.Entry(master, justify='center')
        self.transaction_entry3.grid(row=4, column=2)
        self.amount_entry3 = tkinter.Entry(master, width=12, justify='center')
        self.amount_entry3.grid(row=4, column=3)
        self.v_wf3 = tkinter.IntVar()
        self.v_citi3 = tkinter.IntVar()
        self.v_uber3 = tkinter.IntVar()
        self.wf_box3 = tkinter.Checkbutton(master, variable=self.v_wf3)
        self.wf_box3.grid(row=4, column=4)
        self.citi_box3 = tkinter.Checkbutton(master, variable=self.v_citi3)
        self.citi_box3.grid(row=4, column=5)
        self.uber_box3 = tkinter.Checkbutton(master, variable=self.v_uber3)
        self.uber_box3.grid(row=4, column=6)

        tkinter.Label(master, text="").grid(row=5)
        self.continue_button = tkinter.Button(master, text='Continue',
                                              command=self.save_and_continue)
        self.continue_button.grid(row=6, column=3)
        tkinter.Label(master, text="").grid(row=6)

    def save_and_continue(self):
        self.transactions['transaction date1'] = self.date_entry1.get()
        self.transactions['transaction entry1'] = self.transaction_entry1.get()
        self.transactions['transaction amount1'] = self.amount_entry1.get()
        self.transactions['wf1'] = self.v_wf1.get()
        self.transactions['citi1'] = self.v_citi1.get()
        self.transactions['uber1'] = self.v_uber1.get()

        self.transactions['transaction date2'] = self.date_entry2.get()
        self.transactions['transaction entry2'] = self.transaction_entry2.get()
        self.transactions['transaction amount2'] = self.amount_entry2.get()
        self.transactions['wf2'] = self.v_wf2.get()
        self.transactions['citi2'] = self.v_citi2.get()
        self.transactions['uber2'] = self.v_uber2.get()

        self.transactions['transaction date3'] = self.date_entry3.get()
        self.transactions['transaction entry3'] = self.transaction_entry3.get()
        self.transactions['transaction amount3'] = self.amount_entry3.get()
        self.transactions['wf3'] = self.v_wf3.get()
        self.transactions['citi3'] = self.v_citi3.get()
        self.transactions['uber3'] = self.v_uber3.get()
        self.master.destroy()


##############################################################################
# pay off uber or citi credit card
##############################################################################
class PayoffCC:
    transactions = {}

    def __init__(self, master):
        self.master = master
        master.title("Budgeting")
        tkinter.Label(master, text='Select card to pay off:',
                      font='helvetica 16 bold').grid(row=0, column=0, columnspan=2)
        tkinter.Label(master, text="").grid(row=1)

        self.v_citi = tkinter.IntVar()
        self.v_uber = tkinter.IntVar()

        self.citi_box = tkinter.Checkbutton(master, text='Citi', variable=self.v_citi)
        self.citi_box.grid(column=0, row=2)
        self.citi_date = tkinter.Entry(master, width=12, justify='center')
        self.citi_date.insert(tkinter.END, datetime.date.today() + datetime.timedelta(days=1))
        self.citi_date.grid(column=1, row=2)
        self.uber_box = tkinter.Checkbutton(master, text='Uber', variable=self.v_uber)
        self.uber_box.grid(column=0, row=3)
        self.uber_date = tkinter.Entry(master, width=12, justify='center')
        self.uber_date.insert(tkinter.END, datetime.date.today() + datetime.timedelta(days=1))
        self.uber_date.grid(column=1, row=3)

        tkinter.Label(master, text="").grid(row=4)
        tkinter.Button(master, text='Continue', command=self.save_and_continue).grid(column=0, row=5, columnspan=2)
        tkinter.Label(master, text="").grid(row=6)

    def save_and_continue(self):
        self.transactions['citi'] = self.v_citi.get()
        self.transactions['uber'] = self.v_uber.get()
        self.transactions['citi date'] = self.citi_date.get()
        self.transactions['uber date'] = self.uber_date.get()
        self.master.destroy()

        #persistent notes at the bottom
        #updating cc payment
        #ability to type in transactions into grid
