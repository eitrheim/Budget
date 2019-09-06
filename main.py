import tkinter as tk
import re
import pandas as pd
# importing internal modules
import gui
import update_balance_df

##############################################################################
# read in past balances and add 0 days if there is not 50
##############################################################################
df = pd.read_csv('balances.csv').fillna('')
df = update_balance_df.add_days(df)
notes = pd.read_csv('notes.txt', sep='~', skip_blank_lines=False, header=None).fillna('')
notes = notes.to_string(index=False, header=False)
notes = re.sub('  +', '', notes)
##############################################################################
# show the balances that have been read in
##############################################################################
window = tk.Tk()
window0 = gui.ShowBalances(window, df, notes)
window.mainloop()
notes = window0.save_notes['saved_notes']
##############################################################################
# update current balances, delete past data, and the show new balances
#############################################################################
window = tk.Tk()
window1 = gui.EnterBalances(window, df)
window.mainloop()
df = update_balance_df.update_current_balances(df, window1)
window = tk.Tk()
window2 = gui.ShowBalances(window, df, notes)
window.mainloop()
notes = window2.save_notes['saved_notes']
##############################################################################
# add transactions and show new balances
##############################################################################
window = tk.Tk()
window3 = gui.EnterTransactions(window)
window.mainloop()
df = update_balance_df.balances_after_transactions(df, window3)
window = tk.Tk()
window4 = gui.ShowBalances(window, df, notes)
window.mainloop()
notes = window4.save_notes['saved_notes']
###################################################################################
# give option to pay off credit cards in full tomorrow then show new balances
###################################################################################
window = tk.Tk()
window5 = gui.PayoffCC(window)
window.mainloop()
df = update_balance_df.paid_off_cc(df, window5)
window = tk.Tk()
window6 = gui.ShowBalances(window, df, notes)
window.mainloop()
notes = window6.save_notes['saved_notes']
##############################################################################
# save the new balances to .csv and notes to .txt
##############################################################################
df.to_csv(r'balances.csv', index=None, header=True)
text_file = open('notes.txt', 'w')
text_file.write(notes)
text_file.close()

# TODO ability to type in transactions into grid
# TODO if I press enter, it binds/commits the buttons
# TODO calc historical spending average per day
# TODO delete transactions
# TODO pylint

