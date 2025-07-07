
import tkinter as tk
app = tk.Tk()

import mysql.connector

    # engine

connn = mysql.connector.connect(
    host = 'localhost',
    username = "root",
    password = "Ayush@786",
    database = "SCHOOL"
)


app.geometry("800x800")
app.title("contact us form")
app.config(bg="lightblue")

x= tk.Label(app, text = "", bg = "lightblue")
x.grid(row = 0 , column = 0,  pady = 30, padx = 40)
def savedata():
    a = ent1.get()
    b = ent2.get()
    c = ent3.get()
    d = ent4.get()
    e = ent5.get()

    curr = connn.cursor()
    curr.execute(f"insert into contact_us(full_name, age, phone_number, email, message) values('{a}', {b}, '{c}', '{d}', '{e}');")

    connn.commit()
    ent1.delete(0, tk.END)
    ent2.delete(0, tk.END)
    ent3.delete(0, tk.END)
    ent4.delete(0, tk.END)
    ent5.delete(0, tk.END)


lbl1 = tk.Label(app , text = "Full name", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl2 = tk.Label(app, text = "Age", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl3= tk.Label(app, text = "Phone number", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl4= tk.Label(app, text = "E-mail", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl5= tk.Label(app, text = "Message", font= ("Robort", 20, "bold"),bg = "lightblue")

lbl6 = tk.Label(app, text = ":", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl7 = tk.Label(app, text = ":", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl8 = tk.Label(app, text = ":", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl9 = tk.Label(app, text = ":", font= ("Robort", 20, "bold"),bg = "lightblue")
lbl10 = tk.Label(app, text = ":", font= ("Robort", 20, "bold"),bg = "lightblue")

ent1 = tk.Entry(app, font= ("Robort", 20))
ent2 = tk.Entry(app, font= ("Robort", 20))
ent3 = tk.Entry(app, font= ("Robort", 20))
ent4 = tk.Entry(app, font= ("Robort", 20))
ent5 = tk.Entry(app, font= ("Robort", 20))


lbl1.grid(row = 1 , column = 1)
lbl2.grid(row = 2 , column = 1)
lbl3.grid(row = 3 , column = 1)
lbl4.grid(row = 4 , column = 1)
lbl5.grid(row = 5 , column = 1)

lbl6.grid(row = 1 , column = 2)
lbl7.grid(row = 2 , column = 2)
lbl8.grid(row = 3 , column = 2)
lbl9.grid(row = 4 , column = 2)
lbl10.grid(row = 5 , column = 2)

ent1.grid(row = 1, column = 3, pady = 10, padx = 10 )
ent2.grid(row = 2, column = 3, pady = 10, padx = 10 )
ent3.grid(row = 3, column = 3, pady = 10, padx = 5 )
ent4.grid(row = 4, column = 3, pady = 10, padx = 5 )
ent5.grid(row = 5, column = 3, pady = 10, padx = 5 )

btn = tk.Button(app, text = "Submit",font= ("Robort", 20, "bold"), command = savedata)

btn.grid(rows = 6, column = 3, padx = 40, pady = 40)





app.mainloop()
