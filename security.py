#import win32file
import random
import math
from cryptography.fernet import Fernet 
from getpass import getpass
import time 
from tkinter import *
from tkinter import messagebox
import ctypes
from ctypes import wintypes
import os, re, sys, path
from pprint import pprint
import smtplib, ssl
from getmac import get_mac_address as gma

pendetails=['N:\\', 'ENR']
tempFile = os.environ["TEMP"].replace("\\", "/")+"/python-diskpart.txt"
selected = False
mainC = "diskpart /s "+tempFile
def write(cmd):
	with open(tempFile,'w') as f:
		f.write(cmd) 
def exe(cmd):
	test = os.popen(cmd).read()
	return test
ch=0
pen=False
pi=False
BlockInput = ctypes.windll.user32.BlockInput
BlockInput.argtypes = [wintypes.BOOL]
BlockInput.restype = wintypes.BOOL

#with open('loc.txt','r') as p:
 #   loc=p.read()

def locate_usb():
    cmd ="list volume"
    write(cmd)
    command =mainC+' | findstr /r "Volume.* ----"'
    result = exe(command)
    print(result)
    return temp

   
def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


def sendmail(recivers_address):
    port = 587  
    smtp_server = "smtp.gmail.com"
    sender_email = "pbl.group0000aaar@gmail.com"
    receiver_email = recivers_address
    password = "Pbl@00004"
    message = """
    Subject: Security concern

    Some unothenticate person is trying to acess your device"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def enable_readonly():
    disks=listVolume()
    for disk in disks:
        if 'KEY' in disk:
            lis=disk
    selected=lis.split('  ')[1]
    cmd = "select {}\r\nattributes disk set readonly".format(selected)  
    write(cmd)
    command =mainC
    result = exe(command)
    return result

def disable_readonly():
    disks=listVolume()
    for disk in disks:
        if 'KEY' in disk:
            lis=disk
    selected=lis.split('  ')[1]
    cmd = "select {}\r\nattributes disk clear readonly".format(selected)  
    write(cmd)
    command =mainC
    result = exe(command)
    return result

def lock():
   # blocked = BlockInput(True)
    root=Tk()
    print("pendrive not found")
    # photo = PhotoImage(file="enr.png")
    # img_label = Label(image=photo)
    # img_label.pack()
    l1=Label(root,text="Driver not found...",width=200,font='Helvetica 22 bold').place(x=-1000,y=500)
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes("-fullscreen", True)
    root.after('2000',root.destroy)
    root.mainloop()

def listVolume():
    cmd ="list volume"
    write(cmd)
    command =mainC+' | findstr /r "Volume.* ----"'
    result = exe(command)
    temp = result.split("\n")[1:-1]
    return temp

def getLabel(loc):
    temp=listVolume()
    for label in temp:
        if loc in label:
            return label.split('  ')[4]

def exiting():
    window = Tk()
    window.withdraw()
    messagebox.showinfo("Warning", "program is closing")
    window.mainloop()

def clean(select):
    cmd='select {}\r\nclean'.format(select)
    write(cmd)
    command =mainC
    result = exe(command)

def creatpartition(select):
    cmd='select {}\r\ncreat partition primary'.format(select)
    write(cmd)
    command =mainC
    result = exe(command)

def assgn(select):
    cmd='select {}\r\nassign letter="E"'.format(select)
    write(cmd)
    command =mainC
    result = exe(command)

def formate(select):
    cmd='select {}\r\nformat quick fs=fat32 label="KEY"'.format(select)
    write(cmd)
    command =mainC
    result = exe(command)

def penPrepare():
    print('pls choose the valume ')
    locate_usb()
    t=input('')
    with open('pendetails.txt','w') as d:
        d.write(t)
    totallist=listVolume()
    for volume in totallist:
        if t in volume:
            select = volume.split("  ")[1]
    clean(select)
    time.sleep(10)
    creatpartition(select)
    time.sleep(10)
    assgn(select)
    time.sleep(10)
    formate(select)
    time.sleep(30)
    newRandomkey()


cg= locate_usb()

def check():
    labele=getLabel('KEY')
    cg= locate_usb()
    if labele==' KEY':
        try:
            with open('E:\message.txt','rb') as f:
                message=f.read()
            num2=decrypt_message(message)
        except:
            sys.exit('somthing wrong')    
        try:
            with open('test.txt','r') as f:
                num1=f.read()
        except:
            sys.exit('wong credentials')        
        n1=int(num1)
        n2=int(num2)
        print(n1)
        print(n2)
        if n1==n2:
            return True
        else:
            return False
    else:
        return False

def newRandomkey():
    disable_readonly()
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    try:    
        with open("test.txt",'w') as m:
            m.write(random_str)
        encrypted_message=encrypt_message(random_str) 
        with open('E:\message.txt','wb') as f:
            f.write(encrypted_message)
    except:
        newRandomkey()  
    enable_readonly()          




T=True

if os.path.isfile('test.txt') or os.path.isfile('password.txt') or os.path.isfile('E:\message.txt') or os.path.isfile('mac_adress.txt'):
    try:
        with open('mac_adress.txt','rb') as r:
            mac_adress=r.read()
            
        mac=decrypt_message(mac_adress)
        if mac==bytes(gma(), 'utf-8'):
            print('pendrive ok')
        else:
            sys.exit('wrong device')
    except:
        sys.exit('wrong credentials')                
else:
    penPrepare()
    mac=gma()
    mac_adress=encrypt_message(mac)
    with open('mac_adress.txt','wb') as b:
        b.write(mac_adress)
    mail=input('please enter your mail id: ')
    mial_id=encrypt_message(mail)
    with open('credential.txt','wb') as b:
        b.write(mial_id)
    root1=Tk()
    def getpassword():               
        getpassword.password12=password123.get()
        root1.destroy() 
    root1.overrideredirect(True)
    root1.overrideredirect(False)
    root1.attributes("-fullscreen", True)
    Label(root1, text="Enter password :",font='Helvetica 22 bold').place(x=350,y=400)
    password123=StringVar()  
    e1 = Entry(root1,textvariable=password123,show="*",font='Helvetica 22 bold')
    e1.place(x=600,y=400)
    Button(root1, 
          text='Submit', 
          command=getpassword,font='Helvetica 14 bold' ).place(x=900,y=400)
    root1.mainloop()
    password=getpassword.password12
    

    hashed = encrypt_message(password)
    with open('password.txt','wb') as s:
        s.write(hashed)

with open('credential.txt','rb') as r:
    mail=r.read()
mail_id=decrypt_message(mail).decode("utf-8")    
    

checking = check()
if checking:
    disable_readonly()
    newRandomkey()
    enable_readonly()
else:
    lock()    

while True:
    checking = check()
    if checking:
        print('ok')
    else:
        T=True
        while T:
            lock()
            rechecking=check()
            if rechecking:

                disable_readonly()
                newRandomkey()
                enable_readonly()
                T=False
            else:
                if ch>2:
                    unblocked = BlockInput(False) 
                    root1=Tk()
                    def getpassword():
                        getpassword.password12=password123.get()
                        root1.destroy()
                    root1.overrideredirect(True)
                    root1.overrideredirect(False)
                    root1.attributes("-fullscreen", True)
                    Label(root1, text="Enter password :",font='Helvetica 22 bold').place(x=350,y=400)
                    password123=StringVar()
                    e1 = Entry(root1,textvariable=password123,show="*",font='Helvetica 22 bold')
                    e1.place(x=600,y=400)
                    Button(root1, 
                    text='Submit', 
                    command=getpassword,font='Helvetica 14 bold' ).place(x=900,y=400)
                    root1.mainloop()
                    password=getpassword.password12
                    res = bytes(password, 'utf-8')
                    with open('password.txt','rb') as s:
                        hashed=s.read()
                    if decrypt_message(hashed)==res:
                        sys.exit()
                    elif ch==4:
                        sendmail(mail_id)
                    if ch>15:
                        check()
                        
                ch=ch+1                                  
    time.sleep(25)