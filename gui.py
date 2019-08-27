
import tkinter
import datetime


#########################################################################
# show balances for 15 days into future
#########################################################################

class ShowBalances():

    def __init__(self, master, df):
        self.master = master
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Account Balances', font='Helvetica 9 bold')
        self.title.grid(row=0, columnspan=5, sticky='ew')   

        c = 0
        for i in df.columns:
            tkinter.Label(master, text=i, font='Helvetica 9 bold').grid(row=1, column=c)
            c = c + 1

        ##############################################################
        # adding the results to the results table
        ##############################################################
        
        start_date = int(df[df.Date == str(datetime.date.today())].index.values)
        c = 0
        for x in ['Date','Transaction','WF Amount','Citi Amount','Uber Amount']:
            r = 2
            for y in range(start_date, start_date + 15):
                tkinter.Label(master, text=df[x].iloc[y], font='Helvetica 9').grid(row=r, column=c)
                r = r + 1
            c = c + 1
        
        c = 5
        for x in ['WF']:
            r = 2
            for y in range(start_date, start_date + 15):
                tkinter.Label(master, text=df[x].iloc[y], font='Helvetica 9', background='Gray67', width=8).grid(row=r, column=c)
                r = r + 1
            c = c + 1
            
        c = 6
        for x in ['Citi', 'Uber']:
            r = 2
            for y in range(start_date, start_date + 15):
                tkinter.Label(master, text=df[x].iloc[y], font='Helvetica 9', width=8).grid(row=r, column=c)
                r = r + 1
            c = c + 1
            
        run_model_button = tkinter.Button(master, text='Okay', command=master.destroy)
        run_model_button.grid(row=17, columnspan=12, pady=10)


#########################################################################
# add days to end of df if there is less than 50 days in the future
#########################################################################

def AddDays(df):
    x = df.Date.iloc[-1].split('-')
    x = datetime.date(int(x[0]),int(x[1]),int(x[2])) - datetime.date.today()
    if x.days < 50:
        for i in range(50):
            the_date = df.Date.iloc[-1] + datetime.timedelta(days=1)
            df.loc[i+1] = [the_date, '', 0, 0, 0, 0, 0, 0]
    return df

#########################################################################
# update balances
#########################################################################

class EnterBalances:
    balances = {}

    def __init__(self, master, df):
        self.master = master
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Enter Account Balances', font='Helvetica 9 bold')
        self.title.grid(row=0, columnspan=5, sticky='ew')       

        tkinter.Label(master, text = "").grid(row=1,  column=0, padx=10)
        tkinter.Label(master, text = "Wells Fargo").grid(row=1, column=1, padx=10)
        tkinter.Label(master, text = "Citi").grid(row=1, column=2, padx=10)
        tkinter.Label(master, text = "Uber").grid(row=1, column=3, padx=10)
        tkinter.Label(master, text = "").grid(row=1,  column=4, padx=10)
        
        current_date = int(df[df.Date == str(datetime.date.today())].index.values)
        
        self.wf_entry = tkinter.Entry(master)
        self.wf_entry.grid(row=2, column=1)
        self.wf_entry.insert(tkinter.END, df.loc[current_date, "WF"])
        self.citi_entry = tkinter.Entry(master)
        self.citi_entry.grid(row=2, column=2)
        self.citi_entry.insert(tkinter.END, df.loc[current_date, "Citi"])
        self.uber_entry = tkinter.Entry(master)
        self.uber_entry.grid(row=2, column=3)
        self.uber_entry.insert(tkinter.END, df.loc[current_date, "Uber"])
        
        tkinter.Label(master, text = "").grid(row=3, columnspan=3)
        self.continue_button = tkinter.Button(master, text='Continue', command=self.save_and_continue)
        self.continue_button.grid(row=4, column=2, sticky='ew')
        tkinter.Label(master, text = "").grid(row=5, columnspan=3)

    def save_and_continue(self):
        self.balances['wf'] = self.wf_entry.get()
        self.balances['citi'] = self.citi_entry.get()
        self.balances['uber'] = self.uber_entry.get()                                                             
        self.master.destroy()        

def changebalances(df,window1):
    current_date = int(df[df.Date == str(datetime.date.today())].index.values)
                       
    df.loc[current_date,'WF'] = float(window1.balances['wf'])
    df.loc[current_date,'Citi'] = float(window1.balances['citi'])
    df.loc[current_date,'Uber'] = float(window1.balances['uber'])
    df.loc[current_date,'WF Amount'] = 0
    df.loc[current_date,'Citi Amount'] = 0
    df.loc[current_date,'Uber Amount'] = 0
    df.loc[current_date,'Transaction'] = ''
    
    for i in range(current_date + 1, len(df)-1):
        df.loc[i,'WF'] = df.loc[i-1,'WF'] + df.loc[i,'WF Amount']
        df.loc[i,'Citi'] = df.loc[i-1,'Citi'] + df.loc[i,'Citi Amount']
        df.loc[i,'Uber'] = df.loc[i-1,'Uber'] + df.loc[i,'Uber Amount']
    
    return df         
        
        
#########################################################################
# add transactions
#########################################################################   

class EnterTransactions:
    transactions = {}

    def __init__(self, master):
        self.master = master
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Enter Transactions', font='Helvetica 9 bold')
        self.title.grid(row=0, columnspan=8, sticky='ew', pady=10)       

        
        tkinter.Label(master, text = "").grid(row=1,  column=0, padx=10)
        tkinter.Label(master, text = "Date").grid(row=1,  column=1, padx=10)
        tkinter.Label(master, text = "Transaction").grid(row=1, column=2, padx=10)
        tkinter.Label(master, text = "Amount").grid(row=1, column=3, padx=10)
        tkinter.Label(master, text = "Wells Fargo").grid(row=1, column=4, padx=10)
        tkinter.Label(master, text = "Citi").grid(row=1,  column=5, padx=10)
        tkinter.Label(master, text = "Uber").grid(row=1,  column=6, padx=10)
        tkinter.Label(master, text = "").grid(row=1,  column=7, padx=10)
        
        self.date_entry1 = tkinter.Entry(master, width=12, justify='center')
        self.date_entry1.grid(row=2, column=1)
        self.date_entry1.insert(tkinter.END, datetime.date.today())       
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
        self.date_entry2.insert(tkinter.END, datetime.date.today())
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
        self.date_entry3.insert(tkinter.END, datetime.date.today())
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

        tkinter.Label(master, text = "").grid(row=5) 
        self.continue_button = tkinter.Button(master, text='Continue', command=self.save_and_continue)
        self.continue_button.grid(row=6, column=3)
        tkinter.Label(master, text = "").grid(row=6)

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
        self.transactions['wf2'] = self.v_wf1.get()
        self.transactions['citi2'] = self.v_citi2.get()
        self.transactions['uber2'] = self.v_uber2.get()
                
        self.transactions['transaction date3'] = self.date_entry3.get()
        self.transactions['transaction entry3'] = self.transaction_entry3.get()
        self.transactions['transaction amount3'] = self.amount_entry3.get()
        self.transactions['wf3'] = self.v_wf3.get()
        self.transactions['citi3'] = self.v_citi3.get()
        self.transactions['uber3'] = self.v_uber3.get()            
        self.master.destroy()  

def update_balances(df, window3):
    if len(window3.transactions['transaction amount1']) > 0:
        x = window3.transactions['transaction date1'].split('-')
        rownum = df[df.Date == datetime.date(int(x[0]),int(x[1]),int(x[2]))].index
        df.loc[rownum,'Transaction'] += " " + window3.transactions['transaction entry1']
        x = float(window3.transactions['transaction amount1'])
        df.loc[rownum,'WF Amount'] += x * window3.transactions['wf1']
        df.loc[rownum,'Citi Amount'] += x * window3.transactions['citi1']
        df.loc[rownum,'Uber Amount'] += x * window3.transactions['uber1']
    
    if len(window3.transactions['transaction amount2']) > 0:
        x = window3.transactions['transaction date2'].split('-')
        rownum = df[df.Date == datetime.date(int(x[0]),int(x[1]),int(x[2]))].index
        df.loc[rownum,'Transaction'] += " " + window3.transactions['transaction entry2']
        x = float(window3.transactions['transaction amount2'])
        df.loc[rownum,'WF Amount'] += x * window3.transactions['wf2']
        df.loc[rownum,'Citi Amount'] += x * window3.transactions['citi2']
        df.loc[rownum,'Uber Amount'] += x * window3.transactions['uber2']
    
    if len(window3.transactions['transaction amount3']) > 0:
        x = window3.transactions['transaction date3'].split('-')
        rownum = df[df.Date == datetime.date(int(x[0]),int(x[1]),int(x[2]))].index
        df.loc[rownum,'Transaction'] += " " + window3.transactions['transaction entry3']
        x = float(window3.transactions['transaction amount3'])
        df.loc[rownum,'WF Amount'] += x * window3.transactions['wf3']
        df.loc[rownum,'Citi Amount'] += x * window3.transactions['citi3']
        df.loc[rownum,'Uber Amount'] += x * window3.transactions['uber3']

    for i in range(1,len(df)-1):
        df.loc[i,'WF'] = df.loc[i-1,'WF'] + df.loc[i,'WF Amount']
        df.loc[i,'Citi'] = df.loc[i-1,'Citi'] + df.loc[i,'Citi Amount']
        df.loc[i,'Uber'] = df.loc[i-1,'Uber'] + df.loc[i,'Uber Amount']
    return df 


#########################################################################
# pay off uber or citi credit card
#########################################################################       
        
class PayoffCC:
    transactions = {}

    def __init__(self, master):
        self.master = master
        master.geometry("200x160")
        master.title("Budgeting")
        self.title = tkinter.Label(master, text='Select card to pay off:', font='Helvetica 9 bold')
        self.title.pack(pady=10)       

        self.v_citi = tkinter.IntVar()
        self.v_uber = tkinter.IntVar()
        self.citi_box = tkinter.Checkbutton(master, text='Citi', variable=self.v_citi)
        self.citi_box.pack()
        self.uber_box = tkinter.Checkbutton(master, text='Uber', variable=self.v_uber)
        self.uber_box.pack()

        tkinter.Label(master, text = "").pack()
        self.continue_button = tkinter.Button(master, text='Continue', command=self.save_and_continue)
        self.continue_button.pack()
        tkinter.Label(master, text = "").pack()

    def save_and_continue(self):
        self.transactions['citi'] = self.v_citi.get()
        self.transactions['uber'] = self.v_uber.get()
        self.master.destroy()      
        
def paidCC(df, window5):
    if window5.transactions['citi'] == 1:
        rownum = df[df.Date == datetime.date.today()].index
        x = -float(df.loc[(rownum -1) ,'Citi'])
        df.loc[rownum,'WF Amount'] += x
        df.loc[rownum,'Citi Amount'] += x
        df.loc[rownum,'Transaction'] += " Pay off Citi"
        
    if window5.transactions['uber'] == 1:
        rownum = df[df.Date == datetime.date.today()].index
        x = -float(df.loc[rownum -1 ,'Uber'])
        df.loc[rownum,'WF Amount'] += x
        df.loc[rownum,'Uber Amount'] += x
        df.loc[rownum,'Transaction'] += " Pay off Uber"

    for i in range(1,len(df)):
        df.loc[i,'WF'] = df.loc[i-1,'WF'] + df.loc[i,'WF Amount']
        df.loc[i,'Citi'] = df.loc[i-1,'Citi'] + df.loc[i,'Citi Amount']
        df.loc[i,'Uber'] = df.loc[i-1,'Uber'] + df.loc[i,'Uber Amount']
    return df 
        