"""Celery Email Tasks"""
from src.main import app_logger
from src.app.utils.celery_config import celery
from src.app.utils.integrations.communications.email import send_email

@celery.task
def send_email_task(template_name:str, context:dict, recipients:list, sender:str=None):
    result = send_email(template_name, context, recipients, sender)
    if result:
        app_logger.info("email sent successfuly")
    else:
        app_logger.error("could not send email")
    return
