import imaplib, email, os
'''
Function to authorise a user gievn the username and password
Returns an IMAP4 object
'''
def auth(username,password,imap_url):

    #create an IMAP4 object at the required mail server
    con=imaplib.IMAP4_SSL(imap_url)

    #login to your account
    con.login(username,password)

    #return the IMAP4 object
    return con




'''
Function to extract email body from a message object
Returns the raw data of the body
'''
def get_body(message):

    #Check if email maultiple parts
    if message.is_multipart():

        #Run a recursive function until we arrive at the first part of the payload
        return get_body(message.get_payload(0))

    else:
        return msg.get_payload(None, True)






'''
Function to search for a mail with a given key and value
Key is something like 'FROM' or 'TO', whuch tells us what the value means
Value is an email ID
Returns a byte string with a list of email numbers corresponding to the required emails
e.g. [b'1 2 3']
'''
def search(key, value, imap_object):

    #Search using the search() function of an IMAP object
    imap_object.select('INBOX')
    result, data = imap_object.search(None, key, '"{}"'.format(value))

    #Return the list
    return data




'''
Function to extract corresponding emails, given a byte string with a list of mail numbers
Returns a list of messages in raw parsed form (message object).
'''
def get_emails(results_list, imap_object):

    #Create an empty message list
    messages=[]


    #Since the result list of the form [b'1 2 3'], we need to conver it to an iterable to loop through
    for mail_number in results_list[0].split():

        #Fetch the message with number 'mail_number'
        typ, data = imap_object.fetch(mail_number, '(RFC822)') #RFC specifies protocol used
        
        #Append the initial data part to the list, only this part is required to get attachment
        messages.append(email.message_from_bytes(data[0][1]))


    #Return the list
    return messages





'''
Function to extract a particular attachment from a message object
Does not return anything
Downloads the attachment to the specified location

It is ncessary to decode the attachment as it is in Code64 form
'''
def get_attachment(message, attachment_dir, attachmentName):

    #Iterate through different parts of the email using message.walk()
    for part in message.walk():

        #Check for a multipart message, if not then it will not contain an attachment
        if part.get_content_maintype()=='multipart' :
            continue

        #Check for content disposition, this shows whether the part is an attachment
        if part.get('Content-Disposition') is not None:
            continue

        #At this point we are sure that the message contains an attachment
        #Get the name of the attachment file
        fileName=part.get_filename()

        #Final verification of attachment name
        if bool(fileName) and fileName=='key.key':

            #Set the path for its download
            filePath= os.path.join(attachment_dir, fileName)

            #Write the attachment to the file
            with open(filePath, 'wb') as file:
                file.write(part.get_payload(decode=True))

