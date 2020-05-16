# Secure File Transfer using AES - 128 Encryption

A script which enables file transfer between 2 devices over a LAN using AES-128 algorithm to encrypt the contents of the file.


## Requirements

- Gmail accounts ( ' allow less secure apps ' option must be enabled )
- Python 3.7+

## Instructions
- To run client script : 
``` python3 client.py ```
- To run server script : 
``` python3 server.py ```

## Note
- Make changes to the directory path accordingly in the server program. ( Located in load_key function )
- IP address of receiver device must changed accordingly in both client and server scripts.
