import tkinter as tk
from tkinter import messagebox


root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300)
canvas1.pack()

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def get_square_root():
    x1 = entry1.get()

    label1 = tk.Label(root, text=float(x1) ** 0.5)
    canvas1.create_window(200, 230, window=label1)
    messagebox.showinfo("showinfo", "Information")

    # messagebox.showinfo("showinfo", "Information")
    #
    # messagebox.showwarning("showwarning", "Warning")
    #
    # messagebox.showerror("showerror", "Error")
    #
    # messagebox.askquestion("askquestion", "Are you sure?")
    #
    # messagebox.askokcancel("askokcancel", "Want to continue?")
    #
    # messagebox.askyesno("askyesno", "Find the value?")
    #
    # messagebox.askretrycancel("askretrycancel", "Try again?")


button1 = tk.Button(text='Get the Square Root', command=get_square_root)
canvas1.create_window(200, 180, window=button1)

root.mainloop()