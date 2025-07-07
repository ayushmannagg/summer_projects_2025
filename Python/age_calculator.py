import tkinter as tk

def calAge():
    xy = int(agee.get())
    xy = 2025 - xy
    age.config(text = f"Your age is: {xy}")

app = tk.Tk()

app.geometry("500x500")
app.title("Age calculator")
app.config(bg = "cyan")

xyz = tk.Label(app,text = "Age Calculator", bg ="#12a180" ,
               font = ("robort", 25, "bold"))
xyz.pack(fill ="x", ipady = "5")

xyz = tk.Label(app,text = "Enter your Birth Year:", bg ="#12a180" ,
               font = ("robort", 15, "bold"))
xyz.pack(ipady = "5")

agee = tk.Entry(app, font = ("robort", 20, "bold"), bg = "#b1f0e1",
                fg = "#139c7b")
agee.pack(pady = 20)

btn = tk.Button(app, text = "Check Age",font = ("robort", 15, "bold"), bg = "#b1f0e1",
                fg = "#139c7b", command = calAge )
btn.pack(ipadx = 15)

age = tk.Label(app, text = "",font = ("robort", 15, "bold"), bg = "#b1f0e1",
                fg = "#139c7b")
age.pack(pady = 10)








app.mainloop()







