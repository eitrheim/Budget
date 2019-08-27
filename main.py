import pandas as pd
import tkinter
# importing internal modules
import gui
import update_balance_df

# read in past balances
df = pd.read_csv('balances.csv').fillna('')
# add 50 days if there is not 50
df = update_balance_df.AddDays(df)
# show the past balances
window = tkinter.Tk()
window0 = gui.ShowBalances(window, df)
window.mainloop()
# update new balances
window = tkinter.Tk()
window1 = gui.EnterBalances(window, df)
window.mainloop()
df = update_balance_df.changebalances(df, window1)
# show the new changes
window = tkinter.Tk()
window2 = gui.ShowBalances(window, df)
window.mainloop()
# add transactions
window = tkinter.Tk()
window3 = gui.EnterTransactions(window)
window.mainloop()
df = update_balance_df.update_balances(df, window3)
# show the new changes
window = tkinter.Tk()
window4 = gui.ShowBalances(window, df)
window.mainloop()
# pay off ccs
window = tkinter.Tk()
window5 = gui.PayoffCC(window)
window.mainloop()
df = update_balance_df.paidCC(df,window5)
# show the new changes
window = tkinter.Tk()
window6 = gui.ShowBalances(window, df)
window.mainloop()
# save the new balances
df.to_csv(r'balances.csv', index = None, header=True)
