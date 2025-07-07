# Tkinter - python GUI library
# we can design desktop applications with help of this
import tkinter as tk
app = tk.Tk()

app.geometry("1000x1000")
app.title("MY First")
app.config(background = "#41ac9c")

# widgets :
# text -- label()
# input_box -- Entry()
# button -- Button()
# Methods:
# pack()--center
# grid() -- rows, columns
# place()-- 
lbl= tk.Label(app, text = "Hello World!", font = ("robort", 43, "bold"), fg = "cyan", bg ="purple" )
lbl.pack(fill = "x", pady = 20, padx = 20, ipady = 5, side = "top")

inpx = tk.Entry(app, font = ("robort", 12, "italic" ))
inpx.pack()

btn = tk.Button(app, text = "click me" ,font = ("robort", 12, "bold" ), fg = "blue", bg ="red",pady = 5, padx = 5)
btn.pack()

app.mainloop()