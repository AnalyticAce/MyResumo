import smtplib, ssl, pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
from jinja2 import Environment, FileSystemLoader
import os

def send_email(subject: str, email_sender, 
            email_receiver, passwd, template_file, template_vars=None) -> None:
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject

    template_dir = os.path.dirname(template_file)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(os.path.basename(template_file))

    html_body = template.render(**(template_vars or {}))

    em.add_alternative(html_body, subtype='html')
    context = ssl.create_default_context()

    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
        try:
            smtp.login(email_sender, passwd)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        except smtplib.SMTPAuthenticationError as e:
            print("Authentication failed. Please check:")
            print("1. Make sure you're using your complete email address")
            print("2. Verify your password is correct")
            print("3. Consider using an app-specific password if you have 2-step verification enabled")
            print(f"Error details: {str(e)}")
            
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            print(f"Error type: {type(e).__name__}")
