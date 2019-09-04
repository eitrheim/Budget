import pandas as pd
import tkinter as tk
# importing internal modules
import gui
import update_balance_df

##############################################################################
# read in past balances and add 0 days if there is not 50
##############################################################################
df = pd.read_csv('balances.csv').fillna('')
df = update_balance_df.add_days(df)
##############################################################################
# show the balances that have been read in
##############################################################################
window = tk.Tk()
window0 = gui.ShowBalances(window, df)
window.mainloop()
##############################################################################
# update current balances, delete past data, and the show new balances
##############################################################################
window = tk.Tk()
window1 = gui.EnterBalances(window, df)
window.mainloop()
df = update_balance_df.update_current_balances(df, window1)
window = tk.Tk()
window2 = gui.ShowBalances(window, df)
window.mainloop()
##############################################################################
# add transactions and show new balances
##############################################################################
window = tk.Tk()
window3 = gui.EnterTransactions(window)
window.mainloop()
df = update_balance_df.balances_after_transactions(df, window3)
window = tk.Tk()
window4 = gui.ShowBalances(window, df)
window.mainloop()
###################################################################################
# give option to pay off credit cards in full tomorrow then show new balances
###################################################################################
window = tk.Tk()
window5 = gui.PayoffCC(window)
window.mainloop()
df = update_balance_df.paid_off_cc(df,window5)
window = tk.Tk()
window6 = gui.ShowBalances(window, df)
window.mainloop()
##############################################################################
# save the new balances to .csv
##############################################################################
df.to_csv(r'balances.csv', index = None, header=True)

# TODO persistent notes at the bottom
# TODO updating cc payment
# TODO ability to type in transactions into grid
