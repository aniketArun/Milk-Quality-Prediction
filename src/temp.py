from tkinter import *


root = Tk()
img = PhotoImage(file="cow.png")

Label(image=img).pack()
root.mainloop()