from tkinter import *
from tkinter import ttk, Frame
from tkinter import messagebox
import pymysql
from datetime import datetime


win = Tk()
win.state('zoomed')
win.configure(bg='powder blue')
win.resizable(width=False, height=False)
win.title('Bank Automation')


icon = PhotoImage(file='icon_bank.png')
win.iconphoto(True, icon)
lbl_title = Label(win, text="BANK AUTOMATION",
                  font=('', 50, 'bold', 'underline'),
                  bg='black',
                  fg='green',
                  relief=RAISED,
                  bd=10,
                  padx=10,
                  pady=7)
lbl_title.pack()

photo = PhotoImage(file="images.png")
lbl_img = Label(win, image=photo)
lbl_img.place(x=0, y=0)


def home_screen(pfrm=None):
    if (pfrm!=None):
        pfrm.destroy()
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0, y=110, relwidth=1, relheight=1)

    lbl_user = Label(frm, text="User ID:", font=('', 20, 'bold'), bg='pink')
    entry_user = Entry(frm, font=('', 15, 'bold'), bd=10)

    lbl_user.place(relx=.30, rely=.09)
    entry_user.place(relx=.42, rely=.09)
    entry_user.focus()

    lbl_password = Label(frm, text="Password:", font=('', 20, 'bold'), bg='pink')
    entry_password = Entry(frm, font=('', 15, 'bold'), bd=10, show='*')

    lbl_password.place(relx=.30, rely=.19)
    entry_password.place(relx=.42, rely=.19)

    lbl_type = Label(frm, text="User Type:", font=('', 20, 'bold'), bg='pink')
    lbl_type.place(relx=.30, rely=.29)
    combo_type = ttk.Combobox(frm, width=13,
                              values=["---Select user---", "Customer", "Admin"],
                              font=('', 20), state='readonly')
    combo_type.current(0)
    combo_type.place(relx=.42, rely=.29)


    login_button = Button(frm,
                          command=lambda: login_screen(pfrm, entry_user, entry_password, combo_type),
                          width=13, text="Login", font=('', 17),
                          bg='powder blue', activebackground='powder blue')
    login_button.place(relx=.335, rely=.385)

    reset_button = Button(frm, command=lambda: reset_home(entry_user, entry_password, combo_type), width=13,
                          text="Reset", font=('', 17), bg='powder blue', activebackground='powder blue')
    reset_button.place(relx=.49, rely=.385)

    open_account_button = Button(frm, command=lambda: open_account_screen(frm), width=13, text="Open Account",
                                 font=('', 17), bg='powder blue', activebackground='powder blue')
    open_account_button.place(relx=.335, rely=.49)

    forget_button = Button(frm, command=lambda: forget_password_screen(frm), width=13, text="Forget Password",
                           font=('', 17), bg='powder blue', activebackground='powder blue')
    forget_button.place(relx=.49, rely=.49)


def logout(pfrm):
    option = messagebox.askyesno(title="logout", message="Do you really want to logout?")
    if (option == True):
        home_screen(pfrm)
    else:
        pass

#-------------------Welcome Screen / Login screen------------------------------
def login_screen(pfrm, entry_user, entry_password, combo_type):

    user = entry_user.get()
    pwd = entry_password.get()
    tp = combo_type.get()
    if(tp=="---Select user---"):
        messagebox.showwarning("Warning", "Please select user type")
        return
    elif(tp=="Customer"):
        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select nam, bal, tp from username where acn = %s and pass = %s", (user, pwd))
        tup = cur.fetchone()
        if(tup==None):
            messagebox.showerror("Fail", "Invalid username/password")
            return
        else:
            frm = Frame(win)
            frm.configure(bg='pink')
            frm.place(x=0, y=110, relwidth=1, relheight=1)

            logout_button = Button(frm, command=lambda: logout(frm), width=7, text="logout", font=('', 15, 'bold'),
                                   bg='powder blue', activebackground='powder blue')
            logout_button.pack(anchor='e')

            left_frm = Frame(frm)
            left_frm.configure(background='pink')
            left_frm.place(x=0, y=0, relwidth=.2, relheight=1)

            Label(frm, text=f"Welcome, {tup[0]}", font=(' ', 15)).pack(padx=0, pady=0, anchor="nw")

            check_button = Button(frm, width=15, command=lambda: checkbal_frame(), text='Check Bal',
                                  font=('', 15, 'bold'),
                                  background='powder blue', activebackground='powder blue')
            check_button.place(relx=.02, rely=.14)

            deposit_button = Button(frm, width=15, command=lambda: deposit_frame(), text='Deposite',
                                    font=('', 15, 'bold'),
                                    background='powder blue', activebackground='powder blue')
            deposit_button.place(relx=.02, rely=.24)

            withdraw_button = Button(frm, width=15, command=lambda: withdraw_frame(), text='Withdraw',
                                     font=('', 15, 'bold'),
                                     background='powder blue', activebackground='powder blue')
            withdraw_button.place(relx=.02, rely=.34)

            transfer_button = Button(frm, width=15, command=lambda: transfer_frame(), text='Transfer',
                                     font=('', 15, 'bold'),
                                     background='powder blue', activebackground='powder blue')
            transfer_button.place(relx=.02, rely=.44)

            transaction_history_button = Button(frm, width=15, command=lambda: transaction_history_frame(),
                                                text='Transaction History', font=('', 15, 'bold'),
                                                background='powder blue',
                                                activebackground='powder blue')
            transaction_history_button.place(relx=.02, rely=.56)
    else:
        if (user == 'admin' and pwd =='admin'):
            frm: Frame = Frame(win)
            frm.configure(bg='pink')
            frm.place(x=0, y=110, relwidth=1, relheight=1)

            logout_button = Button(frm, command=lambda: logout(frm), width=7, text="logout", font=('', 15, 'bold'),
                                   bg='powder blue', activebackground='powder blue')
            logout_button.pack(anchor='e')

            Label(frm, text="Welcome, Admin*", font=(' ', 15)).pack(anchor="nw")

            view_customers_button = Button(frm, width=15, command=lambda: view_customer(), text='View Customers',
                                           font=('', 15, 'bold'),
                                           background='powder blue', activebackground='powder blue')
            view_customers_button.pack(anchor='center')



        else:
            messagebox.showerror("Invalid", "Invalid username/password")
            return


    def view_customer():
        f = Frame(frm)
        f.configure(background='pink')
        f.place(x=300, y=15, relwidth=.6, relheight=.8)

        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select nam, acn, tp, bal, mobile, email from username")
        Label(f, text="Name", font=('', 15, 'bold'), bg='pink').place(x=30, y=10)
        Label(f, text="A/c No", font=('', 15, 'bold'), bg='pink').place(x=130, y=10)
        Label(f, text="Type", font=('', 15, 'bold'), bg='pink').place(x=230, y=10)
        Label(f, text="Bal.", font=('', 15, 'bold'), bg='pink').place(x=330, y=10)
        Label(f, text="Mobile", font=('', 15, 'bold'), bg='pink').place(x=430, y=10)
        Label(f, text="E-mail", font=('', 15, 'bold'), bg='pink').place(x=530, y=10)
        i = 70
        for row in cur:
            Label(f, text=f"{row[0]}", font=('', 12), bg='pink', fg='black').place(x=30, y=i)
            Label(f, text=f"{row[1]}", font=('', 12), bg='pink', fg='black').place(x=130, y=i)
            Label(f, text=f"{row[2]}", font=('', 12), bg='pink', fg='black').place(x=230, y=i)
            Label(f, text=f"{row[3]}", font=('', 12), bg='pink', fg='black').place(x=330, y=i)
            Label(f, text=f"{row[4]}", font=('', 12), bg='pink', fg='black').place(x=430, y=i)
            Label(f, text=f"{row[5]}", font=('', 12), bg='pink', fg='black').place(x=530, y=i)
            i = i + 40


    def checkbal_frame():
        f = Frame(frm)
        f.configure(background='pink')
        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select bal from username where acn = %s", (user,))
        tupp = cur.fetchone()
        bal = float(tupp[0])
        con.close()
        f.place(x=300, y=15, relwidth=.6, relheight=.8)
        lbl_name = Label(f, text=f"Name:\t\t{tup[0]}",
                         foreground='green',
                         font=('', 20, 'bold'),
                         background='pink')
        lbl_bal = Label(f, text=f"Balance:\t\t{bal}",
                        foreground='green',
                        font=('', 20, 'bold'),
                        background='pink')
        lbl_type = Label(f, text=f"Type:\t\t{tup[2]}",
                         foreground='green',
                         font=('', 20, 'bold'),
                         background='pink')
        lbl_acn = Label(f, text=f"A/c No:\t\t{user}",
                        fg='green',
                        bg='pink',
                        font=('', 20, 'bold'))
        lbl_checkbal_title = Label(f, text='Check Balance Page',
                                   font=(' ', 22, 'bold', 'underline'),
                                   bg='pink',
                                   fg='blue')
        lbl_checkbal_title.pack()
        lbl_acn.place(x=140, y=100)
        lbl_name.place(x=140, y=150)
        lbl_bal.place(x=140, y=200)
        lbl_type.place(x=140, y=250)

    def deposit_frame():
        f = Frame(frm)
        f.configure(bg='pink')
        f.place(x=300, y=15, relwidth=.6, relheight=.8)
        lbl_amt = Label(f, text="Amount:", fg='green', font=('', 20, 'bold'), bg='pink')
        entry_amt = Entry(f, font=('', 20, 'bold'), border=10)
        submit_button = Button(f, width=7, text='Submit', font=('', 15, 'bold'), bg='powder blue', bd=10,
                               command=lambda: deposite_db(entry_amt))
        reset_button = Button(f, width=7, text='Reset', font=('', 15, 'bold'), bg='powder blue', bd=10,
                              command=lambda: reset_login2(entry_amt))
        lbl_deposite_title = Label(f, text='Deposite Page', font=(' ', 22, 'bold', 'underline'), bg='pink', fg='blue')
        lbl_deposite_title.pack()
        lbl_amt.place(x=100, y=140)
        entry_amt.place(x=240, y=135)
        submit_button.place(x=210, y=250)
        reset_button.place(x=390, y=250)

    def deposite_db(entry_amt):
        amt = float(entry_amt.get())
        dt = datetime.now()
        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select bal from username where acn = %s", (user,))
        tup = cur.fetchone()
        bal = float(tup[0])
        cur.execute("update username set bal = bal + %s where acn = %s", (amt, user))
        cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)", (user, dt, amt, 'Cr.', bal + amt))
        con.commit()
        messagebox.showinfo("Update", f"{amt} is deposited")
        entry_amt.delete(0, END)
        con.close()



    def withdraw_frame():
        f = Frame(frm)
        f.configure(bg='pink')
        f.place(x=300, y=15, relwidth=.6, relheight=.8)
        lbl_amt = Label(f, text="Amount:", fg='green', font=('', 20, 'bold'), bg='pink')
        entry_amt = Entry(f, font=('', 20, 'bold'), bd=10)
        submit_button = Button(f, width=7, text='Submit', font=('', 15, 'bold'), bg='powder blue', bd=10,
                               command=lambda: withdraw_db(entry_amt))
        reset_button = Button(f, width=7, text='Reset', font=('', 15, 'bold'), bg='powder blue', bd=10,
                              command=lambda: reset_login2(entry_amt))
        lbl_withdraw_frame_title = Label(f, text='Withdraw Page', font=(' ', 22, 'bold', 'underline'), bg='pink',
                                         fg='blue')
        lbl_withdraw_frame_title.pack()
        lbl_amt.place(x=100, y=140)
        entry_amt.place(x=240, y=135)
        submit_button.place(x=210, y=250)
        reset_button.place(x=390, y=250)

    def withdraw_db(entry_amt):
        amt = float(entry_amt.get())
        dt = datetime.now()
        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select bal from username where acn = %s", (user,))
        tup = cur.fetchone()
        bal = float(tup[0])
        if bal < amt:
            messagebox.showinfo('Information', 'Insufficient balance')
        else:
            cur.execute("update username set bal = bal - %s where acn = %s", (amt, user))
            cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)", (user, dt, amt, 'Db.', bal - amt))
            con.commit()
            messagebox.showinfo("Update", f"{amt} is Withdraw")
            entry_amt.delete(0, END)
            con.close()

    def transfer_frame():
        f = Frame(frm)
        f.configure(background='pink')
        f.place(x=300, y=15, relwidth=.6, relheight=.8)
        lbl_amt = Label(f, text="Amount:", fg='green', font=('', 20, 'bold'), bg='pink')
        entry_amt = Entry(f, font=('', 20, 'bold'), bd=10)
        lbl_to = Label(f, text="To A/c No:", fg='green', font=('', 20, 'bold'), bg='pink')
        entry_to = Entry(f, font=('', 20, 'bold'), bd=10)
        submit_button = Button(f, width=7, text='Submit', font=('', 15, 'bold'), bg='powder blue', bd=10,
                               command=lambda: transfer_db(entry_amt, entry_to))
        reset_button = Button(f, width=7, text='Reset', font=('', 15, 'bold'), bg='powder blue', bd=10,
                              command=lambda: reset_login(entry_amt, entry_to))
        lbl_transfer_title = Label(f, text='Amount Transfer Page', font=(' ', 22, 'bold', 'underline'), bg='pink',
                                   fg='blue')
        lbl_transfer_title.pack()
        lbl_amt.place(x=100, y=140)
        entry_amt.place(x=260, y=135)
        lbl_to.place(x=100, y=240)
        entry_to.place(x=260, y=235)
        submit_button.place(x=210, y=350)
        reset_button.place(x=390, y=350)

    def transaction_history_frame():
        f = Frame(frm)
        f.configure(background='pink')
        f.place(x=300, y=15, relwidth=.6, relheight=.8)

        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select * from txnhistory where acn = %s", (user,))
        Label(f, text="Date", font=('', 15, 'bold'), bg='pink').place(x=30, y=10)
        Label(f, text="Amount", font=('', 15, 'bold'), bg='pink').place(x=230, y=10)
        Label(f, text="Trans. Type", font=('', 15, 'bold'), bg='pink').place(x=380, y=10)
        Label(f, text="Update Balance", font=('', 15, 'bold'), bg='pink').place(x=530, y=10)
        i=70
        for row in cur:
            Label(f,text=f"{row[1][:10]}", font=('',12), bg='pink', fg='black').place(x=30, y=i)
            Label(f, text=f"{row[2]}", font=('', 12), bg='pink', fg='black').place(x=230, y=i)
            Label(f, text=f"{row[3]}", font=('', 12), bg='pink', fg='black').place(x=380, y=i)
            Label(f, text=f"{row[4]}", font=('', 12), bg='pink', fg='black').place(x=530, y=i)
            i = i+40

    def transfer_db(entry_amt, entry_to):
        amt = float(entry_amt.get())
        to = entry_to.get()
        dt = str(datetime.now())
        con = pymysql.connect(user='root', password='root', database='bank_automation')
        cur = con.cursor()
        cur.execute("select * from username where acn=%s", (to,))
        cur.execute("select bal from username where acn=%s", (user,))
        tup = cur.fetchone()
        bal8 = int(tup[0])
        if (tup == None):
            messagebox.showerror("fail", "Invalid to account")
            return
        elif bal8 < amt:
            messagebox.showerror("Error", "Insufficient amount")
        else:
            # cur.execute("select bal from username where acn=%s", (user,))
            tup1 = cur.fetchone()
            bal1 = int(tup1[0])

            cur.execute("select bal from username where acn=%s", (to,))
            tup2 = cur.fetchone()
            bal2 = int(tup2[0])

            cur.execute("update username set bal=bal-%s where acn=%s", (amt, user))
            cur.execute("update username set bal=bal+%s where acn=%s", (amt, to))

            cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)", (user, dt, amt, 'Db.', bal1 - amt))
            cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)", (to, dt, amt, 'Cr.', bal2 + amt))

            con.commit()
            messagebox.showinfo("Success", "Amount transfer done..")
            entry_amt.delete(0, END)
            entry_to.delete(0, END)
            con.close()

    if(user!='admin' and pwd!='admin'):
        checkbal_frame()




def forget_password_screen(pfrm):
    pfrm.destroy()
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0, y=110, relwidth=1, relheight=1)

    back_button = Button(frm, command=lambda: home_screen(frm), width=7, text="Back",
                         font=('', 15, 'bold'), bg='powder blue')
    back_button.pack(anchor='w')

    lbl_acn_no = Label(frm, text="A/c No:", fg='green', font=('', 20, 'bold'), bg='pink')
    entry_acn_no = Entry(frm, font=('', 20, 'bold'), border=10)
    lbl_mobile_no = Label(frm, text="Mobile No:", fg='green', font=('', 20, 'bold'), bg='pink')
    entry_mobile_no = Entry(frm, font=('', 20, 'bold'), border=10)
    recover_button = Button(frm, width=7, text='Get', font=('', 15, 'bold'), bg='powder blue', bd=10,
                            command=lambda: recover_pass(frm, entry_acn_no, entry_mobile_no))
    reset_button = Button(frm, width=7, text='Reset', font=('', 15, 'bold'), bg='powder blue', bd=10,
                          command=lambda: reset_forget_pass(entry_acn_no, entry_mobile_no))

    lbl_acn_no.place(x=300, y=190)
    entry_acn_no.place(x=500, y=185)
    lbl_mobile_no.place(x=300, y=270)
    entry_mobile_no.place(x=500, y=265)
    recover_button.place(x=500, y=350)
    reset_button.place(x=700, y=350)


def open_account_screen(pfrm):
    pfrm.destroy()
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(x=0, y=110, relwidth=1, relheight=1)

    back_button = Button(frm, command=lambda: home_screen(frm), width=7, text="Back", font=('', 15, 'bold'),
                         bg='powder blue')
    back_button.pack(anchor='w')


    lbl_name = Label(frm, text="Name:", fg='green', font=('', 20, 'bold'), bg='pink')
    entry_name = Entry(frm, font=('', 20, 'bold'), bd=10)

    lbl_mobile_no = Label(frm, text="Mobile No:", fg='green', font=('', 20, 'bold'), bg='pink')
    entry_mobile_no = Entry(frm, font=('', 20, 'bold'), bd=10)

    lbl_email = Label(frm, text="Email:", fg='green', font=('', 20, 'bold'), bg='pink')
    entry_email = Entry(frm, font=('', 20, 'bold'), bd=10)

    lbl_password = Label(frm, text="Password:", fg='green', font=('', 20, 'bold'), bg='pink')
    entry_password = Entry(frm, font=('', 20, 'bold'), bd=10, show='*')

    lbl_type = Label(frm, text="Type:", fg='green', font=('', 20, 'bold'), bg='pink')
    combo_type = ttk.Combobox(frm, width=13, values=["-------Select-------", "Saving", "Current"], state='readonly',
                              font=('', 20))
    combo_type.current(0)

    submit_button = Button(frm,
                           command=lambda: open_acn_db(frm,
                                                       entry_name,
                                                       entry_mobile_no,
                                                       entry_email,
                                                       entry_password,
                                                       combo_type),
                           width=7, text='Submit', font=('', 15, 'bold'),
                           bg='powder blue', bd=10)
    reset_button = Button(frm, width=7, text='Reset', font=('', 15, 'bold'), bg='powder blue', bd=10,
                          command=lambda: reset_open_acn(entry_name, entry_mobile_no, entry_email, entry_password,
                                                         combo_type))

    lbl_name.place(x=300, y=105)
    entry_name.place(x=550, y=100)

    lbl_mobile_no.place(x=300, y=175)
    entry_mobile_no.place(x=550, y=170)

    lbl_email.place(x=300, y=245)
    entry_email.place(x=550, y=240)

    lbl_password.place(x=300, y=315)
    entry_password.place(x=550, y=310)

    lbl_type.place(x=300, y=380)
    combo_type.place(x=550, y=380)

    submit_button.place(x=516, y=450)
    reset_button.place(x=700, y=450)


def reset_home(entry_user, entry_password, combo_type):
    entry_user.delete(0, END)
    entry_password.delete(0, END)
    combo_type.current(0)
    entry_user.focus()


def reset_login(entry_amt, entry_to):
    entry_amt.delete(0, END)
    entry_to.delete(0, END)
    entry_amt.focus()


def reset_login2(entry_amt):
    entry_amt.delete(0, END)
    entry_amt.focus()


def reset_open_acn(entry_name, entry_mobile_no, entry_email, entry_password, combo_type):
    entry_name.delete(0, END)
    entry_mobile_no.delete(0, END)
    entry_email.delete(0, END)
    entry_password.delete(0, END)
    combo_type.current(0)
    entry_name.focus()


def reset_forget_pass(entry_acn_no, entry_mobile_no):
    entry_acn_no.delete(0, END)
    entry_mobile_no.delete(0, END)

def clear():
    pass


def open_acn_db(pfrm, entry_name, entry_mobile_no, entry_email, entry_password, combo_type):
    con = pymysql.connect(user='root', password='root', database='bank_automation')
    cur = con.cursor()
    cur.execute("select max(acn) from username")
    tup = cur.fetchone()
    acn = tup[0]
    acn = acn + 1
    con.close()

    name = entry_name.get()
    mob = entry_mobile_no.get()
    email = entry_email.get()
    pwd = entry_password.get()
    type = combo_type.get()
    status = 'active'
    bal = 1000

    con = pymysql.connect(user='root', password='root', database='bank_automation')
    cur = con.cursor()
    cur.execute("insert into username values(%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, pwd, email, mob, acn, bal, type, status))
    con.commit()
    con.close()
    messagebox.showinfo("Account Opening", f"Your Account is opened with Acn: {acn}")
    home_screen(pfrm)


def recover_pass(pfrm, entry_acn_no, entry_mobile_no):
    acn = int(entry_acn_no.get())
    mob = entry_mobile_no.get()
    con = pymysql.connect(user='root', password='root', database='bank_automation')
    cur = con.cursor()
    cur.execute("select pass from username where acn = %s and mobile = %s", (acn, mob))
    tup = cur.fetchone()
    if (tup == None):
        messagebox.showwarning("Password", "Invalid Acn/Mob")
        return
    else:
        pwd = tup[0]
        messagebox.showinfo("Password", f"Your Password: {pwd}")
    con.close()
    home_screen(pfrm)




home_screen()
win.mainloop()
