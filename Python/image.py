import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox

conn = mysql.connector.connect(
    host = "localhost",
    username = "root",
    password = "Ayush@786",
    database = "SCHOOL"
)

cr = conn.cursor()

def saveinfo():
    full_nm = ent1.get()
    email = ent2.get()
    phone = ent3.get() 
    message = ent4.get()

    cr.execute(f"insert into contactinfo(ful_name, email_id, phone_number, message) values({full_nm}, {email}, {phone}, {message});")
    conn.commit()

    messagebox.showinfo("Data Saved", "Your data saved successfully in database")
app = tk.Tk()

app.geometry("1000x600")
app.title("Contact Us Form")
app.config(bg = "lightblue")

frame1 = tk.Frame(app, relief = "raised", borderwidth = 20, bg = "#5888d6")
frame1.pack(fill ="x")

contact_lbl = tk.Label(frame1, text = "Contact Us Now", font=("robert", 20, "bold"), bg = "#5888d6" )
contact_lbl.pack()

frame2 = tk.Frame(app, relief ="groove",borderwidth= 20, bg = "#5888d6" )
frame2.pack(fill = "x")

img = Image.open("C:\Summer 2025 Projects\Python\contact.jpg")
img_new = ImageTk.PhotoImage(img)

imgg = tk.Label(frame2, image = img_new, height = 200 )
imgg.pack()

frame3 = tk.Frame(app, relief = "sunken", bg = "#5888d6", borderwidth= 20)
frame3.pack(fill ="x")

frame4 = tk.Frame(frame3, bg = "#5888d6")
frame4.grid(row = 0, column = 0)

frame5 = tk.Frame(frame3, bg = "#5888d6")
frame5.grid(row = 0, column = 1,)

lbl1 = tk.Label(frame4, text = "Full Name",font = ("robert", 20), bg = "#5888d6")
lbl2 = tk.Label(frame4, text = "Email Id",font = ("robert", 20), bg = "#5888d6")

lbl3 = tk.Label(frame5, text = "Phone No.",font = ("robert", 20), bg = "#5888d6")
lbl4 = tk.Label(frame5, text = "Message",font = ("robert", 20), bg = "#5888d6")

lbl5 = tk.Label(frame4, text = ":",font = ("robert", 20), bg = "#5888d6")
lbl6 = tk.Label(frame4, text = ":",font = ("robert", 20), bg = "#5888d6")

lbl7 = tk.Label(frame5, text = ":",font = ("robert", 20), bg = "#5888d6")
lbl8 = tk.Label(frame5, text = ":",font = ("robert", 20), bg = "#5888d6")


ent1 = tk.Entry(frame4,font = ("robert", 20), bg = "#5888d6")
ent2 = tk.Entry(frame4,font = ("robert", 20), bg = "#5888d6")

ent3 = tk.Entry(frame5,font = ("robert", 20), bg = "#5888d6")
ent4 = tk.Entry(frame5,font = ("robert", 20), bg = "#5888d6")


lbl1.grid(row = 1, column = 1)
lbl2.grid(row = 2, column = 1)
lbl5.grid(row = 1, column = 2)
lbl6.grid(row = 2, column = 2)
ent1.grid(row= 1, column = 3)
ent2.grid(row= 2, column = 3)

lbl3.grid(row = 1, column = 1)
lbl4.grid(row = 2, column = 1)
lbl7.grid(row = 1, column = 2)
lbl8.grid(row = 2, column = 2)
ent3.grid(row= 1, column = 3)
ent4.grid(row= 2, column = 3)

frame6 = tk.Frame(app)
frame6.pack(fill = "x")
btn = tk.Button( text = "Submit",font = ("robert", 20), bg = "#5888d6", command = saveinfo)
btn.pack(pady = 20, padx = 20)




app.mainloop()






















