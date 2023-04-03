import smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,otp):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('munvarsulthana35@gmail.com','ucdxnyborboztnip')
    msg=EmailMessage()
    msg['From']='munvarsulthana35@gmail.com'
    msg['Subject']='Account Sign up OTP'
    msg['To']=to
    body=f'Your one time password for registrstion is {otp}'
    msg.set_content(body)
    server.send_message(msg)
    server.quit()
