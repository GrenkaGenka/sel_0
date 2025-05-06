import time
from mailslurp_client import ApiClient, Configuration, InboxControllerApi, WaitForControllerApi

# Простой пример создания временной почты с помощью MailSlurp

def create_email_example():
    # 1. Настройка MailSlurp API
    MAILSLURP_API_KEY = "YOUR_MAILSLURP_API_KEY_HERE"  # Замените на ваш API ключ
    
    config = Configuration()
    config.api_key['x-api-key'] = MAILSLURP_API_KEY
    api_client = ApiClient(config)
    
    # 2. Создание клиентов MailSlurp
    inbox_controller = InboxControllerApi(api_client)
    wait_controller = WaitForControllerApi(api_client)
    
    # 3. Создание нового почтового ящика
    print("Создание нового временного почтового ящика...")
    inbox = inbox_controller.create_inbox()
    
    # 4. Получение данных почтового ящика
    inbox_id = inbox.id
    email_address = inbox.email_address
    
    print(f"Создан почтовый ящик:")
    print(f"- ID: {inbox_id}")
    print(f"- Email адрес: {email_address}")
    
    # 5. Ожидание входящего письма (опционально)
    wait_for_emails = input("Хотите дождаться входящих писем? (да/нет): ").lower()
    
    if wait_for_emails == "да":
        print(f"Ожидаем входящие письма для {email_address}...")
        print("(Отправьте тестовое письмо на этот адрес)")
        
        # Ожидание до 30 секунд для получения письма
        try:
            emails = wait_controller.wait_for_latest_emails(
                inbox_id=inbox_id,
                count=1,
                timeout=30000,  # 30 секунд
                unread_only=True
            )
            
            if emails and len(emails) > 0:
                email = emails[0]
                print("\nПолучено новое письмо:")
                print(f"От: {email.from_}")
                print(f"Тема: {email.subject}")
                print(f"Содержание:\n{email.body}")
            else:
                print("Письма не получены в течение времени ожидания.")
        except Exception as e:
            print(f"Ошибка при ожидании писем: {e}")
    
    # 6. Получение списка писем (альтернативный подход)
    list_emails = input("Хотите проверить все письма в ящике? (да/нет): ").lower()
    
    if list_emails == "да":
        emails = inbox_controller.get_emails(inbox_id)
        
        if emails and len(emails) > 0:
            print(f"\nВсего писем в ящике: {len(emails)}")
            for i, email in enumerate(emails):
                print(f"\nПисьмо #{i+1}:")
                print(f"От: {email.from_}")
                print(f"Тема: {email.subject}")
                print(f"Дата: {email.created_at}")
        else:
            print("В ящике нет писем.")
    
    # 7. Удаление ящика (опционально)
    delete_inbox = input("Хотите удалить созданный почтовый ящик? (да/нет): ").lower()
    
    if delete_inbox == "да":
        inbox_controller.delete_inbox(inbox_id)
        print(f"Почтовый ящик {email_address} удален.")
    else:
        print(f"Почтовый ящик {email_address} сохранен для дальнейшего использования.")
        print("Обратите внимание, что временные ящики могут быть автоматически удалены через определенное время.")
    
    return {
        "inbox_id": inbox_id,
        "email_address": email_address
    }

# Простая функция для отправки письма на указанный адрес
def send_test_email(sender_inbox_id, recipient_email):
    MAILSLURP_API_KEY = "YOUR_MAILSLURP_API_KEY_HERE"  # Замените на ваш API ключ
    
    config = Configuration()
    config.api_key['x-api-key'] = MAILSLURP_API_KEY
    api_client = ApiClient(config)
    
    inbox_controller = InboxControllerApi(api_client)
    
    from mailslurp_client import SendEmailOptions
    
    # Создаем опции для письма
    send_options = SendEmailOptions(
        to=[recipient_email],
        subject="Тестовое письмо",
        body="Это тестовое письмо отправлено с помощью MailSlurp API.\n\nПривет!",
        from_=f"sender_{sender_inbox_id}@mailslurp.com",  # Это будет заменено на реальный адрес отправителя
        is_html=False
    )
    
    # Отправляем письмо
    sent_email = inbox_controller.send_email(sender_inbox_id, send_options)
    print(f"Письмо отправлено с ID: {sent_email.id}")

# Функция для проверки всех писем в ящике
def check_inbox(inbox_id):
    MAILSLURP_API_KEY = "YOUR_MAILSLURP_API_KEY_HERE"  # Замените на ваш API ключ
    
    config = Configuration()
    config.api_key['x-api-key'] = MAILSLURP_API_KEY
    api_client = ApiClient(config)
    
    inbox_controller = InboxControllerApi(api_client)
    
    # Получаем все письма
    emails = inbox_controller.get_emails(inbox_id)
    
    print(f"Найдено {len(emails)} писем в ящике")
    
    for i, email in enumerate(emails):
        print(f"\nПисьмо #{i+1}:")
        print(f"ID: {email.id}")
        print(f"От: {email.from_}")
        print(f"Тема: {email.subject}")
        print(f"Получено: {email.created_at}")
        
        # Получить полное содержание письма
        full_email = inbox_controller.get_email(email.id)
        print(f"Содержание:\n{full_email.body}")

if __name__ == "__main__":
    # Исполняем пример создания почты
    inbox_info = create_email_example()
    
    # Дополнительные операции с созданным ящиком
    while True:
        print("\nДополнительные действия:")
        print("1. Отправить тестовое письмо с этого ящика")
        print("2. Проверить входящие письма")
        print("3. Выйти")
        
        choice = input("Выберите действие (1-3): ")
        
        if choice == "1":
            recipient = input("Введите адрес получателя: ")
            send_test_email(inbox_info["inbox_id"], recipient)
        elif choice == "2":
            check_inbox(inbox_info["inbox_id"])
        elif choice == "3":
            print("Завершение программы...")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")