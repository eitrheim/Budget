import datetime
import pandas as pd
# TODO add more sectioning

##############################################################################
# add days to end of df if there is less than 50 days in the future
##############################################################################
def add_days(df):
    x = str(df.loc[len(df) - 1, 'Date']).split('-')
    x = datetime.date(int(x[0]), int(x[1]), int(x[2])) - datetime.date.today()

    if x.days < 50:
        for i in range(50):
            n = str(df.loc[len(df) - 1, 'Date']).split('-')
            n = datetime.date(int(n[0]), int(n[1]), int(n[2]))
            the_date = n + datetime.timedelta(days=1)
            df.loc[len(df)] = [str(the_date), '', 0, 15, 25, df.loc[len(df) - 1, 'WF'],
                               df.loc[len(df) - 1, 'Citi'], df.loc[len(df) - 1, 'Uber']]

    for i in range(1, len(df.Date)):
        if df.Transaction[i] == "Pay off Citi":
            x = -df.loc[i-1, 'Citi']
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Citi Amount'] = x
        elif df.loc[i, "Transaction"] == "Pay off Uber":
            x = -df.loc[i-1, 'Uber']
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Uber Amount'] = x
        else:
            pass
        df.loc[i, 'WF'] = df.loc[i - 1, 'WF'] + df.loc[i, 'WF Amount']
        df.loc[i, 'Citi'] = df.loc[i - 1, 'Citi'] + df.loc[i, 'Citi Amount']
        df.loc[i, 'Uber'] = df.loc[i - 1, 'Uber'] + df.loc[i, 'Uber Amount']

    df[['WF', 'Citi', 'Uber']] = round(df[['WF', 'Citi', 'Uber']], 2)
    df.reset_index(inplace=True, drop=True)

    return df


##############################################################################
# update balances after entering current balances
##############################################################################
def update_current_balances(df, window1):
    current_date = df[df.Date == str(datetime.date.today())].index.values[-1].astype(int)
    df.drop(range(0, current_date), axis=0, inplace=True)
    df.reset_index(inplace=True, drop=True)

    df.loc[0, 'WF'] = float(window1.balances['wf'])
    df.loc[0, 'Citi'] = float(window1.balances['citi'])
    df.loc[0, 'Uber'] = float(window1.balances['uber'])
    df.loc[0, 'WF Amount'] = 0
    df.loc[0, 'Citi Amount'] = 0
    df.loc[0, 'Uber Amount'] = 0
    df.loc[0, 'Transaction'] = ''

    for i in range(1, len(df)):
        if df.loc[i, "Transaction"] == "Pay off Citi":
            x = -df.loc[i-1, 'Citi']
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Citi Amount'] = x
        elif df.loc[i, "Transaction"] == "Pay off Uber":
            x = -df.loc[i-1, 'Uber']
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Uber Amount'] = x
        else:
            pass
        df.loc[i, 'WF'] = df.loc[i - 1, 'WF'] + df.loc[i, 'WF Amount']
        df.loc[i, 'Citi'] = df.loc[i - 1, 'Citi'] + df.loc[i, 'Citi Amount']
        df.loc[i, 'Uber'] = df.loc[i - 1, 'Uber'] + df.loc[i, 'Uber Amount']

    df[['WF', 'Citi', 'Uber']] = round(df[['WF', 'Citi', 'Uber']], 2)
    df.reset_index(inplace=True, drop=True)

    return df


##############################################################################
# update balances after entering transactions
##############################################################################
def balances_after_transactions(df, window3):
    if len(window3.transactions['transaction amount1']) > 0:
        x = window3.transactions['transaction date1'].split('-')
        rownum = df[df.Date == str(datetime.date(int(x[0]), int(x[1]), int(x[2])))].index[-1]
        if bool(df.loc[rownum, 'Transaction']):
            line = pd.DataFrame({"Date": df.Date.loc[rownum],
                                 "Transaction": window3.transactions['transaction entry1']}, index=[rownum + 1])
            df = pd.concat([df.loc[:rownum], line, df.loc[rownum + 1:]], sort=False)
            df.reset_index(inplace=True, drop=True)
            rownum = rownum + 1
        else:
            df.loc[rownum, 'Transaction'] = window3.transactions['transaction entry1']
        x = float(window3.transactions['transaction amount1'])
        df.loc[rownum, 'WF Amount'] = x * window3.transactions['wf1']
        df.loc[rownum, 'Citi Amount'] = x * window3.transactions['citi1']
        df.loc[rownum, 'Uber Amount'] = x * window3.transactions['uber1']

    if len(window3.transactions['transaction amount2']) > 0:
        x = window3.transactions['transaction date2'].split('-')
        rownum = df[df.Date == str(datetime.date(int(x[0]), int(x[1]), int(x[2])))].index[-1]
        if bool(df.loc[rownum, 'Transaction']):
            line = pd.DataFrame({"Date": df.Date.loc[rownum],
                                 "Transaction": window3.transactions['transaction entry2']}, index=[rownum + 1])
            df = pd.concat([df.loc[:rownum], line, df.loc[rownum + 1:]], sort=False)
            df.reset_index(inplace=True, drop=True)
            rownum = rownum + 1
        else:
            df.loc[rownum, 'Transaction'] = window3.transactions['transaction entry2']
        x = float(window3.transactions['transaction amount2'])
        df.loc[rownum, 'WF Amount'] = x * window3.transactions['wf2']
        df.loc[rownum, 'Citi Amount'] = x * window3.transactions['citi2']
        df.loc[rownum, 'Uber Amount'] = x * window3.transactions['uber2']

    if len(window3.transactions['transaction amount3']) > 0:
        x = window3.transactions['transaction date3'].split('-')
        rownum = df[df.Date == str(datetime.date(int(x[0]), int(x[1]), int(x[2])))].index[-1]
        if bool(df.loc[rownum, 'Transaction']):
            line = pd.DataFrame({"Date": df.Date.loc[rownum],
                                 "Transaction": window3.transactions['transaction entry3']}, index=[rownum + 1])
            df = pd.concat([df.loc[:rownum], line, df.loc[rownum + 1:]], sort=False)
            df.reset_index(inplace=True, drop=True)
            rownum = rownum + 1
        else:
            df.loc[rownum, 'Transaction'] = window3.transactions['transaction entry3']
        x = float(window3.transactions['transaction amount3'])
        df.loc[rownum, 'WF Amount'] = x * window3.transactions['wf3']
        df.loc[rownum, 'Citi Amount'] = x * window3.transactions['citi3']
        df.loc[rownum, 'Uber Amount'] = x * window3.transactions['uber3']

    for i in range(1, len(df)):
        if df.loc[i, "Transaction"] == "Pay off Citi":
            x = -df.loc[i-1, 'Citi']
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Citi Amount'] = x
        elif df.loc[i, "Transaction"] == "Pay off Uber":
            x = -df.loc[i-1, 'Uber']
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Uber Amount'] = x
        else:
            pass
        df.loc[i, 'WF'] = df.loc[i - 1, 'WF'] + df.loc[i, 'WF Amount']
        df.loc[i, 'Citi'] = df.loc[i - 1, 'Citi'] + df.loc[i, 'Citi Amount']
        df.loc[i, 'Uber'] = df.loc[i - 1, 'Uber'] + df.loc[i, 'Uber Amount']

    df[['WF', 'Citi', 'Uber']] = round(df[['WF', 'Citi', 'Uber']], 2)
    return df


##############################################################################
# update balances after paying off CCs
##############################################################################
def paid_off_cc(df, window5):
    if window5.transactions['citi'] == 1:
        x = window5.transactions['citi date'].split('-')
        x = datetime.date(int(x[0]), int(x[1]), int(x[2]))
        rownum = df[df.Date == str(x)].index.values[-1].astype(int)
        if bool(df.loc[rownum, 'Transaction']):
            line = pd.DataFrame({"Date": window5.transactions['citi date'],
                                 'Transaction': 'Pay off Citi',
                                 'Uber Amount': 0}, index=[rownum + 1])
            df = pd.concat([df.loc[:rownum], line, df.loc[rownum + 1:]], sort=False)
            df.reset_index(inplace=True, drop=True)
        else:
            df.loc[rownum, 'Transaction'] = 'Pay off Citi'

    if window5.transactions['uber'] == 1:
        x = window5.transactions['uber date'].split('-')
        x = datetime.date(int(x[0]), int(x[1]), int(x[2]))
        rownum = df[df.Date == str(x)].index.values[-1].astype(int)
        if bool(df.loc[rownum, 'Transaction']):
            line = pd.DataFrame({"Date": window5.transactions['uber date'],
                                 'Transaction': 'Pay off Uber',
                                 'Citi Amount': 0}, index=[rownum + 1])
            df = pd.concat([df.loc[:rownum], line, df.loc[rownum + 1:]], sort=False)
            df.reset_index(inplace=True, drop=True)
        else:
            df.loc[rownum, 'Transaction'] = 'Pay off Uber'

    for i in range(1, len(df)):
        if df.loc[i, "Transaction"] == "Pay off Citi":
            x = -float(df.loc[i-1, 'Citi'])
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Citi Amount'] = x
        elif df.loc[i, "Transaction"] == "Pay off Uber":
            x = -float(df.loc[i-1, 'Uber'])
            df.loc[i, 'WF Amount'] = x
            df.loc[i, 'Uber Amount'] = x
        else:
            pass
        df.loc[i, 'WF'] = df.loc[i - 1, 'WF'] + df.loc[i, 'WF Amount']
        df.loc[i, 'Citi'] = df.loc[i - 1, 'Citi'] + df.loc[i, 'Citi Amount']
        df.loc[i, 'Uber'] = df.loc[i - 1, 'Uber'] + df.loc[i, 'Uber Amount']

    df[['WF', 'Citi', 'Uber']] = round(df[['WF', 'Citi', 'Uber']], 2)

    return df
