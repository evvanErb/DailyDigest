"""Send Mail"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open ("passwords.txt", "r") as myfile:
    keysAndPasses = myfile.read()

keysAndPasses = eval(keysAndPasses)
EMAIL_PASSWORD = keysAndPasses["EMAIL_PASSWORD"]
SENDER_ADDR = keysAndPasses["SENDER_ADDR"]

def sendEMail(messageContent, receiveAddr, session):

    #Setup the MIME
    message = MIMEMultipart()
    message["From"] = "Daily Digest"
    message["To"] = receiveAddr
    message["Subject"] = "Daily Digest Report"

    #The body and the attachments for the mail
    message.attach(MIMEText(messageContent, "html"))
    #Text of email
    text = message.as_string()
    #Send EMail
    session.sendmail(SENDER_ADDR, receiveAddr, text)


def sendMassIndividualEmails(messageContent, addresses):
    #Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.gmail.com", 587) #use gmail with port
    session.starttls() #enable security
    session.login(SENDER_ADDR, EMAIL_PASSWORD) #login with mail_id and password

    #Iterate over all user emails and send to each
    for email in addresses:
        sendEMail(messageContent, email, session)

    #End Session after all emails sent
    session.quit()

    print("[*] Mail Sent")
