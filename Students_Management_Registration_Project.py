import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk , ImageDraw, ImageFont, ImageOps
from io import BytesIO
import re
import random
import sqlite3
import os
import win32api
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import my_email

root = tk.Tk()
root.geometry("500x600")
root.title("Students Management & Registration System")

bg_color = '#273b7a'

login_stud_icon = tk.PhotoImage(file='Images/login_student_img.png')
login_admin_icon = tk.PhotoImage(file='Images/admin_img.png')
create_account_icon = tk.PhotoImage(file='Images/add_student_img.png')
locked_icon = tk.PhotoImage(file='Images/locked.png')
unlocked_icon = tk.PhotoImage(file='Images/unlocked.png')
add_image = tk.PhotoImage(file='Images/add_image.png')


def init_database():
    if os.path.exists('student_account.db'):
        
     connection = sqlite3.connect('student_account.db')

     cursor = connection.cursor()

     cursor.execute("""
            SELECT * FROM data  
        """)
    
     connection.commit()
     print(cursor.fetchall())
     connection.close()


    else: 
       
       connection = sqlite3.connect('student_account.db')

       cursor = connection.cursor()

       cursor.execute("""
              CREATE TABLE data (
    id_number text ,
    name text ,
    gender text,
    age text,
    phone_number text,
    class text,
    email text,
    password text,   
    image blob
    )      
        """)
    
       connection.commit()
       connection.close()

def check_id_already_exists(id_number):

  connection = sqlite3.connect('student_account.db')

  cursor = connection.cursor()

  cursor.execute(f"""
        SELECT id_number FROM data WHERE id_number == '{id_number}'
 """)
        
  connection.commit()
  response = cursor.fetchall()
  connection.close()

  return response



def check_valid_password(id_number, password):

  connection = sqlite3.connect('student_account.db')

  cursor = connection.cursor()

  cursor.execute(f"""
        SELECT id_number, password FROM data WHERE id_number == '{id_number}' 
        AND password == '{password}'
 """)
        
  connection.commit()
  response = cursor.fetchall()
  connection.close()

  return response


def add_data( id_number,name,gender,age,phone_number,
              student_class,email,password,pic_data):    
       connection = sqlite3.connect('student_account.db')

       cursor = connection.cursor()

       cursor.execute(f"""
           INSERT INTO data VALUES('{id_number}','{name}','{gender}','{age}',
           '{phone_number}','{student_class}','{email}','{password}', ?)
           """, [pic_data])
       
       connection.commit()
       connection.close()

# --------------------------Welcome Page -------------------------------- #

def confirmation_box(massage):

    answer = tk.BooleanVar()
    answer.set(False)

    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()

    confirmation_box_fm = tk.Frame(root, highlightbackground=bg_color,
                                    highlightthickness=3)

    confirmation_box_fm.place(x=100, y=120, width=328, height=228)

    massage_lb = tk.Label(confirmation_box_fm, text=massage , font=('Bold', 15))
    massage_lb.pack(pady=20)

    cancel_btn = tk.Button(confirmation_box_fm, text='Cancel', font=('Bold', 15),
                           bd=0, bg=bg_color, fg='white', command=lambda: action(False))
    cancel_btn.place(x=50, y=160, width=80)

    yes_btn = tk.Button(confirmation_box_fm, text='Yes', font=('Bold', 15),
                           bd=0, bg=bg_color, fg='white', command=lambda: action(True))
    yes_btn.place(x=200, y=160 ,width=80)

    root.wait_window(confirmation_box_fm)
    return answer.get()

def massage_box(massage):
    massage_box_fm = tk.Frame(root ,highlightbackground=bg_color, highlightthickness=3)
    massage_box_fm.place(x=100, y=120, width=320, height=200)

    close_btn = tk.Button(massage_box_fm, text='X', bd=0 ,font=('Bold', 13),
                          fg=bg_color, command=lambda: massage_box_fm.destroy())
    close_btn.place(x=290, y=5)


    massage_lb = tk.Label(massage_box_fm, text=massage, font=('Bold',15))
    massage_lb.pack(pady=50)

def draw_student_card(student_pic_path, student_data):

    labels = """
ID Number:
Name:
Gender:
Age:
Contact:
Class:
Email:
"""

   

    student_card = Image.open('Images/student_card_frame.png')
    pic = Image.open(student_pic_path).resize((100, 100))


    student_card.paste(pic, (15,25))

    drew = ImageDraw.Draw(student_card)
    
    heading_font = ImageFont.truetype('bahnschrift', 18)
    Labels_font = ImageFont.truetype('arial', 15)
    data_font = ImageFont.truetype('bahnschrift', 13)


    drew.text(xy=(150,60), text='Student Card', fill=(0, 0, 0),
              
              font=heading_font )
    
    drew.multiline_text(xy=(15, 120), text=labels, fill=(0, 0, 0), 
                        font=Labels_font, spacing=6)
    
    drew.multiline_text(xy=(95, 120), text=student_data, fill=(0, 0, 0), 
                        font=data_font, spacing=10)

    return student_card
    

def student_card_page(student_card_obj):

    def save_student_card():
        path = askdirectory()

        if path:
            print(path)

            student_card_obj.save(f'{path}/student_card.png')

    def print_student_card():
        path = askdirectory()

        if path:
            print(path)

            student_card_obj.save(f'{path}/student_card.png')

            win32api.ShellExecute(0, 'print', f'{path}/student_card.png',
                                  None, '.', 0)


    def close_page():
        student_card_page_fm.destroy()
        root.update()
        student_login_page()

    student_card_img = ImageTk.PhotoImage(student_card_obj)

    student_card_page_fm = tk.Frame(root,highlightbackground=bg_color,
                                    highlightthickness=3)

    heading_lb = tk.Label(student_card_page_fm, text='Student Card',
                          bg=bg_color, fg='white', font=('bold', 16),)

    heading_lb.place(x=0, y=0, width=400)

    close_btn = tk.Button(student_card_page_fm, text='X', bg=bg_color,
                         fg='white', font=('Bold', 13), bd=0,
                         command=close_page)
    close_btn.place(x=370, y=0)


    student_card_lb = tk.Label(student_card_page_fm, image=student_card_img)
    student_card_lb.place(x=50, y=56)

    student_card_lb.image = student_card_img

    save_student_card_btn = tk.Button(student_card_page_fm, text= "Save Student Card",
                                      bg= bg_color, fg='white', font=('Bold',15),
                                      bd=1, command=save_student_card)
    save_student_card_btn.place(x=80, y=375)

    print_student_card_btn = tk.Button(student_card_page_fm, text= "🖨",
                                      bg= bg_color, fg='white', font=('Bold',15),
                                      bd=1, command=print_student_card)
    print_student_card_btn.place(x=275, y=375)

    student_card_page_fm.place(x=50, y=30, width=400, height=450)

def welcome_page():

    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_Login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()
    
    def forward_to_create_account_page():
        welcome_page_fm.destroy()
        root.update()
        create_account_page()

    welcome_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                highlightthickness=3)

    # --------------------------Label Header-------------------------------- #

    heading_lb = tk.Label(welcome_page_fm, 
                        text='Welcome To Student Registreration\n&& Managment System',
                        bg=bg_color, fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=480)

    # --------------------------Label Header-------------------------------- #

    # --------------------------Buttons and Icons---------------------------- #

    student_login_btn = tk.Button(welcome_page_fm, text='Login Student', bg=bg_color,
                                fg='white', font=('Bold',18), bd=0, command=forward_to_student_login_page)
    student_login_btn.place(x=120, y=125, width=200)

    student_login_img = tk.Button(welcome_page_fm, image=login_stud_icon, bd=0, command=forward_to_student_login_page)
    student_login_img.place(x=60, y=100)


    Admin_Login_btn = tk.Button(welcome_page_fm, text='Login Admin', bg=bg_color,
                                fg='white', font=('Bold',18), bd=0, command=forward_to_admin_Login_page)
    Admin_Login_btn.place(x=120, y=225, width=200)

    Admin_Login_img = tk.Button(welcome_page_fm, image=login_admin_icon, bd=0, command=forward_to_admin_Login_page)
    Admin_Login_img.place(x=60, y=200)


    create_account_btn = tk.Button(welcome_page_fm, text='  Create Account', bg=bg_color,
                                fg='white', font=('Bold',18), bd=0, command=forward_to_create_account_page)
    create_account_btn.place(x=120, y=325, width=200)

    create_account_img = tk.Button(welcome_page_fm, image=create_account_icon, bd=0 , command=forward_to_create_account_page)
    create_account_img.place(x=60, y=300)

# --------------------------Buttons and Icons---------------------------- #

    welcome_page_fm.pack(pady= 30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=480 , height=420) 

# --------------------------Welcome Page -------------------------------- #

# ------------------------Forget Password Page----------------------------------------- #


def sendmail_to_student(email, massage, subject):

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = my_email.email_address
    password = my_email.password

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = email

    msg.attach(MIMEText(
        _text=massage, _subtype='html'
    ))
    smtp_connection = smtplib.SMTP(host=smtp_server, port=smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username, password=password)

    smtp_connection.sendmail(from_addr=username, to_addrs=email,
                              msg=msg.as_string())
    
    print('Mail Sent Successful')

def forget_password_page():

    def recover_password():
        if check_id_already_exists(id_number=student_id_ent.get()):

            connection = sqlite3.connect('student_account.db')
            cursor = connection.cursor()

            cursor.execute(f"""
            SELECT password FROM data WHERE id_number == '{student_id_ent.get()}'
            """)

            connection.commit()
            recover_password = cursor.fetchall()[0][0]
            print(recover_password)
          
            cursor.execute(f"""
            SELECT email FROM data WHERE id_number == '{student_id_ent.get()}'
            """)

            connection.commit()
            student_email = cursor.fetchall()[0][0]
            connection.close()

            confirmation = confirmation_box(massage=f"""We will Send\nYour Forget Password
Via Your Email Address
{student_email}
Do you Want To Continue?""")

        if confirmation:
           
           msg = f"""<h1>Your Forgot Password is</h1>
           <h2>{recover_password}</h2>
           <p>Once Remember Your Password, After Delete This Messages.</p>"""

           sendmail_to_student(email=student_email, massage=msg,
                               subject='Password Recovery')

        else:
            print('Incorect ID')
            massage_box(massage='invalid ID Number')
     
    forget_password_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                       highlightthickness=3)
    
    forget_password_page_fm.place(x=75, y=120, width=350, height=250)

    heading_lb = tk.Label(forget_password_page_fm, text='⚠ Fogetting Password?',
                          font=('Bold', 13), bg=bg_color, fg='white')
    heading_lb.place(x=0,y=0, width=350)

    close_btn = tk.Button(forget_password_page_fm, text='X', bd=0 ,font=('Bold', 10),
                          bg=bg_color, fg='white',command=lambda: forget_password_page_fm.destroy())
    close_btn.place(x=320, y=0)

    student_id_lb = tk.Label(forget_password_page_fm, text='Enter Student ID Number:',
                             font=('Bold', 13))
    
    student_id_lb.place(x=70, y=40)

    student_id_ent = tk.Entry(forget_password_page_fm,
                              font=('Bold', 15), justify=tk.CENTER)
    
    student_id_ent.place(x=70, y=70, width=180)

    info_lb = tk.Label(forget_password_page_fm, text="""Via Your Email Address
We will Send to you
Your Forgot Password """, justify=tk.LEFT)

    info_lb.place(x=75, y=110)

    next_btn = tk.Button(forget_password_page_fm, text='Next',
                         font=('Bold', 13), bg=bg_color,
                         fg='white', command=recover_password)

    next_btn.place(x=130, y=200, width=80)

def fetch_student_data(query):

    connection = sqlite3.connect('student_account.db')
    cursor = connection.cursor()

    cursor.execute(query)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response

# --------------------------- Student Dashboard Page ---------------------------- #

def student_dashboard(student_id):

    get_student_details = fetch_student_data(f"""
    SELECT name, gender, age ,phone_number ,class ,email FROM data WHERE id_number == {student_id}
""")
    
    get_student_pic = fetch_student_data(f"""
    SELECT image FROM data WHERE id_number == {student_id}
""")
    
    student_pic = BytesIO(get_student_pic[0][0])

    def logout():

        conform = confirmation_box(massage="Do You Want to\n Logout Your Account?")
        if conform:
            dashboard_fm.destroy()
            welcome_page()
            root.update()

    class_list = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th']

    def switch(indicator, page):
        home_btn_indicator.config(bg='#c3c3c3')
        student_card_btn_indicator.config(bg='#c3c3c3')
        security_btn_indicator.config(bg='#c3c3c3')
        edit_data_btn_indicator.config(bg='#c3c3c3')
        delete_account_btn_indicator.config(bg='#c3c3c3')

        indicator.config(bg=bg_color)

        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()

        page()

    dashboard_fm = tk.Frame(root, highlightbackground=bg_color,
                            highlightthickness=3)
    

    options_fm = tk.Frame(dashboard_fm, highlightbackground=bg_color,
                            highlightthickness=2, bg='#c3c3c3')


    home_btn = tk.Button(options_fm, text='Home', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                         command=lambda:switch(indicator=home_btn_indicator, page=home_page))
    home_btn.place(x=10, y=50)

    home_btn_indicator = tk.Label(options_fm, bg=bg_color)
    home_btn_indicator.place(x=5, y=48, width=3, height=40)

    student_card_btn = tk.Button(options_fm, text='Student\nCard', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                         command=lambda:switch(indicator=student_card_btn_indicator,
                         page=dashboard_student_card_page))
    student_card_btn.place(x=10, y=100)

    student_card_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    student_card_btn_indicator.place(x=5, y=110, width=3, height=40)

    security_btn = tk.Button(options_fm, text='Security', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                         command=lambda:switch(indicator=security_btn_indicator,
                                               page=security_page))
    security_btn.place(x=10, y=170)

    security_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    security_btn_indicator.place(x=5, y=170, width=3, height=40)

    edit_data_btn = tk.Button(options_fm, text='Edit Data', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, command=lambda:switch(indicator=edit_data_btn_indicator,
                                                page=edit_data_page))
    edit_data_btn.place(x=10, y=220)

    edit_data_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    edit_data_btn_indicator.place(x=5, y=220, width=3, height=40)

    delete_account_btn = tk.Button(options_fm, text='Delete\nAccount', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT, command=lambda:switch(indicator=delete_account_btn_indicator,
                            page=delete_account_page))
    delete_account_btn.place(x=10, y=270)
 
    delete_account_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    delete_account_btn_indicator.place(x=5, y=280, width=3, height=40)

    logout_btn = tk.Button(options_fm, text='Logout', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0,
                         command=logout)
    logout_btn.place(x=10, y=340)


    options_fm.place(x=0, y=0, width=120, height=575)

    def home_page():

        student_pic_image_obj = Image.open(student_pic)
        size = 100
        mask = Image.new(mode='L', size=(size, size))

        draw_circle = ImageDraw.Draw(im=mask)
        draw_circle.ellipse(xy=(0, 0, size, size), fill=250, outline=True)

        output = ImageOps.fit(image=student_pic_image_obj, size=mask.size,
                              centering=(1, 1))

        output.putalpha(mask)

        
        student_picture = ImageTk.PhotoImage(output)
      
        home_page_fm = tk.Frame(pages_fm)

        student_pic_lb = tk.Label(home_page_fm, image=student_picture)
        student_pic_lb.image = student_picture
        student_pic_lb.place(x=10, y=10)

        hi_lb = tk.Label(home_page_fm, text=f'Welcome: {get_student_details[0][0]}',
                         font=('Bold', 15))
        hi_lb.place(x=130, y=50)

        student_details = f"""
Student ID: {student_id}\n        
Name: {get_student_details[0][0]}\n
Gender: {get_student_details[0][1]}\n
Age: {get_student_details[0][2]}\n
Contact: {get_student_details[0][3]}\n
Class: {get_student_details[0][4]}\n
Email: {get_student_details[0][5]}
"""

        student_details_lb = tk.Label(home_page_fm, text=student_details,
                                      font=('Bold', 13), justify=tk.LEFT)

        student_details_lb.place(x=20, y=130)

        home_page_fm.pack(fill=tk.BOTH, expand=True)

    def dashboard_student_card_page():

        student_details = f"""
{student_id}
{get_student_details[0][0]}
{get_student_details[0][1]}
{get_student_details[0][2]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
"""

      

        student_card_image_obj = draw_student_card(student_pic_path=student_pic,
                                                   student_data=student_details)

        def save_student_card():
            path = askdirectory()

            if path:
                print(path)

                student_card_image_obj.save(f'{path}/student_card.png')

        def print_student_card():
            path = askdirectory()

            if path:
                print(path)

                student_card_image_obj.save(f'{path}/student_card.png')

                win32api.ShellExecute(0, 'print', f'{path}/student_card.png',
                                      None, '.', 0)


        student_card_img = ImageTk.PhotoImage(student_card_image_obj)

        student_card_page_fm = tk.Frame(pages_fm)


        student_card_page_fm = tk.Frame(pages_fm)

        card_lb = tk.Label(student_card_page_fm, image=student_card_img)
        card_lb.image = student_card_img
        card_lb.place(x=20, y=50)


        save_student_card_btn = tk.Button(student_card_page_fm, text='Save Student Card',
                                          font=('Bold', 15),bd=1, fg='white', 
                                          bg=bg_color, command=save_student_card)
        save_student_card_btn.place(x=40, y=400)

        print_student_card_btn = tk.Button(student_card_page_fm, text='🖨',
                                          font=('Bold', 15), bd=1, fg='white', 
                                          bg=bg_color, command=print_student_card)
        print_student_card_btn.place(x=240, y=400)

        student_card_page_fm.pack(fill=tk.BOTH, expand=True)

    def security_page():

        def show_hide_password():
            if current_password_ent['show'] == '*':
                current_password_ent.config(show='')
                show_hide_btn.config(image=unlocked_icon)

            else:
                current_password_ent.config(show='*')
                show_hide_btn.config(image=locked_icon)

        def set_password():
            if new_password_ent.get() != '':
            
                confirm = confirmation_box(massage='Do You Want to Change\n Your Password?') 

                if confirm:
                    connection = sqlite3.connect('student_account.db')

                    cursor = connection.cursor()
                    cursor.execute(f"""UPDATE data SET password = '{new_password_ent.get()}'
                                   WHERE id_number == '{student_id}' """)

                    connection.commit()
                    connection.close()

                    massage_box(massage='Password Changed Successfully!')

                    current_password_ent.config(state=tk.NORMAL)
                    current_password_ent.delete(0, tk.END)
                    current_password_ent.insert(0, new_password_ent.get())
                    current_password_ent.config(state='readonly')

                    new_password_ent.delete(0, tk.END)


            else:
                massage_box(massage='Enter New Password Required!')

        security_page_fm = tk.Frame(pages_fm)

        current_password_lb = tk.Label(security_page_fm, text='Your Current Password',
                                        font=('Bold', 12))

        current_password_lb.place(x=80, y=30)

        current_password_ent = tk.Entry(security_page_fm, font=('Bold', 15),
                                       justify=tk.CENTER ,show='*')
        
        current_password_ent.place(x=50, y=80)

        student_current_password = fetch_student_data(f"SELECT password FROM data WHERE id_number == {student_id}")

        current_password_ent.insert(tk.END, student_current_password[0][0])
        current_password_ent.config(state='readonly')

        show_hide_btn = tk.Button(security_page_fm, image=locked_icon, 
                                bd=0, command=show_hide_password)
        show_hide_btn.place(x=280 , y= 70)

        change_password_lb = tk.Label(security_page_fm, text='Change Password',
                                        font=('Bold', 12), bg="red", fg='white')
        change_password_lb.place(x=30, y=210, width=290)

        new_password_lb = tk.Label(security_page_fm, text='Set New Password',   
                                        font=('Bold', 12))
        new_password_lb.place(x=100, y=280)

        new_password_ent = tk.Entry(security_page_fm, font=('Bold', 15),
                                        justify=tk.CENTER)
        new_password_ent.place(x=60, y=330)
        
        change__password_btn = tk.Button(security_page_fm, text='Change Password',
                                        font=('Bold', 15), bg=bg_color, fg='white',
                                        command=set_password) 
        change__password_btn.place(x=90, y=380)                                

        security_page_fm.pack(fill=tk.BOTH, expand=True)
    
    def edit_data_page():
        edit_data_page_fm = tk.Frame(pages_fm)

        pic_path = tk.StringVar()
        pic_path.set('')

        def open_pic():
            path = askopenfilename()
        
            if path:
                img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
                pic_path.set(path)

                add_pic_btn.config(image=img)
                add_pic_btn.image = img

        def remove_highlight_warning(entry):
            if entry['highlightbackground'] != 'gray':
                if entry.get() != '':
                    entry.config(highlightcolor =bg_color,
                                highlightbackground= 'gray')

        def verify_email(Email):

            pattern ="^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

            match = re.match(pattern=pattern, string=Email)

            return match


        def check_inputs():
            nonlocal get_student_details, get_student_pic, student_pic
            
            if student_name_ent.get() == '':
                student_name_ent.config(highlightcolor='red',
                                        highlightbackground='red')
                student_name_ent.focus()
                massage_box(massage='Student Full Name \nis Required!')

            elif student_age_ent.get() == '':
                student_age_ent.config(highlightcolor='red',
                                        highlightbackground='red')
                student_age_ent.focus()
                massage_box(massage='Student Age is Required!')

            elif student_contact_ent.get() == '':
                student_contact_ent.config(highlightcolor='red',
                                        highlightbackground='red')
                student_contact_ent.focus()
                massage_box(massage='Student Contact Phone Number \nis Required!')

            elif student_email_ent.get() == '':
                student_email_ent.config(highlightcolor='red',
                                        highlightbackground='red')
                student_email_ent.focus()
                massage_box(massage='Student Email Address \n is Required!')

            elif not verify_email(Email=student_email_ent.get().lower()):
                student_email_ent.config(highlightcolor='red',
                                        highlightbackground='red')
                student_email_ent.focus()
                massage_box(massage='Please Enter a Valid \nEmail Address!')

            else:

                if pic_path.get() != '':
                    new_student__picture = Image.open(pic_path.get()).resize((100, 100))
                    new_student__picture.save("temp_pic.png")

                    with open("temp_pic.png", 'rb') as read_new_pic:
                        new_picture_binary = read_new_pic.read()
                        read_new_pic.close()
                    
                    connection = sqlite3.connect('student_account.db')
                    cursor = connection.cursor()

                    cursor.execute(f""" UPDATE data SET image=? WHERE id_number == '{student_id}' 
                    """, [new_picture_binary])
                    
                    connection.commit()
                    connection.close()
                    
                    massage_box(massage='Data Updated Successfully!')

                name = student_name_ent.get()
                age = student_age_ent.get()
                selected_class = select_class_btn.get()
                contact_number = student_contact_ent.get()
                email_address = student_email_ent.get()

                connection = sqlite3.connect('student_account.db')
                cursor = connection.cursor()

                cursor.execute(f"""
                UPDATE data SET name = '{name}', age = '{age}', phone_number = '{contact_number}',
                class = '{selected_class}', email = '{email_address}' 
                WHERE id_number == '{student_id}'
                """)

                connection.commit()
                connection.close()

                get_student_details = fetch_student_data(f"""
                SELECT name, gender, age ,phone_number ,class ,email FROM data WHERE id_number == {student_id}
                """)
                    
                get_student_pic = fetch_student_data(f"""
                SELECT image FROM data WHERE id_number == {student_id}
                """)

                student_pic = BytesIO(get_student_pic[0][0])
                    
                massage_box(massage='Data Updated Successfully!')

        

        student_current_pic = ImageTk.PhotoImage(Image.open(student_pic))
        


        add_pic_section_fm = tk.Frame(edit_data_page_fm, highlightbackground=bg_color,
                                        highlightthickness=2)

        add_pic_btn = tk.Button(add_pic_section_fm, image=student_current_pic, 
                                bd=0, command=open_pic)

        add_pic_btn.image = student_current_pic
        add_pic_btn.pack()

        add_pic_section_fm.place(x=5, y=5, width=105, height=105)

        student_name_lb = tk.Label(edit_data_page_fm, text="Student Full Name:",font=('Bold', 12))

        student_name_lb.place(x= 5, y=130)

        student_name_ent = tk.Entry(edit_data_page_fm, font=('Bold', 14),
                                    highlightcolor=bg_color, highlightbackground='gray',
                                    highlightthickness=2)
        student_name_ent.place(x=5, y=160, width=200)
        student_name_ent.bind('<KeyRelease>',
                            lambda e: remove_highlight_warning(entry=student_name_ent))


        student_name_ent.insert(tk.END, get_student_details[0][0])


        student_age_lb = tk.Label(edit_data_page_fm, text="Student Age:",
                                font=('Bold', 12))
        student_age_lb.place(x=5, y=210)

        student_age_ent = tk.Entry(edit_data_page_fm, font=('Bold', 14),
                                    highlightcolor=bg_color, highlightbackground='gray',
                                    highlightthickness=2)
        student_age_ent.place(x=5, y=235, width=200)

        student_age_ent.bind('<KeyRelease>',
                            lambda e: remove_highlight_warning(entry=student_age_ent))
        
        student_age_ent.insert(tk.END, get_student_details[0][2])

        student_contact_lb = tk.Label(edit_data_page_fm, text="Contact Phone Number:",
                            font=('Bold', 12))
        student_contact_lb.place(x=5, y=285)

        student_contact_ent = tk.Entry(edit_data_page_fm, font=('Bold', 14),
                                    highlightcolor=bg_color, highlightbackground='gray',
                                    highlightthickness=2)
        student_contact_ent.place(x=5, y=310, width=200)

        student_contact_ent.bind('<KeyRelease>',
                            lambda e: remove_highlight_warning(entry=student_contact_ent))
        
        student_contact_ent.insert(tk.END, get_student_details[0][3])

        student_class_lb = tk.Label(edit_data_page_fm, text="Student Class:",
                            font=('Bold', 12))  
        student_class_lb.place(x=5, y=360)

        select_class_btn = Combobox(edit_data_page_fm, font=('Bold', 15),
                                    state='randomly', values=class_list)
        select_class_btn.place(x=5 ,y=385, width=180, height=30)

        select_class_btn.set(get_student_details[0][4])

        student_email_lb = tk.Label(edit_data_page_fm, text="Student Email Address:",
                            font=('Bold', 12))
        student_email_lb.place(x=5, y=425)

        student_email_ent = tk.Entry(edit_data_page_fm, font=('Bold', 14),
                                    highlightcolor=bg_color, highlightbackground='gray',
                                    highlightthickness=2)
        student_email_ent.place(x=5, y=460, width=200)
        student_email_ent.bind('<KeyRelease>',
                              lambda e: remove_highlight_warning(entry=student_email_ent))

        student_email_ent.insert(tk.END, get_student_details[0][5])

        update_data_btn = tk.Button(edit_data_page_fm, text='Update Data',
                                    font=('Bold', 15), bg=bg_color, fg='white',
                                    command=check_inputs)
        update_data_btn.place(x=215, y=470)


        edit_data_page_fm.pack(fill=tk.BOTH, expand=True)


    def delete_account_page():

        def confirm_delete_account():
            confirm = confirmation_box(massage='⚠ Are You Sure\nYou Want to Delete\nYour Account?')

            if confirm:
                connection = sqlite3.connect('student_account.db')
                cursor = connection.cursor()

                cursor.execute(f"""
                DELETE FROM data WHERE id_number == '{student_id}'
                """)

                connection.commit()
                connection.close()


                delete_account_page_fm.destroy()
                welcome_page()
                root.update()
                massage_box(massage='Account Deleted Successfully!')

            

        delete_account_page_fm = tk.Frame(pages_fm)

        delete_account_lb = tk.Label(delete_account_page_fm, text='⚠ Delete Account',
                                    bg='red', fg='white', font=('Bold', 15))

        delete_account_lb.place(x=30, y=100, width=290)

        delete_account_button = tk.Button(delete_account_page_fm,
                                            text='DELETE Account',
                                            bg="red", fg='white', font=('Bold', 13),
                                            command=confirm_delete_account)

        delete_account_button.place(x=110, y=200)

        delete_account_page_fm.pack(fill=tk.BOTH, expand=True)
      

    pages_fm = tk.Frame(dashboard_fm)
    pages_fm.place(x=122, y=5, width=350, height=550)
    home_page()

    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.config(width=480, height=580)






# -------------------------- Student Login Page  -------------------------------- #

def student_login_page():
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_Welcome_Page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()


    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'gray':
            if entry.get() != '':
                entry.config(highlightcolor =bg_color,
                        highlightbackground= 'gray')


    def  login_account():
        verify_id_number = check_id_already_exists(id_number=id_number_ent.get())
        
        if verify_id_number:
            print('ID is Correct.')

            verify_password = check_valid_password(id_number=id_number_ent.get(),
                                                   password=password_ent.get())

            if verify_password:
                id_number = id_number_ent.get()
                student_login_page_fm.destroy()
                student_dashboard(student_id=id_number)
                root.update()
            

            else:
                print('OOPS!!, Password is Incorrect.')

            password_ent.config(highlightcolor ='red',
                            highlightbackground= 'red')
            
            massage_box(massage='Please Enter \nValid Student Password!')
            
        else:
            print('OOPS!!, ID is Incorrect.')
            id_number_ent.config(highlightcolor ='red',
                            highlightbackground= 'red')
            
            massage_box(massage='Please Enter \n Valid Student_ID!')

 
 
    # ----------------------------------------------------------------------- #
    student_login_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                highlightthickness=3)
    

    heading_lb = tk.Label(student_login_page_fm, text="Student Login Page", bg=bg_color,
                        fg='white', font=('Bold', 18))

    heading_lb.place(x=0, y=0, width=480)
    # -----------------------------------Creating Back button--------------------------- #
    back_btn = tk.Button(student_login_page_fm, text='←', font=('Bold', 20), 
                         fg=bg_color, bd=0 , command=forward_to_Welcome_Page)
    back_btn.place(x=5, y=40)
    # -----------------------------------Creating Back button--------------------------- #

    stud_icon_lb = tk.Label(student_login_page_fm, image=login_stud_icon)
    stud_icon_lb.place(x=200, y=40)

    id_number_lb = tk.Label(student_login_page_fm, text='Enter Student ID Number: ',
                            font=('Bold',18), fg=bg_color)
    id_number_lb.place(x=110,y=140)

    id_number_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), 
                            fg='black', justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2)
    id_number_ent.place(x=110, y= 190,  width= 250)
    id_number_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=id_number_ent))
    

    password_lb = tk.Label(student_login_page_fm, text='Enter Student Password: ',
                            font=('Bold',18), fg=bg_color)
    password_lb.place(x=110,y=240)

    password_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), 
                            fg='black', justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2, show='*')
    password_ent.place(x=110, y= 290, width= 250)
    password_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=password_ent))


    show_hide_btn = tk.Button(student_login_page_fm, image=locked_icon, 
                            bd=0 , command=show_hide_password)
    show_hide_btn.place(x=360 , y=280 )


    login_btn = tk.Button(student_login_page_fm, text='Login', 
                        font=('Bold', 15), bg=bg_color, fg='White',
                        command=login_account)
    login_btn.place(x=130, y= 350, width=200 , height= 40)

    forget_password_btn = tk.Button(student_login_page_fm, text='⚠Forget Password?'
                                    ,fg=bg_color, bd=0, command=forget_password_page)
    forget_password_btn.place(x=175, y=400)

    student_login_page_fm.pack(pady= 30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=480 , height=450)

# --------------------------Student Login Page  -------------------------------- #

# --------------------------Admin Dashboard Page  -------------------------------- #

def admin_dashboard():


    def switch(indicator):

        home_btn_indicator.config(bg='#c3c3c3')
        find_student_btn_indicator.config(bg='#c3c3c3')
        announcement_btn_indicator.config(bg='#c3c3c3')

        indicator.config(bg=bg_color)




    dashboard_fm = tk.Frame(root, highlightbackground=bg_color,
                            highlightthickness=3)

    option_fm = tk.Frame(dashboard_fm, highlightbackground=bg_color,    
                        highlightthickness=2, bg='#c3c3c3')

    home_btn = tk.Button(option_fm, text='Home', font=('Bold', 15),
                            fg=bg_color, bg='#c3c3c3', bd=0,
                            command=lambda: switch(indicator=home_btn_indicator))
    home_btn.place(x=10, y=50)

    home_btn_indicator = tk.Label(option_fm, bg=bg_color)
    home_btn_indicator.place(x=5, y=48, width=3, height=40)

    find_student_btn = tk.Button(option_fm, text='Find\nStudent', font=('Bold', 15),
                            fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                            command=lambda: switch(indicator=find_student_btn_indicator))
    find_student_btn.place(x=10, y=100)

    find_student_btn_indicator = tk.Label(option_fm, bg='#c3c3c3')
    find_student_btn_indicator.place(x=5, y=110, width=3, height=40)

    announcement_btn = tk.Button(option_fm, text='Announce\n-Ment📢', font=('Bold', 15),
                            fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                            command=lambda: switch(indicator=announcement_btn_indicator))
    announcement_btn.place(x=10, y=170)

    announcement_btn_indicator = tk.Label(option_fm, bg='#c3c3c3')
    announcement_btn_indicator.place(x=5, y=180, width=3, height=40)

    logout_btn = tk.Button(option_fm, text='Logout', font=('Bold', 15),
                            fg=bg_color, bg='#c3c3c3', bd=0)
    logout_btn.place(x=10, y=240)


    option_fm.place(x=0, y=0, width=120, height=575)

    page_fm = tk.Frame(dashboard_fm)
    page_fm.place(x=122, y=5, width=350, height=550)


    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.config(width=480, height=580)


# --------------------------Admin Login Page  -------------------------------- #
def admin_login_page():
    def show_hide_password():
            if password_ent['show'] == '*':
                password_ent.config(show='')
                show_hide_btn.config(image=unlocked_icon)

            else:
                password_ent.config(show='*')
                show_hide_btn.config(image=locked_icon)

    def forward_to_Welcome_Page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    def login_account():
        if Admin_User_Name_ent.get() == 'admin':
        
            if password_ent.get() == 'admin':
                admin_login_page_fm.destroy()
                root.update()
                admin_dashboard()

            else:
                massage_box(massage='Wrong Password')

        else:
            massage_box(massage='Wrong Username')


    admin_login_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                    highlightthickness=3)



    heading_lb = tk.Label(admin_login_page_fm, text='Admin Login Page',
                        font=('Bold', 18), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=480)

  # -----------------------------------Creating Back button--------------------------- #
    back_btn = tk.Button(admin_login_page_fm, text='←', font=('Bold', 20), 
                         fg=bg_color, bd=0 , command=forward_to_Welcome_Page)
    back_btn.place(x=5, y=40)
    # -----------------------------------Creating Back button--------------------------- #


    admin_icon_lb = tk.Label(admin_login_page_fm, image=login_admin_icon)
    admin_icon_lb.place(x=200, y=40)


    Admin_User_Name_lb = tk.Label(admin_login_page_fm, text='Enter Admin User Name: ',
                            font=('Bold',18), fg=bg_color)
    Admin_User_Name_lb.place(x=110,y=140)

    Admin_User_Name_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15), 
                            fg='black', justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2)
    Admin_User_Name_ent.place(x=110, y= 190,  width= 250)


    password_lb = tk.Label(admin_login_page_fm, text='Enter Admin Password: ',
                            font=('Bold',18), fg=bg_color)
    password_lb.place(x=110,y=240)

    password_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15), 
                            fg='black', justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2, show='*')
    password_ent.place(x=110, y= 290, width= 250)

    show_hide_btn = tk.Button(admin_login_page_fm, image=locked_icon, 
                                bd=0 , command=show_hide_password)
    show_hide_btn.place(x=360 , y=280 )

    login_btn = tk.Button(admin_login_page_fm, text='Login', 
                            font=('Bold', 15), bg=bg_color, fg='White', command=login_account)
    login_btn.place(x=130, y= 350, width=200 , height= 40)
    
    

    forget_password_btn = tk.Button(admin_login_page_fm, text='⚠Forget Password?'
                                        ,fg=bg_color, bd=0)
    forget_password_btn.place(x=175, y=400)


    admin_login_page_fm.pack(pady= 30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=480 , height=430)



def create_account_page():
    pic_path = tk.StringVar()
    pic_path.set('')

    def open_pic():
        path = askopenfilename()
    
        if path:
    
            img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
            pic_path.set(path)

            add_pic_btn.config(image=img)
            add_pic_btn.image = img

    def forward_to_welcome_page():

        ans = confirmation_box(massage='Do you want to leave \nRegistration Form?')
        
        if ans:

            create_account_page_fm.destroy()
            root.update()
            welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'gray':
            if entry.get() != '':
                entry.config(highlightcolor =bg_color,
                            highlightbackground= 'gray')


    def verify_email(Email):

        pattern ="^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

        match = re.match(pattern=pattern, string=Email)

        return match


    def generate_id_number():
        generated_id = ''

        for r in range(6):
            generated_id += str(random.randint(0, 9))

            if not check_id_already_exists(id_number=generated_id):


             print('ID Number:', generated_id)
            
            student_id.config(state=tk.NORMAL)
            student_id.delete(0, tk.END)
            student_id.insert(0, generated_id)  
            student_id.config(state='readonly')

      
    def check_input_validation():
        if student_name_ent.get() == '':
            student_name_ent.config(highlightcolor='red',
                                    highlightbackground='red' )
            student_name_ent.focus()
            massage_box(massage='Student Full Name is Required.')
        elif student_age_ent.get() == '':
             student_age_ent.config(highlightcolor='red',
                                    highlightbackground='red' )
             student_age_ent.focus()
             massage_box(massage='Student Age is Required.')
 
        elif student_contact_ent.get() == '':
             student_contact_ent.config(highlightcolor='red',
                                    highlightbackground='red' )
             student_contact_ent.focus()
             massage_box(massage='Student Contact Phone is Required.')
        elif select_class_btn.get()== '':
             
             select_class_btn.focus()
             massage_box(massage='Select Student Class is Required.')

        elif student_email_ent.get()== '':
             student_email_ent.config(highlightcolor='red',
                                    highlightbackground='red' )
             student_email_ent.focus()
             massage_box(massage='Student Email Address is Required.')
 
        elif not verify_email(Email=student_email_ent.get().lower()):
             student_email_ent.config(highlightcolor='red',
                                    highlightbackground='red' )
             student_email_ent.focus()
             massage_box(massage='Please Enter a valid\nEmail Address.')

        elif account_password_ent.get()== '':
             account_password_ent.config(highlightcolor='red',
                                    highlightbackground='red' )
             account_password_ent.focus()
             massage_box(massage='Create Account Password is Required.')   

        else:
            pic_data = b''

            
            if pic_path.get() != '':

                resize_pic = Image.open(pic_path.get()).resize((100,100))
                resize_pic.save('temp_pic.png')

                read_data = open('temp_pic.png','rb')
                pic_data = read_data.read()
                read_data.close()
                
            else:
                read_data = open('image/student_profile_img.png','rb')
                pic_data = read_data.read()
                read_data.close()
                pic_path.set('image/student_profile_img.png')

            add_data(id_number=student_id.get(),
                     name=student_name_ent.get(),
                     gender=student_gender.get(),
                     age=student_age_ent.get(),
                     phone_number= student_contact_ent.get(),
                     student_class=select_class_btn.get(),
                     email=student_email_ent.get(),
                     password=account_password_ent.get(),
                     pic_data=pic_data)
            
            data = f"""
{student_id.get()}
{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{student_contact_ent.get()}
{select_class_btn.get()}
{student_email_ent.get()}
"""
            
            get_student_card = draw_student_card(student_pic_path=pic_path.get(),
                              student_data=data )
            student_card_page(student_card_obj = get_student_card)
  
            create_account_page_fm.destroy()
            root.update()

            massage_box('Account Successful Created.')

    student_gender = tk.StringVar()
    class_list = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th']

    create_account_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                        highlightthickness=3)
    add_pic_section_fm = tk.Frame(create_account_page_fm,highlightbackground=bg_color,
                                        highlightthickness=2)

    add_pic_btn = tk.Button(add_pic_section_fm, image=add_image, bd=0, command= open_pic)

    add_pic_btn.pack()

    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    student_name_lb = tk.Label(create_account_page_fm, text="Enter Full Student Name:",font=('Bold', 12))

    student_name_lb.place(x= 5, y=130)

    student_name_ent = tk.Entry(create_account_page_fm, font=('Bold', 14),
                                highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_name_ent.place(x=5, y=160, width=200)
    student_name_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_name_ent))

    student_gender_lb = tk.Label(create_account_page_fm, text="Enter Student Gender:",font=('Bold', 12))

    student_gender_lb.place(x= 5, y=210)

    male_gender_btn = tk.Radiobutton(create_account_page_fm, text='Male',
    font=('Bold',12), variable=student_gender, value='male')

    male_gender_btn.place(x=5, y=235)

    female_gender_btn = tk.Radiobutton(create_account_page_fm, text='Female', 
    font=('Bold',12), variable=student_gender, value='female')

    female_gender_btn.place(x=75, y=235)

    student_gender.set('male')

    student_age_lb = tk.Label(create_account_page_fm, text="Enter Student Age:",
                            font=('Bold', 12))
    student_age_lb.place(x=5, y=275)

    student_age_ent = tk.Entry(create_account_page_fm, font=('Bold', 14),
                                highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_age_ent.place(x=5, y=305, width=200)

    student_age_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_age_ent))

    student_contact_lb = tk.Label(create_account_page_fm, text="Enter Student Contact Phone:",
                            font=('Bold', 12))
    student_contact_lb.place(x=5, y=360)

    student_contact_ent = tk.Entry(create_account_page_fm, font=('Bold', 14),
                                highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_contact_ent.place(x=5, y=390, width=200)

    student_contact_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_contact_ent))


    student_class_lb = tk.Label(create_account_page_fm, text="Select Student CLass:",
                            font=('Bold', 12))
    student_class_lb.place(x=5, y=445)

    select_class_btn = Combobox(create_account_page_fm, font=('Bold', 15),
                                state='randomly', values=class_list)
    select_class_btn.place(x=5 ,y=475, width=180, height=30)

    student_id_lb = tk.Label(create_account_page_fm, text='Student ID Number:',
                            font=('Bold', 12))
    student_id_lb.place(x=240, y=35)


    student_id = tk.Entry(create_account_page_fm, font=('Bold', 18), bd=0)
    student_id.place(x=380, y=35, width=80)


    student_id.config(state='readonly')
    
    generate_id_number()

    id_info_lb = tk.Label(create_account_page_fm, text="""Automatically Generated ID Number
! Remember Using This ID Number
Student will Login Account.""", justify=tk.LEFT)
    id_info_lb.place(x=240, y=65)

    student_email_lb = tk.Label(create_account_page_fm, text="Enter Student Email Address:",
                            font=('Bold', 12))
    student_email_lb.place(x=240, y=130)

    student_email_ent = tk.Entry(create_account_page_fm, font=('Bold', 14),
                                highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_email_ent.place(x=240, y=160, width=200)

    student_email_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=student_email_ent))

    email_info_lb = tk.Label(create_account_page_fm, text="""Via Email Address Student
Can Recover Account
! In Case Forgetting Password And Also 
Student will get future Verification.""", justify=tk.LEFT)
    email_info_lb.place(x=240, y=200)


    account_password_lb = tk.Label(create_account_page_fm, text="Create Account Password:",
                            font=('Bold', 12))
    account_password_lb.place(x=240, y=275)

    account_password_ent = tk.Entry(create_account_page_fm, font=('Bold', 14),
                                highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    account_password_ent.place(x=240, y=307, width=200)

    account_password_ent.bind('<KeyRelease>',
                          lambda e: remove_highlight_warning(entry=account_password_ent))

    account_password_info_lb = tk.Label(create_account_page_fm, text="""Via Student Create Password 
And Provided ID Number
Student Can Login Account.""", justify=tk.LEFT)
    account_password_info_lb.place(x=240, y=345)

    home_btn = tk.Button(create_account_page_fm, text='Home', font=('Bold', 15),
                        bg='red', fg='white', bd=0, command=forward_to_welcome_page)
    home_btn.place(x=240, y=420)

    Submit_btn = tk.Button(create_account_page_fm, text='Submit', font=('Bold', 15),
                        bg=bg_color, fg='white', bd=0, command=check_input_validation)
    Submit_btn.place(x=360, y=420)

    create_account_page_fm.pack(pady=5)
    create_account_page_fm.pack_propagate(False)
    create_account_page_fm.configure(width=480, height=580)

init_database()
# welcome_page()
# admin_dashboard()
admin_login_page()
# student_dashboard(student_id=736150)
root.mainloop()