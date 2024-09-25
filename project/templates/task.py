import logging
from celery import shared_task
import requests, os


@shared_task
def send_sms_task(phone, text):
    """call api"""
    action = os.environ.get("SMS_ACTION")
    api_key = os.environ.get("SMS_API_KEY")
    sender_id = os.environ.get("SMS_SENDER_ID")
    url = os.environ.get("SMS_SEND_URL")
    url = f"{url}?action={action}&api_key={api_key}&to={phone}&from={sender_id}&sms={text}&unicode=1"
    if os.environ.get("FEATURE_SMS", False):
        try:
            res = requests.post(url)
            return res
        except Exception as e:
            logging.critical(f"Failed to send sms to phone: {phone}. Due to {str(e)}")
