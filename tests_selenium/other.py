from login_mail import MailSlurpClient

client = MailSlurpClient()

email_address = client.create_email()

while True:
    list_emails = input("Хотите проверить все письма в ящике? (да/нет): ").lower()
    if list_emails == "да":
        client.check_inbox()

