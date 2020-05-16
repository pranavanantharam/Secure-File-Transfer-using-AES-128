# Server reads the key and decrypts the file and displays the data.

import socket
import time
import tqdm
import os
import time
from cryptography.fernet import Fernet
import attachmentDownload as ad



def get_cred(imap_url):
    print("Enter details: \n")
    username=input("Enter your email username: ")
    pwd=input("Enter your email password: ")
    sender=input("Enter sender email username: ")
    try:
        con=ad.auth(username,pwd,imap_url)
    except:
        print("\nINVALID CREDENTIALS. PLEASE RE-ENTER DETAILS.\n")
        get_cred(imap_url)
        
    print('\n')
    return (con,str(sender))



def create_socket():
    try:
        s = socket.socket()
        return s
    except socket.error as msg:
        print("Socket creation error: " + str(msg))



def bind_socket(s,server_ip):
    try:
        host=server_ip
        port=8921
        print("Binding the port: " + str(port))
        s.bind((host,port))
        s.listen(5)
        print(f"[*] Listening on {host}:{port}")
    except socket.error as msg:
        print("Socket binding error: " + str(msg))


       
def load_key(con,sender):
    attachment_dir=r"C:\Python\CRYPTO PROJECT\FINAL"
    name="key.key"
    while True:
        messages_list=ad.search('FROM', sender, con)
        messages=ad.get_emails(messages_list, con)
        for message in messages:
            ad.get_attachment(message, attachment_dir, name)    
        try:
            return open("key.key", "rb").read()
            break
        except:
            print("Waiting for key...")
            time.sleep(2000)



def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()			# read the encrypted data
 
    decrypted_data = f.decrypt(encrypted_data)		# decrypt data
    with open("output.txt", "wb") as file:
        file.write(decrypted_data)		        # write the original file




def socket_accept(s):
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    client_socket, address = s.accept()
    
    print("Connection has been established: " + "IP " + str(address[0]) + " |Port " + str(address[1]))
    
    received = client_socket.recv(BUFFER_SIZE).decode()
    fileName, fileSize = received.split(SEPARATOR)
    fileName = os.path.basename(fileName)
    fileSize = int(fileSize)

    progress = tqdm.tqdm(range(fileSize), f"Receiving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(fileName, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    client_socket.close()
    s.close()
    return fileName



def main():
    server_ip="192.168.0.107"
    imap_url='imap.gmail.com'
    
    con,sender=get_cred(imap_url)
    
    s=create_socket()
    bind_socket(s,server_ip)
    fileName = socket_accept(s)
    print("DOWNLOADED CIPHER TEXT")
    key = load_key(con,sender)
    print("DOWNLOADED KEY")
    decrypt(fileName,key)
    print("DECRYPTION DONE")


if __name__ == "__main__":
    main()


