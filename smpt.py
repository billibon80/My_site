import smtplib


class PostSomeself:

    def __init__(self, name, email, phone, message):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message

    def connection_mail_ru(self, email, password):
        with smtplib.SMTP_SSL("smtp.mail.ru", port=465, timeout=15) as connection:
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=email, msg=self.message_from_site())

    def connection_gmail_com(self, email, password):
        with smtplib.SMTP("smtp.gmail.com", port=587, timeout=15) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=email, msg=self.message_from_site())

    def message_from_site(self):
        return f"Subject: Message from site\n\nName: {self.name}\nEmail: {self.email}\n" \
                  f"Phone: {self.phone}\nMessage: {self.message}"
