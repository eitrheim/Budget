import tkinter as tk
from tkinter import ttk
import datetime


##############################################################################
# show balances
##############################################################################
class ShowBalances:

    def __init__(self, master, df, notes):
        self.master = master
        master.title('Budgeting')
        master.geometry('840x550')
        tk.Label(master, text='Account Balances', font='None 14 bold').pack(pady=1)
        self.tree = ttk.Treeview(master, height=15)
        self.save_notes = {}

        ##############################################################################
        # column headings
        ##############################################################################
        self.tree['columns'] = ('one', 'two', 'three', 'four', 'five', 'six', 'seven')
        self.tree.column('#0', width=100, stretch=tk.NO, anchor='center')
        self.tree.column('one', width=250, minwidth=150, anchor='center')
        self.tree.column('two', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('three', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('four', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('five', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('six', width=80, stretch=tk.NO, anchor='center')
        self.tree.column('seven', width=80, stretch=tk.NO, anchor='center')

        self.tree.heading('#0', text='Date')
        self.tree.heading('one', text='Transaction')
        self.tree.heading('two', text='WF Amt')
        self.tree.heading('three', text='Citi Amt')
        self.tree.heading('four', text='Uber Amt')
        self.tree.heading('five', text='WF')
        self.tree.heading('six', text='Citi')
        self.tree.heading('seven', text='Uber')

        ##############################################################################
        # filling in the table
        ##############################################################################
        df.Transaction = df.Transaction.replace('0', '')
        for i in range(len(df)):
            if df.Date.value_counts()[df.Date[i]] == 1:  # when there's <= 1 transaction a day
                df.loc[i] = df.loc[i].replace(0, '')
                if df.loc[i, 'Transaction'] == '':  # if there are no transactions for a day
                    self.tree.insert('', 'end', text=df.loc[i, 'Date'],
                                     values=[df.loc[i, 'Transaction'], df.loc[i, 'WF Amount'],
                                             df.loc[i, 'Citi Amount'], df.loc[i, 'Uber Amount'],
                                             df.loc[i, 'WF'], df.loc[i, 'Citi'], df.loc[i, 'Uber']])
                else:  # if there is a transaction we add a tag
                    self.tree.insert('', 'end', text=df.loc[i, 'Date'], tags=('transaction',),
                                     values=[df.loc[i, 'Transaction'], df.loc[i, 'WF Amount'],
                                             df.loc[i, 'Citi Amount'], df.loc[i, 'Uber Amount'],
                                             df.loc[i, 'WF'], df.loc[i, 'Citi'], df.loc[i, 'Uber']])
                df.loc[i] = df.loc[i].replace('', 0)
            elif df.Date[i] != df.Date[i-1]:  # if first trans listed when there are multiple a day
                x = len(df[df.Date == df.Date[i]].index.values) - 1
                # creating the folder to store the multiple transactions
                globals()['folder' + str(i)] = self.tree.insert('', 'end', text=df.loc[i, 'Date'],
                                                                tags=('folder',), open=True,
                                                                values=[' Multiple',
                                                                        round(df.loc[i:i+x, 'WF Amount'].sum(), 2),
                                                                        round(df.loc[i:i+x, 'Citi Amount'].sum(), 2),
                                                                        round(df.loc[i:i+x, 'Uber Amount'].sum(), 2),
                                                                        df.loc[i+x, 'WF'],
                                                                        df.loc[i+x, 'Citi'],
                                                                        df.loc[i+x, 'Uber']])
                # putting first transaction in the folder
                df.loc[i] = df.loc[i].replace(0, '')
                self.tree.insert(globals()['folder' + str(i)], 'end',
                                 text='', tags=('foldercontents',),
                                 values=[df.loc[i, 'Transaction'], df.loc[i, 'WF Amount'],
                                         df.loc[i, 'Citi Amount'], df.loc[i, 'Uber Amount'],
                                         '', '', ''])
                df.loc[i] = df.loc[i].replace('', 0)
            else:  # putting next transactions in the folder
                df.loc[i] = df.loc[i].replace(0, '')
                x = df[df.Date == df.Date[i]].index.values[0]
                self.tree.insert(globals()['folder' + str(x)], 'end',
                                 text='', tags=('foldercontents',),
                                 values=[df.loc[i, 'Transaction'], df.loc[i, 'WF Amount'],
                                         df.loc[i, 'Citi Amount'], df.loc[i, 'Uber Amount'],
                                         '', '', ''])
                df.loc[i] = df.loc[i].replace('', 0)
        df.Transaction = df.Transaction.replace('0', '')

        ##############################################################################
        # colors and styling of data table
        ##############################################################################
        color1 = 'lavender'  # background of folder
        color2 = 'gray90'  # background of folder items and transactions
        color3 = 'gray98'  # main background
        color4 = 'black'  # font color

        self.scroll = tk.Scrollbar(self.tree, command=self.tree.yview)
        self.scroll.config()
        ttk.Style().configure('.', borderwidth=0)  # every class to have zero width border, no ridge
        ttk.Style().configure('Treeview', background=color3,  # color of cells not clicked on
                              foreground=color4,   # color of font when clicked on
                              font='helvetica 12')
        self.tree.config(yscrollcommand=self.scroll.set)
        ttk.Style().configure('Treeview.Heading', font='helvetica 12')  # (None, 12) to change size
        self.tree.tag_configure('transaction', background=color2)
        self.tree.tag_configure('folder', background=color1)
        self.tree.tag_configure('foldercontents', background=color2)

        self.scroll.pack(side=tk.RIGHT, anchor='ne', fill=tk.Y)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0)
        tk.Label(master, text='Notes', font='None 14 bold').pack(fill=tk.BOTH, expand=False, pady=1)

        ##############################################################################
        # text box for notes
        ##############################################################################
        self.text_box = tk.Text(master, font='helvetica 12', highlightthickness=0, height=10, bg=color3)
        self.text_box.config(wrap=tk.WORD)
        self.text_box.insert('end', notes, 'area')  # area is the tag name
        # self.text_box.tag_add('area', '1.0', 'end')
        self.text_box.tag_config('area', justify='center', font='helvetica 12')
        self.text_box.tag_config('sel', font='helvetica 12 bold')
        ttk.Style().configure('Text', relief='flat', borderwidth=0)
        self.text_box.pack()
        self.text_box.focus_set()

        ##############################################################################
        # add continue button
        ##############################################################################
        tk.Label(master, text='', font='helvetica 2').pack(expand=False)
        tk.Button(master, text='Continue', font='helvetica 14 bold',
                  command=self.save_and_continue).pack(ipadx=50, ipady=1)
        tk.Label(master, text='', font='helvetica 2').pack(expand=False)

    def save_and_continue(self):
        self.save_notes['saved_notes'] = self.text_box.get('1.0', 'area.last')
        self.master.destroy()


##############################################################################
# update account balances
##############################################################################
class EnterBalances:
    balances = {}

    def __init__(self, master, df):
        self.master = master
        master.title('Budgeting')
        self.title = tk.Label(master, text='Enter Account Balances', font='helvetica 14 bold')
        self.title.grid(row=0, columnspan=5, sticky='ew', pady=1)

        ##############################################################################
        # add column headings
        ##############################################################################
        tk.Label(master, text='').grid(row=1, column=0, padx=10)
        tk.Label(master, text='Wells Fargo', font='helvetica 14 bold').grid(row=1, column=1, padx=10)
        tk.Label(master, text='Citi', font='helvetica 14 bold').grid(row=1, column=2, padx=10)
        tk.Label(master, text='Uber', font='helvetica 14 bold').grid(row=1, column=3, padx=10)
        tk.Label(master, text='').grid(row=1, column=4, padx=10)

        ##############################################################################
        # entry boxes to put updated balances in, fill in with forecasted value
        ##############################################################################
        current_date = int(df[df.Date == str(datetime.date.today())].index.values[-1])

        self.wf_entry = tk.Entry(master, justify='center')
        self.wf_entry.grid(row=2, column=1, padx=10)
        self.wf_entry.insert(tk.END, df.loc[current_date, 'WF'])
        self.wf_entry.configure(highlightbackground='lavender')

        self.citi_entry = tk.Entry(master, justify='center')
        self.citi_entry.grid(row=2, column=2, padx=10)
        self.citi_entry.insert(tk.END, df.loc[current_date, 'Citi'])
        self.citi_entry.configure(highlightbackground='lavender')

        self.uber_entry = tk.Entry(master, justify='center')
        self.uber_entry.grid(row=2, column=3, padx=10)
        self.uber_entry.insert(tk.END, df.loc[current_date, 'Uber'])
        self.uber_entry.configure(highlightbackground='lavender')

        ##############################################################################
        # button to continue
        ##############################################################################
        tk.Label(master, text='', font='helvetica 2').grid(row=3, columnspan=3)
        tk.Button(master, text='Continue', font='helvetica 14 bold',
                  command=self.save_and_continue).grid(row=4, column=2, sticky='ew')
        tk.Label(master, text='', font='helvetica 2').grid(row=5, columnspan=3)

        ##############################################################################
        # adjusting spacing when window expands
        ##############################################################################
        for i in range(0, 5):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

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
        master.title('Budgeting')
        self.title = tk.Label(master, text='Enter Transactions', font='helvetica 14 bold')
        self.title.grid(row=0, columnspan=8, sticky='ew', pady=10)

        tk.Label(master, text='').grid(row=1, column=0, padx=10)
        tk.Label(master, text='Date').grid(row=1, column=1, padx=10)
        tk.Label(master, text='Transaction').grid(row=1, column=2, padx=10)
        tk.Label(master, text='Amount').grid(row=1, column=3, padx=10)
        tk.Label(master, text='Wells Fargo').grid(row=1, column=4, padx=10)
        tk.Label(master, text='Citi').grid(row=1, column=5, padx=10)
        tk.Label(master, text='Uber').grid(row=1, column=6, padx=10)
        tk.Label(master, text='').grid(row=1, column=7)

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

        ##############################################################################
        # button to continue
        ##############################################################################
        tk.Label(master, text='', font='helvetica 2').grid(row=5)
        tk.Button(master, text='        Continue        ', font='helvetica 14 bold',
                  command=self.save_and_continue).grid(row=6, columnspan=8)
        tk.Label(master, text='', font='helvetica 2').grid(row=7)

        ##############################################################################
        # adjusting spacing when window expands
        ##############################################################################
        for i in range(0, 8):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

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
        master.title('Budgeting')
        master.geometry('250x200')
        tk.Label(master, text='', font='helvetica 2').grid(row=0)
        tk.Label(master, text='Select card to pay off:',
                 font='helvetica 14 bold').grid(row=1, column=0, columnspan=2)
        tk.Label(master, text='', font='helvetica 2').grid(row=2)

        self.v_citi = tk.IntVar()
        self.v_uber = tk.IntVar()

        self.citi_box = tk.Checkbutton(master, text='Citi', variable=self.v_citi)
        self.citi_box.grid(column=0, row=3)
        self.citi_date = tk.Entry(master, width=12, justify='center')
        self.citi_date.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.citi_date.grid(column=1, row=3)
        self.citi_date.configure(highlightbackground='lavender')
        self.uber_box = tk.Checkbutton(master, text='Uber', variable=self.v_uber)
        self.uber_box.grid(column=0, row=4)
        self.uber_date = tk.Entry(master, width=12, justify='center')
        self.uber_date.insert(tk.END, datetime.date.today() + datetime.timedelta(days=1))
        self.uber_date.grid(column=1, row=4)
        self.uber_date.configure(highlightbackground='lavender')

        ##############################################################################
        # button to continue
        ##############################################################################
        tk.Label(master, text='', font='helvetica 2').grid(row=5)
        tk.Button(master, text='       Continue       ', font='helvetica 14 bold',
                  command=self.save_and_continue).grid(row=6, columnspan=2)
        tk.Label(master, text='', font='helvetica 2').grid(row=7)

        ##############################################################################
        # adjusting spacing when window expands
        ##############################################################################
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        for i in range(0, 8):
            master.grid_rowconfigure(i, weight=1)

    def save_and_continue(self):
        self.transactions['citi'] = self.v_citi.get()
        self.transactions['uber'] = self.v_uber.get()
        self.transactions['citi date'] = self.citi_date.get()
        self.transactions['uber date'] = self.uber_date.get()
        self.master.destroy()
