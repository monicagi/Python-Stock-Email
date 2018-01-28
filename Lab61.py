# sendemailMIMEmsg.py
# Tindall, example sending MIMEMultipart email message
# MIME    Mail Interchange Message Extension format

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import password
import Lab6

#-- End SendEmailMsgWithAttachment -------------------------------------------------------
def SendEmailMsgWithAttachment(fromuser, tolist, subject, message, \
                               attachmentfilename="No Filename.txt", \
                               attachmentContent="No Content"):



    msg = MIMEMultipart()
    msg.attach(MIMEText(message))

    msg['From'] = fromuser
    msg['To'] = ', '.join(tolist)
    msg['Subject'] = subject

    #attachment = MIMEText(open(attachmentfilename,"r").read())
    attachment = MIMEText(attachmentContent)
    attachment.add_header('Content-Disposition', 'attachment', filename=attachmentfilename+".txt")
    msg.attach(attachment)

    smtpObj = smtplib.SMTP('smtp.office365.com', 587)
    smtpObj.starttls()
    #Place your email in the enter email and your email password
    smtpObj.login('ENTER EMAIL', password.password)
    smtpObj.sendmail(fromuser, tolist, msg.as_string())
    smtpObj.quit()

    return

def SendEmailMsgWithAttachmentFilename(fromuser, tolist, subject, message, attachmentfilename):

    SendEmailMsgWithAttachment(fromuser, tolist, subject, message, \
                               attachmentfilename, \
                               open(attachmentfilename, "r").read())
    return

#-- End SendEmailMsgWithAttachment -------------------------------------------------------

if __name__ == "__main__":
    print("Sending message with attachment")

    #Calls the get_file function from Lab6
    Lab6.get_file()

    #Sends an email with the file and stock information
    SendEmailMsgWithAttachmentFilename('guevaram@spu.edu', \
                           ['guevaram@spu.edu'], \
                           'CSC 4800 XML Stock Quotes-Monica Guevara', \
                           Lab6.info, \
                           '2017-02-15 stockquotes.xml')


    print("Done")
