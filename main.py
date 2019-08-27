import datetime
import pandas as pd
import tkinter
import gui

# read in past balances
df = pd.read_csv('balances.csv').fillna('')
# add 50 days if there is not 50 # TODO test this
df = gui.AddDays(df)
# show the past balances
window = tkinter.Tk()
window0 = gui.ShowBalances(window, df)
window.mainloop()
# update new balances
window = tkinter.Tk()
window1 = gui.EnterBalances(window, df)
window.mainloop()
df = gui.changebalances(df, window1)
# show the new changes
window = tkinter.Tk()
window2 = gui.ShowBalances(window, df)
window.mainloop()
# add transactions
window = tkinter.Tk()
window3 = gui.EnterTransactions(window)
window.mainloop()
df = gui.update_balances(df, window3)
print(df.head(5))
print(df.tail(5))

# show the new changes
window = tkinter.Tk()
window4 = gui.ShowBalances(window, df)
window.mainloop()
# pay off ccs
window = tkinter.Tk()
window5 = gui.PayoffCC(window)
window.mainloop()
df = gui.paidCC(df,window5)
# show the new changes
print(df.head(5))
print(df.tail(5))

window = tkinter.Tk()
window6 = gui.ShowBalances(window, df)
window.mainloop()
# save the new balances
# df.to_csv(r'balances.csv', index = None, header=True)
