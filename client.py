# Client generates a key and encrypts the file, and sends it to server.
# client is the sender and server is the receiver


import socket
import tqdm
import os
import yagmail
import time
from cryptography.fernet import Fernet



def get_cred():
    print("\nEnter details: \n")
    username=input("Enter your email username: ")
    pwd=input("Enter your email password: ")
    receiver=input("Enter receiver email username: ")
    try:
        yag = yagmail.SMTP(username,pwd)
    except:
        print("\nINVALID CREDENTIALS. PLEASE RE-ENTER DETAILS.\n ")
        get_cred()
        
    print('\n')
    return (yag,str(receiver))
    


def create_socket():
    try:
        s = socket.socket()
        return s
    except:
        print("Socket creation error")




def connect_to_server(s,server_ip):
    try:
        host=server_ip
        port=8921
        print("Connecting to: " + str(host) + ":" + str(port))
        s.connect((host, port))
        print("Connected")
    except:
        s=create_socket()
        print("error while connecting to server")
        print("Reconnecting...\n")
        time.sleep(1000)
        connect_to_server(s,server_ip)




def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key




def encrypt(ptext,ctext,key):
    f = Fernet(key)
    with open(ptext, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    print("ENCRYPTION DONE")
    with open(ctext, "wb") as file:
        file.write(encrypted_data)
    print("CIPHERTEXT.TXT CREATED")




def send_email(yag,receiver):
    body = "CIPHER KEY"
    filename = "key.key"
    yag.send(to=receiver, subject="KEY", contents=body,attachments=filename)





def send_file(s,ctext):
    fileSize = os.path.getsize(ctext)
    print("filesize", fileSize)
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096  # sending 4096 bytes each time step
    s.send(f"{ctext}{SEPARATOR}{fileSize}".encode())

    progress = tqdm.tqdm(range(
        fileSize), f"Sending {ctext}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(ctext, "rb") as f:
        bytes_read = f.read(BUFFER_SIZE)
        for _ in progress:
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()




def main():
    server_ip="192.168.0.107"            # Enter server ip address here
    
    yag,receiver=get_cred()
    
    ptext= "plaintext.txt"
    ctext= "ciphertext.txt"
    
    s=create_socket()
    connect_to_server(s,server_ip)
    
    key = write_key()    
    encrypt(ptext,ctext,key)
    send_email(yag,receiver)
    
    print("Press any key to continue")
    input()
    
    try:
        send_file(s,ctext)
        print("SENT FILE")
    except:
        print("\nFile not sent\n")


if __name__ == "__main__":
    main()
