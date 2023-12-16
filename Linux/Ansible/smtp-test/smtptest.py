import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "sender@gmail.com"  # Replace with your Gmail email address
receiver_email = "receiver@gmail.com"
subject = "pythontest"
body = "This is a test email sent from Python."

# SMTP server configuration
smtp_server = "smtp.server"
smtp_port = 25  # Adjust the port as needed

# Create the MIME message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the body to the message
message.attach(MIMEText(body, "plain"))

# Establish a connection to the SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent successfully.")