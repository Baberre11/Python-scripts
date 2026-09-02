import argparse 
import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = ""
APP_PASSWORD = ""

def send_email(recipient_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email.")
    parser.add_argument("recipient_email", help="Recipient's email address")
    parser.add_argument("subject", help="Subject of the email")
    parser.add_argument("body", help="Body of the email")

    args = parser.parse_args()

    send_email(args.recipient_email, args.subject, args.body)
    
    