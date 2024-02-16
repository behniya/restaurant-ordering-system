import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror , showinfo , askquestion
import sys
import re
import os
from datetime import datetime
import decimal

global cost
cost = 0

global itemID
itemID = []

global Running 
Running = True

def close_window():
    global Running
    Running = False
    sys.exit()

def sql_connection():
    try:
        con = mysql.connector.connect(
                                      host = '127.0.0.1',
                                      password = 'av21gbwjgkvtn',
                                      database = 'restaurantdb',
                                      user = 'root')
        if con.is_connected():
            pass
    except Error as e:
        print('Problem while connecting to the database\n' , e)
    
    return con

def sql_cursor(con):
    cur = con.cursor()

    return cur

def submit():
    global cost

    con = sql_connection()
    cur = sql_cursor(con)

    ords = (mycombo.get() + '\t' + str(countlbl.cget('text')))
    orders_label.config(text = (orders_label.cget('text') + '\n' + ords))

    itemID.append(int(mycombo.get()[0]))
    cur.execute(f"SELECT item_cost FROM menue WHERE item_id = {itemID[-1]}")
    isnumbs = ""
    for i in str(cur.fetchall()):
        if i.isdigit() or i == ".":
            isnumbs = isnumbs + i
    cost = cost + (decimal.Decimal(isnumbs)*decimal.Decimal(countlbl.cget('text')))

    global value
    value = IntVar(value = 1)
    countlbl.config(textvariable = value)

    mycombo.current('0')

    con.commit()
    con.close()
    cur.close()

def restart_win():
    orders_label.config(text = '')
    global value
    value = IntVar(value = 1)
    countlbl.config(textvariable = value)
    mycombo.current('0')

def Op_new():
    if orders_label.cget('text') == '':
        showerror(title = 'Error in ordering' , message = 'No order founded!')
    else:
        win.destroy()


win = Tk()
win.geometry('700x600')
win.minsize('700' , '600')
win.maxsize('700' , '600')
win.title('Restaurant')
win.configure(bg = '#198602' , borderwidth = 10 , highlightthickness = 7 , highlightcolor = '#047313')

formheading = Label(text = 'Restaurant menue And orders' , font = ('b nazanin' , 20) , bg = '#000000' , fg = '#FFFFFF' , width = 500 , height = 1)
formheading.pack()

wrapper = LabelFrame(win , text = 'Menue')
wrapper.pack(padx = 10 , pady = 10 , fill = 'both' , expand = 'yes')
Label(wrapper , text = 'Select item').place(x = 10 , y = 10)

Button(text = 'Exit' , width = 7 , height = 2 , command = sys.exit).place(x = 590 , y = 250)
value = IntVar(value = 1)
minbutton = Button(wrapper , text = '-' , width = 2 , height = 1 , command = lambda: value.set(value.get()-1)).place(x = 540 , y = 30)
countlbl = Label(wrapper , textvariable = value , width = 2 , height = 1)
countlbl.place(x = 570 , y = 30)
sumbutton = Button(wrapper ,text = '+' , width = 2 , height = 1 , command = lambda: value.set(value.get()+1)).place(x = 600 , y = 30)

wrapper2 = LabelFrame(win , text = 'Your order')
wrapper2.pack(padx = 10 , pady= 10 , fill = 'both' , expand = 'yes')
orders_label = Label(wrapper2)
orders_label.place(x = 20 , y = 20)

options = []
opts = StringVar()
mycombo = ttk.Combobox(wrapper , textvariable = opts , width = 75)
con = sql_connection()
cur = sql_cursor(con)
cur.execute("SELECT item_id , item_name , item_time , item_material , item_cost FROM menue")
menue = cur.fetchall()
for i in menue:
    options.append(str(i[0]) + ' - ' + str(i[1]) + ' - ' + str(i[2]) + ' - ' + str(i[3]) + ' - ' + str(i[4]))
mycombo['values'] = options
mycombo.current(0)
mycombo.place(x = 10 , y = 30)

cur.close()
con.close()

Button(text = 'Submit' , width = 7 , height = 2 , command = submit).place(x = 530 , y = 250)
Button(wrapper2 , text = 'Cancel' , width = 7 , height = 2 , command = restart_win).place(x = 580 , y = 180)
Button(wrapper2 , text = 'Order' , width = 7 , height = 2 , command = Op_new).place(x = 520 , y = 180)

win.protocol("WM_DELETE_WINDOW" , close_window)

win.mainloop()

def submitinf():
    con = sql_connection()
    cur = sql_cursor(con)

    sql_querry = "INSERT INTO customer (customer_name , customer_lastname , customer_phonenumber , customer_adress) VALUES (%s,%s,%s,%s)"
    data = ((ent1.get()).capitalize() , (ent2.get()).capitalize() , ent3.get() , ent4.get())

    cur.execute('SELECT customer_name , customer_lastname FROM customer')
    database_data = cur.fetchall()
    database_data = list(database_data)
    
    i = 0
    for j in database_data:
        if ent1.get().capitalize() == database_data[i][0] and ent2.get().capitalize() == database_data[i][1]:
            showerror(title = 'Account Error' , message = 'This account already exist!\nEnter your ID')
            ent1.delete(0 , END)
            ent2.delete(0 , END)
            ent3.delete(0 , END)
            ent4.delete(0 , END)
        else:
            i += 1
    if ent1.get() == '' or ent2.get() == '':
        showerror(title = 'data error' , message = 'Two first field can not be empty')
        ent1.delete(0 , END)
        ent2.delete(0 , END)
        ent3.delete(0 , END)
        ent4.delete(0 , END)
    else:
        cur.execute(sql_querry , data)
        cur.execute("SELECT customer_id FROM customer;")
        id = cur.fetchall()
        id = list(id)
        showinfo('Order' , 'Your order has been successfully placed')
        showinfo('ID' , f'We made an account for you \nYour id is {id[-1]}')

        sql_querry01 = "INSERT INTO orders (orders_time , orders_cost , itemID , customerID) VALUES(%s,%s,%s,%s)"
        data01 = (datetime.now() , cost , str(itemID) , int(str(id[-1][0])))
        cur.execute(sql_querry01 , data01)

        #cur.execute("SELECT itemID FROM orders WHERE orders_id = (SELECT MAX(orders_id FROM orders))")

        con.commit()
        cur.close()
        con.close()
        sys.exit()


win2 = Tk()
win2.geometry('400x300')
win2.minsize('400' , '300')
win2.maxsize('400' , '300')
win2.title('Informations page')
win2.configure(bg = '#198602' , borderwidth = 10 , highlightthickness = 7 , highlightcolor = '#047313')

lbl0 = Label(win2 , text = 'Customers informations' , font = ('b nazanin' , 25) , bg = '#000000' , fg = '#FFFFFF' , width = 500).pack()
lbl1 = Label(win2 , text = 'Name :' , width = 6 , anchor = 'w').place(x = 10 , y = 70)
ent1 = Entry(win2 , width = 25)
ent1.place(x = 135 , y = 70)
lbl2 = Label(win2 , text = 'Last name :' , width = 9 , anchor = 'w').place(x = 10 , y = 100)
ent2 = Entry(win2 , width = 25)
ent2.place(x = 135 , y = 100)
lbl3 = Label(win2 , text = 'Phone Number :' , width = 13 , anchor = 'w').place(x = 10 , y = 130)
ent3 = Entry(win2 , width = 25)
ent3.place(x = 135 , y = 130)
lbl4 = Label(win2 , text = 'Adress :' , width = 6 , anchor = 'w').place(x = 10 , y = 160)
ent4 = Entry(win2 , width = 25)
ent4.place(x = 135 , y = 160)
btn = Button(win2 , text = 'Record' , width = 5 , height = 1 , command = submitinf).place(x = 320 , y = 240)

def recordinf():
    id = ent5.get()
    con = sql_connection()
    cur = sql_cursor(con)
    cur.execute("SELECT * FROM customer WHERE customer_id = %s" , (id,))
    customer_inf = cur.fetchall()
    if not customer_inf:
        showerror(title = 'Data' , message = 'You has not opened an accout \n Open an account')
        ent5.delete(0 , END)
    else:
        showinfo(title = 'Your account' , message = f'{customer_inf}')
        showinfo(title = 'Order' , message = 'Your order has been successfully placed')
        sql_querry00 = "INSERT INTO orders (orders_time , orders_cost , itemID , customerID) VALUES (%s,%s,%s,%s)"
        data00 = (datetime.now() , cost , str(itemID) , int(ent5.get()))
        cur.execute(sql_querry00 , data00)

        con.commit()
        con.close()
        cur.close()
        sys.exit()
    
    cur.close()
    con.close()


win3 = Tk()
win3.geometry('400x300')
win3.minsize('400' , '300')
win3.maxsize('400' , '300')
win3.title('Informations page')
win3.configure(bg = '#198602' , borderwidth = 10 , highlightthickness = 7 , highlightcolor = '#047313')

Label(win3 , text = 'Login Panel' ,  font = ('b nazanin' , 25) , bg = '#000000' , fg = '#FFFFFF' , width = 500).pack()
Label(win3 , text = 'Enter your ID' , font = ('b nazanin' , 15)).place(x = 135 , y = 70)
ent5 = Entry(win3 , width = 5 , justify = 'center')
ent5.place(x = 175 , y = 110)
btn = Button(win3 , text = 'Record' , width = 5 , height = 1 , command = recordinf).place(x = 170 , y = 170)

win2.protocol("WM_DELETE_WINDOW" , close_window)
win3.protocol("WM_DELETE_WINDOW" , close_window)

win2.mainloop()
win3.mainloop()