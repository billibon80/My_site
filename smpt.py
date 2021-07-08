import smtplib
from email.mime.text import MIMEText
from email.header import Header

class PostSomeself:

    def __init__(self, name, email, phone, message):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message

    def connection_mail_ru(self, email, password):
        with smtplib.SMTP_SSL("smtp.mail.ru", port=465, timeout=15) as connection:
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=email, msg=self.message_from_site().as_string())

    def connection_gmail_com(self, email, password):
        with smtplib.SMTP("smtp.gmail.com", port=587, timeout=15) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=email, msg=self.message_from_site().as_string())

    def message_from_site(self):
        msg_site = f"Name: {self.name}\nEmail: {self.email}\n" \
               f"Phone: {self.phone}\nMessage: {self.message}"
        msg = MIMEText(msg_site, 'plain', 'utf-8')
        msg['Subject'] = Header("Сообщение с сайта", 'utf-8')

        return msg
