import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from to_do_365.settings.base import EMAIL_HOST, EMAIL_PORT


class Util:
    @staticmethod
    def send_email(data):
        subject = data['email_subject']
        body = data['email_body']
        to_email = data['to_email']

        EMAIL_HOST = os.environ.get('EMAIL_HOST')
        EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))
        EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                server.sendmail(EMAIL_HOST_USER, to_email, msg.as_string())
        except smtplib.SMTPAuthenticationError as e:
            print(f'Erro de autenticação SMTP: {e}')
