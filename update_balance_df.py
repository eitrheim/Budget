import datetime


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
            df.loc[len(df)] = [str(the_date), '', 0, -15, -25, df.loc[len(df) - 1, 'WF'],
                               df.loc[len(df) - 1, 'Citi'], df.loc[len(df) - 1, 'Uber']]

    df.reset_index(inplace=True, drop=True)

    return df


##############################################################################
# update balances after entering current balances
##############################################################################
def update_current_balances(df, window1):
    current_date = int(df[df.Date == str(datetime.date.today())].index.values)

    df.loc[current_date, 'WF'] = float(window1.balances['wf'])
    df.loc[current_date, 'Citi'] = float(window1.balances['citi'])
    df.loc[current_date, 'Uber'] = float(window1.balances['uber'])
    df.loc[current_date, 'WF Amount'] = 0
    df.loc[current_date, 'Citi Amount'] = 0
    df.loc[current_date, 'Uber Amount'] = 0
    df.loc[current_date, 'Transaction'] = ''

    for i in range(current_date + 1, len(df) - 1):
        df.loc[i, 'WF'] = df.loc[i - 1, 'WF'] + df.loc[i, 'WF Amount']
        df.loc[i, 'Citi'] = df.loc[i - 1, 'Citi'] + df.loc[i, 'Citi Amount']
        df.loc[i, 'Uber'] = df.loc[i - 1, 'Uber'] + df.loc[i, 'Uber Amount']

    df[['WF', 'Citi', 'Uber']] = round(df[['WF', 'Citi', 'Uber']], 2)
    df = df.loc[current_date:, ]
    df.reset_index(inplace=True, drop=True)

    return df


##############################################################################
# update balances after entering transactions
##############################################################################
def balances_after_transactions(df, window3):
    if len(window3.transactions['transaction amount1']) > 0:
        x = window3.transactions['transaction date1'].split('-')
        rownum = df[df.Date == str(datetime.date(int(x[0]), int(x[1]), int(x[2])))].index
        if df.loc[rownum, 'Transaction'] != '':
            df.loc[rownum, 'Transaction'] = df.loc[rownum, 'Transaction'] + " & " +\
                                            window3.transactions['transaction entry1']
        else:
            df.loc[rownum, 'Transaction'] = window3.transactions['transaction entry1']
        x = float(window3.transactions['transaction amount1'])
        df.loc[rownum, 'WF Amount'] = df.loc[rownum, 'WF Amount'] + x * window3.transactions['wf1']
        df.loc[rownum, 'Citi Amount'] = df.loc[rownum, 'Citi Amount'] + \
                                        x * window3.transactions['citi1']
        df.loc[rownum, 'Uber Amount'] = df.loc[rownum, 'Uber Amount'] + \
                                        x * window3.transactions['uber1']

    if len(window3.transactions['transaction amount2']) > 0:
        x = window3.transactions['transaction date2'].split('-')
        rownum = df[df.Date == str(datetime.date(int(x[0]), int(x[1]), int(x[2])))].index
        if df.loc[rownum, 'Transaction'] != '':
            df.loc[rownum, 'Transaction'] = df.loc[rownum, 'Transaction'] + " & " +\
                                            window3.transactions['transaction entry2']
        else:
            df.loc[rownum, 'Transaction'] = window3.transactions['transaction entry2']
        x = float(window3.transactions['transaction amount2'])
        df.loc[rownum, 'WF Amount'] = df.loc[rownum, 'WF Amount'] + x * window3.transactions['wf2']
        df.loc[rownum, 'Citi Amount'] = df.loc[rownum, 'Citi Amount'] + \
                                        x * window3.transactions['citi2']
        df.loc[rownum, 'Uber Amount'] = df.loc[rownum, 'Uber Amount'] + \
                                        x * window3.transactions['uber2']

    if len(window3.transactions['transaction amount3']) > 0:
        x = window3.transactions['transaction date3'].split('-')
        rownum = df[df.Date == str(datetime.date(int(x[0]), int(x[1]), int(x[2])))].index
        if df.loc[rownum, 'Transaction'] != '':
            df.loc[rownum, 'Transaction'] = df.loc[rownum, 'Transaction'] + " & " +\
                                            window3.transactions['transaction entry3']
        else:
            df.loc[rownum, 'Transaction'] = window3.transactions['transaction entry3']
        x = float(window3.transactions['transaction amount3'])
        df.loc[rownum, 'WF Amount'] = df.loc[rownum, 'WF Amount'] + x * window3.transactions['wf3']
        df.loc[rownum, 'Citi Amount'] = df.loc[rownum, 'Citi Amount'] + \
                                        x * window3.transactions['citi3']
        df.loc[rownum, 'Uber Amount'] = df.loc[rownum, 'Uber Amount'] + \
                                        x * window3.transactions['uber3']

    for i in range(2, len(df)):
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
        rownum = df[df.Date == window5.transactions['citi date']].index.values
        x = -float(df.loc[rownum, 'Citi'])
        df.loc[rownum + 1, 'WF Amount'] = x + df.loc[rownum + 1, 'WF Amount']
        df.loc[rownum + 1, 'Citi Amount'] = x + df.loc[rownum + 1, 'Citi Amount']
        df.loc[rownum + 1, 'Transaction'] = df.loc[rownum + 1, 'Transaction'] + " Pay off Citi"

    if window5.transactions['uber'] == 1:
        rownum = df[df.Date == window5.transactions['uber date']].index.values
        x = -float(df.loc[rownum, 'Uber'])
        df.loc[rownum + 1, 'WF Amount'] = x + df.loc[rownum + 1, 'WF Amount']
        df.loc[rownum + 1, 'Uber Amount'] = x + df.loc[rownum + 1, 'Uber Amount']
        df.loc[rownum + 1, 'Transaction'] = df.loc[rownum + 1, 'Transaction'] + " Pay off Uber"

    for i in range(1, len(df)):
        df.loc[i, 'WF'] = df.loc[i - 1, 'WF'] + df.loc[i, 'WF Amount']
        df.loc[i, 'Citi'] = df.loc[i - 1, 'Citi'] + df.loc[i, 'Citi Amount']
        df.loc[i, 'Uber'] = df.loc[i - 1, 'Uber'] + df.loc[i, 'Uber Amount']

    df[['WF', 'Citi', 'Uber']] = round(df[['WF', 'Citi', 'Uber']], 2)

    return df
