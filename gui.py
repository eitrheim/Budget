import tkinter as tk
from tkinter import ttk
import datetime


##############################################################################
# show balances
##############################################################################
class ShowBalances:

    def __init__(self, master, df):
        self.master = master
        master.title("Budgeting")
        self.title = tk.Label(master, text='Account Balances', font='helvetica 16 bold')

        self.tree = ttk.Treeview(master, height=15)

        self.tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
        self.tree.column("#0", width=100, minwidth=100, stretch=tk.NO, anchor='center')
        self.tree.column("one", width=250, minwidth=150, anchor='center')
        self.tree.column("two", width=80, minwidth=80, stretch=tk.NO, anchor='center')
        self.tree.column("three", width=80, minwidth=50, stretch=tk.NO, anchor='center')
        self.tree.column("four", width=80, minwidth=50, stretch=tk.NO, anchor='center')
        self.tree.column("five", width=80, minwidth=50, stretch=tk.NO, anchor='center')
        self.tree.column("six", width=80, minwidth=50, stretch=tk.NO, anchor='center')
        self.tree.column("seven", width=80, minwidth=50, stretch=tk.NO, anchor='center')

        self.tree.heading("#0", text="Date", anchor='center')
        self.tree.heading("one", text="Transaction", anchor='center')
        self.tree.heading("two", text="WF Amt", anchor='center')
        self.tree.heading("three", text="Citi Amt", anchor='center')
        self.tree.heading("four", text="Uber Amt", anchor='center')
        self.tree.heading("five", text="WF", anchor='center')
        self.tree.heading("six", text="Citi", anchor='center')
        self.tree.heading("seven", text="Uber", anchor='center')

        ##############################################################################
        # filling in the table
        ##############################################################################
        for i in range(len(df)):
            if df.Date.value_counts()[df.Date[i]] == 1:  # when there is <= one transaction for a day
                if df.loc[i, 'Transaction'] == '':  # if there are no transactions for a day
                    self.tree.insert('', 'end', text=df.loc[i, 'Date'],
                                     values=[df.loc[i, 'Transaction'],
                                             df.loc[i, 'WF Amount'].astype(str).replace('0.0',''),
                                             df.loc[i, 'Citi Amount'].astype(str).replace('0.0',''),
                                             df.loc[i, 'Uber Amount'].astype(str).replace('0.0',''),
                                             df.loc[i, 'WF'], df.loc[i, 'Citi'], df.loc[i, 'Uber']])
                else:  # if there is a transaction we add a tag
                    self.tree.insert('', 'end', text=df.loc[i, 'Date'], tags=('transaction',),
                                     values=[df.loc[i, 'Transaction'],
                                             df.loc[i, 'WF Amount'].astype(str).replace('0.0',''),
                                             df.loc[i, 'Citi Amount'].astype(str).replace('0.0',''),
                                             df.loc[i, 'Uber Amount'].astype(str).replace('0.0',''),
                                             df.loc[i, 'WF'], df.loc[i, 'Citi'], df.loc[i, 'Uber']])
            elif df.Date[i] != df.Date[i-1]:  # if this is the first transaction listed when there are multiple in a day
                x = len(df[df.Date == df.Date[i]].index.values) - 1
                # creating the folder to store the multiple transactions
                globals()['folder' + str(i)] = self.tree.insert('', 'end', text=df.loc[i, 'Date'],
                                                                tags=('folder',), open=False,
                                                                values=[' Multiple',
                                                                round(df.loc[i:i+x, 'WF Amount'].sum(), 2),
                                                                round(df.loc[i:i+x, 'Citi Amount'].sum(), 2),
                                                                round(df.loc[i:i+x, 'Uber Amount'].sum(), 2),
                                                                df.loc[i+x, 'WF'],
                                                                df.loc[i+x, 'Citi'],
                                                                df.loc[i+x, 'Uber']])
                # putting first transaction in the folder
                self.tree.insert(globals()['folder' + str(i)], 'end', text='', tags=('foldercontents',),
                                 values=[df.loc[i, 'Transaction'], df.loc[i, 'WF Amount'].astype(str).replace('0.0',''),
                                         df.loc[i, 'Citi Amount'], df.loc[i, 'Uber Amount'],
                                         df.loc[i, 'WF'], df.loc[i, 'Citi'], df.loc[i, 'Uber']])
            else:  # putting next transactions in the folder
                x = df[df.Date == df.Date[i]].index.values[0]
                self.tree.insert(globals()['folder' + str(x)], 'end', text='', tags=('foldercontents',),
                                 values=[df.loc[i, 'Transaction'], df.loc[i, 'WF Amount'].astype(str).replace('0.0',''),
                                         df.loc[i, 'Citi Amount'], df.loc[i, 'Uber Amount'],
                                         df.loc[i, 'WF'], df.loc[i, 'Citi'], df.loc[i, 'Uber']])

        ##############################################################################
        # colors and styling of table
        ##############################################################################
        ttk.Style().configure("Treeview", background="gray95",  # color of cells not clicked on
                              foreground="black")  # color of font when clicked on
        ttk.Style().configure("Treeview.Heading", font=('Helvetica bold', 14))  # (None, 12) to just change size
        self.tree.tag_configure('transaction', background='gray87')
        self.tree.tag_configure('folder', background='gray75')
        self.tree.tag_configure('foldercontents', background='gray87')

        self.tree.pack(side=tk.TOP, fill=tk.X, padx=0)  # TODO somehow make it so it grows vertically, and what is fill
        tk.Label(master, text='', font='helvetica 2').pack()
        self.okay_button = tk.Button(master, text='Okay', command=master.destroy)
        self.okay_button.pack(ipadx=20)
        tk.Label(master, text='', font='helvetica 2').pack()


##############################################################################
# update account balances
##############################################################################
class EnterBalances:
    balances = {}

    def __init__(self, master, df):
        self.master = master
        master.title("Budgeting")
        self.title = tk.Label(master, text='Enter Account Balances', font='helvetica 16 bold')
        self.title.grid(row=0, columnspan=5, sticky='ew')

        tk.Label(master, text="").grid(row=1, column=0, padx=10)
        tk.Label(master, text="Wells Fargo").grid(row=1, column=1, padx=10)
        tk.Label(master, text="Citi").grid(row=1, column=2, padx=10)
        tk.Label(master, text="Uber").grid(row=1, column=3, padx=10)
        tk.Label(master, text="").grid(row=1, column=4, padx=10)

        current_date = int(df[df.Date == str(datetime.date.today())].index.values[-1])

        self.wf_entry = tk.Entry(master, justify='center')
        self.wf_entry.grid(row=2, column=1)
        self.wf_entry.insert(tk.END, df.loc[current_date, "WF"])
        self.citi_entry = tk.Entry(master, justify='center')
        self.citi_entry.grid(row=2, column=2)
        self.citi_entry.insert(tk.END, df.loc[current_date, "Citi"])
        self.uber_entry = tk.Entry(master, justify='center')
        self.uber_entry.grid(row=2, column=3)
        self.uber_entry.insert(tk.END, df.loc[current_date, "Uber"])

        tk.Label(master, text="").grid(row=3, columnspan=3)
        self.continue_button = tk.Button(master, text='Continue', command=self.save_and_continue)
        self.continue_button.grid(row=4, column=2, sticky='ew')
        tk.Label(master, text="").grid(row=5, columnspan=3)

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
        self.title = tk.Label(master, text='Enter Transactions', font='helvetica 16 bold')
        self.title.grid(row=0, columnspan=8, sticky='ew', pady=10)

        tk.Label(master, text="").grid(row=1, column=0, padx=10)
        tk.Label(master, text="Date").grid(row=1, column=1, padx=10)
        tk.Label(master, text="Transaction").grid(row=1, column=2, padx=10)
        tk.Label(master, text="Amount").grid(row=1, column=3, padx=10)
        tk.Label(master, text="Wells Fargo").grid(row=1, column=4, padx=10)
        tk.Label(master, text="Citi").grid(row=1, column=5, padx=10)
        tk.Label(master, text="Uber").grid(row=1, column=6, padx=10)
        tk.Label(master, text="").grid(row=1, column=7, padx=10)

        self.date_entry1 = tk.Entry(master, width=12, justify='center')
        self.date_entry1.grid(row=2, column=1)
        self.date_entry1.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.transaction_entry1 = tk.Entry(master, justify='center')
        self.transaction_entry1.grid(row=2, column=2)
        self.amount_entry1 = tk.Entry(master, width=12, justify='center')
        self.amount_entry1.grid(row=2, column=3)
        self.v_wf1 = tk.IntVar()
        self.v_citi1 = tk.IntVar()
        self.v_uber1 = tk.IntVar()
        self.wf_box1 = tk.Checkbutton(master, variable=self.v_wf1)
        self.wf_box1.grid(row=2, column=4)
        self.citi_box1 = tk.Checkbutton(master, variable=self.v_citi1)
        self.citi_box1.grid(row=2, column=5)
        self.uber_box1 = tk.Checkbutton(master, variable=self.v_uber1)
        self.uber_box1.grid(row=2, column=6)

        self.date_entry2 = tk.Entry(master, width=12, justify='center')
        self.date_entry2.grid(row=3, column=1)
        self.date_entry2.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.transaction_entry2 = tk.Entry(master, justify='center')
        self.transaction_entry2.grid(row=3, column=2)
        self.amount_entry2 = tk.Entry(master, width=12, justify='center')
        self.amount_entry2.grid(row=3, column=3)
        self.v_wf2 = tk.IntVar()
        self.v_citi2 = tk.IntVar()
        self.v_uber2 = tk.IntVar()
        self.wf_box2 = tk.Checkbutton(master, variable=self.v_wf2)
        self.wf_box2.grid(row=3, column=4)
        self.citi_box2 = tk.Checkbutton(master, variable=self.v_citi2)
        self.citi_box2.grid(row=3, column=5)
        self.uber_box2 = tk.Checkbutton(master, variable=self.v_uber2)
        self.uber_box2.grid(row=3, column=6)

        self.date_entry3 = tk.Entry(master, width=12, justify='center')
        self.date_entry3.grid(row=4, column=1)
        self.date_entry3.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.transaction_entry3 = tk.Entry(master, justify='center')
        self.transaction_entry3.grid(row=4, column=2)
        self.amount_entry3 = tk.Entry(master, width=12, justify='center')
        self.amount_entry3.grid(row=4, column=3)
        self.v_wf3 = tk.IntVar()
        self.v_citi3 = tk.IntVar()
        self.v_uber3 = tk.IntVar()
        self.wf_box3 = tk.Checkbutton(master, variable=self.v_wf3)
        self.wf_box3.grid(row=4, column=4)
        self.citi_box3 = tk.Checkbutton(master, variable=self.v_citi3)
        self.citi_box3.grid(row=4, column=5)
        self.uber_box3 = tk.Checkbutton(master, variable=self.v_uber3)
        self.uber_box3.grid(row=4, column=6)

        tk.Label(master, text="").grid(row=5)
        self.continue_button = tk.Button(master, text='Continue', command=self.save_and_continue)
        self.continue_button.grid(row=6, column=3)
        tk.Label(master, text="").grid(row=6)

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
        tk.Label(master, text='Select card to pay off:', font='helvetica 16 bold').grid(row=0, column=0, columnspan=2)
        tk.Label(master, text="").grid(row=1)

        self.v_citi = tk.IntVar()
        self.v_uber = tk.IntVar()

        self.citi_box = tk.Checkbutton(master, text='Citi', variable=self.v_citi)
        self.citi_box.grid(column=0, row=2)
        self.citi_date = tk.Entry(master, width=12, justify='center')
        self.citi_date.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.citi_date.grid(column=1, row=2)
        self.uber_box = tk.Checkbutton(master, text='Uber', variable=self.v_uber)
        self.uber_box.grid(column=0, row=3)
        self.uber_date = tk.Entry(master, width=12, justify='center')
        self.uber_date.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.uber_date.grid(column=1, row=3)

        tk.Label(master, text="").grid(row=4)
        tk.Button(master, text='Continue', command=self.save_and_continue).grid(column=0, row=5, columnspan=2)
        tk.Label(master, text="").grid(row=6)

    def save_and_continue(self):
        self.transactions['citi'] = self.v_citi.get()
        self.transactions['uber'] = self.v_uber.get()
        self.transactions['citi date'] = self.citi_date.get()
        self.transactions['uber date'] = self.uber_date.get()
        self.master.destroy()
