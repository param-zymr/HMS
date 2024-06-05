"""Core email sending functionality"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from src.main import app_settings, app_logger

email_template_dir = "/email/"

def send_email(template_name:str, context:dict, recipients:list, sender:str=None) -> bool:
    template_name = email_template_dir + template_name
    if not sender:
        sender = app_settings.SMTP_DEFAULT_SENDER
    mail_server_session = smtplib.SMTP(app_settings.SMTP_SERVER, app_settings.SMTP_PORT)
    mail_server_session.starttls()
    mail_server_session.login(app_settings.SMTP_USERNAME, app_settings.SMTP_PASSWORD)
    environment = Environment(loader=FileSystemLoader(\
        app_settings.TEMPLATE_DIR+email_template_dir))
    template = environment.get_template("notification_email.html")
    email_html = template.render(**context)
    email_message = MIMEMultipart('alternative')
    email_message['From'] = sender
    email_message['To'] = ",".join(recipients)
    email_message['Subject'] = context["subject"]
    email_message.attach(MIMEText(email_html, 'html'))
    try:
        mail_server_session.sendmail(sender, recipients, str(email_message))
        mail_server_session.quit()
        return True
    except Exception as email_error:
        app_logger.error(str(email_error))
        return False
