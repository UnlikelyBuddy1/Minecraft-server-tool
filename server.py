#region imports
import socket
import threading
import time
import subprocess
import os
import csv
#endregion
#region init
current_directory = (os.path.dirname(os.path.realpath(__file__)))
current_directory = current_directory.replace("\\", '/')

if(os.path.isfile(current_directory+'/MCserver_configs.csv')):
    with open(current_directory+'/MCserver_configs.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            try:
                PORT = int(line['port'])
            except:
                print("the port value MUST be an integer, check your MCserver_configs.csv file")
            first_launch = line['first_launch']
    if first_launch:
        PORT=int(input("PORT of the server ? must be an integer (default is 9999)\n"))
        first_launch=0
        fieldnames=['port','first_launch']
        with open(current_directory+'/MCserver_configs.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames, delimiter=',')
            csv_writer.writeheader()
            line = {fieldnames[0]: PORT, fieldnames[1]: first_launch}
            csv_writer.writerow(line)

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
status="closed"
mc=False
#endregion
#region server funcs
def handle_client(conn, addr):
    global status, mc
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            if msg == "start":
                #launch program
                mc=subprocess.Popen("start.bat", shell=True)
                status="open"
            if msg == "stop":
                if mc:
                    try :
                        mc=subprocess.Popen("stop.bat")
                    except :
                        pass
                    status="closed"
            conn.send(status.encode(FORMAT))
    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
#endregion
print("[STARTING] server is starting...")
start()
