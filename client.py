#region imports
import csv
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from datetime import datetime
from PIL import ImageTk, Image
import os
import sys
import socket
#endregion
#region initial variables
client=None
error=0
focus_settings=0
status="off"
command=""
#endregion
#region GUI colors theme and image looading
# default
light_gray_color = "#333333"
dark_gray_color = "#1e1e1e"
white_color = "#f1f1f1"
accent_color = "#007acc" 
connect_color = "#eaa100" 
start_color = "#ff830f"
selected_color = "#252526"
#endregion
#region GUI
current_directory = (os.path.dirname(os.path.realpath(__file__)))
current_directory = current_directory.replace("\\", '/')
fieldnames=['ip','port']

def shut_down():
    global fieldnames
    if(os.path.isfile(current_directory+'/configs/configs.csv')):
        with open(current_directory+'/configs/configs.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames, delimiter=',')
            csv_writer.writeheader()
            line = {fieldnames[0]: '{}'.format(ip_entry.get()), fieldnames[1]: '{}'.format(port_entry.get())}
            csv_writer.writerow(line)
    client.close()
    sys.exit()

root = Tk()
root.geometry("381x181")
root.title("Rlcraft Tool")  # assign a title to the window
root.protocol('WM_DELETE_WINDOW', shut_down)
try :
    img = (ImageTk.PhotoImage(Image.open(current_directory+"/images/background.png")))
    img_settings = (ImageTk.PhotoImage(Image.open(current_directory+"/images/settings_bg.png")))
    bedrock = (ImageTk.PhotoImage(Image.open(current_directory+"/images/bedrock.png")))
    img_start = (ImageTk.PhotoImage(Image.open(current_directory+"/images/dirt.png")))
    img_stop = (ImageTk.PhotoImage(Image.open(current_directory+"/images/stone.png")))
except:
    pass
background = Label(root, image=img).place(x=0, y=0, relwidth=1, relheight=1)
try:
    root.iconphoto(False, tk.PhotoImage(
        file=current_directory+'/images/logo.png'))
except:
    pass
fontStyle = tkFont.Font(family="sans-serif", size=16)

frame=Frame(root, bd=0, bg=light_gray_color)
frame.pack(side=LEFT)

status_frame=Frame(root, bd=0, bg=dark_gray_color)
status_frame.pack(side=BOTTOM)
#endregion
#region network funcs
def get_status():
    global client, error, command
    PORT = int(port_entry.get())
    SERVER = str(ip_entry.get())
    ADDR = (SERVER, PORT)
    try: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        reply=send(command)
        test(reply)
    except:
        error=1
        test("")
    else:
        error=0

status_button = Button(status_frame, width=5, padx=5, pady=5, fg=dark_gray_color, bg="orange",bd=0, command=get_status)
status_button.pack(side=RIGHT, expand=1)
status_text = Label(status_frame, width=5, text="Status", bg=dark_gray_color, fg=white_color,justify='center').pack(side=RIGHT, expand=1)  # put text on the window

def test(state):
    global status
    if state == "open":
        status_button.configure(bg="green")
    elif state == "closed" :
        status_button.configure(bg="orange")
    else:
        status_button.configure(bg="red")
    status=state
#endregion
#region settings

def dont_close():
    global focus_settings, error, command, client
    PORT = int(port_entry.get())
    SERVER = str(ip_entry.get())
    ADDR = (SERVER, PORT)
    if error:
        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            reply=send(command)
            test(reply)
        except:
            status_button.configure(bg="red")
        else:
            error=0
            
    settings.withdraw()
    

def show_settings():
    global focus_settings
    settings.update()
    settings.deiconify()
    focus_settings=1

settings = Toplevel()
settings.geometry("181x181")

background = Label(settings, image=img_settings).place(x=0, y=0, relwidth=1, relheight=1)
settings.title("")
settings.configure(bg=light_gray_color)
try :
    settings.iconphoto(False, tk.PhotoImage(file=current_directory+'/images/logo.png'))
except:
    pass
settings.protocol('WM_DELETE_WINDOW', dont_close)
settings.withdraw()

show_settings_button = Button(frame, image=bedrock, bd=0, command=show_settings)

ip_label=Label(settings, text="IP ADRESS", bg="#8B4513", width=12, fg="black", relief=RAISED)
ip_label['font']=fontStyle
ip_label.pack(side=TOP)
ip_entry=Entry(settings, justify='center', bg="#8B4513", width=12, fg="black", relief=SUNKEN)
ip_entry['font']=fontStyle
ip_entry.pack(side=TOP)

port_label=Label(settings, text="PORT", width=9, bg="#8B4513", fg="black", relief=RAISED)
port_label['font']=fontStyle
port_entry=Entry(settings, justify='center', bg="#8B4513", width=12, fg="black", relief=SUNKEN)
port_entry['font']=fontStyle
port_label.pack()
port_entry.pack()

if(os.path.isfile(current_directory+'/configs/configs.csv')):
    with open(current_directory+'/configs/configs.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            ip = line['ip']
            port = line['port']
            ip_entry.insert(INSERT, ip)
            port_entry.insert(INSERT, port)
else:
    port_entry.insert(INSERT, 9999)
# endregion
#region Network
HEADER = 64

PORT = int(port_entry.get())
SERVER = str(ip_entry.get())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)
    
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    return (client.recv(2048).decode(FORMAT))

get_status()
if error:
    MsgBox = tk.messagebox.showwarning('Warning', 'The IP adress or PORT are wrong OR the server pc is turned off', icon='warning')
    show_settings()
    status_button.configure(bg="red")
    
#endregion
#region start & stop buttons
def start():
    try:
        reply=send("start")
        test(reply)
    except:
        status_button.configure(bg="red")
    
    
def stop():
    if status != "off":
        MsgBox = tk.messagebox.askquestion('Warning', 'Are you sure you want to Stop server ?', icon='warning')
        if (MsgBox == 'yes'):
            try:
                reply=send("stop")
                test(reply)
            except:
                status_button.configure(bg="red")
        

start_button = Button(frame, image=img_start, bd=0, command=start)
stop_button = Button(frame, image=img_stop, bd=0, command=stop)
start_button.pack()
stop_button.pack()  
show_settings_button.pack()
#endregion
root.mainloop()