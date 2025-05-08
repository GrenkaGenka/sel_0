import time
from mailslurp_client import ApiClient, Configuration, InboxControllerApi, WaitForControllerApi
import mailslurp_client

# Простой пример создания временной почты с помощью MailSlurp

def create_email_example():
    # 1. Настройка MailSlurp API
    MAILSLURP_API_KEY = "f1d6106c5464c6751a87cbee9cdee5290403ce9874fa9e4c4d4e3cc501caa6a9"  # Замените на ваш API ключ
    
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
    

    
    # 6. Получение списка писем (альтернативный подход)
    list_emails = input("Хотите проверить все письма в ящике? (да/нет): ").lower()
    
    if list_emails == "да":
        emails = inbox_controller.get_emails(inbox_id)
        
        if emails and len(emails) > 0:
            print(f"\nВсего писем в ящике: {len(emails)}")
            for i, email in enumerate(emails):
                print(f"\nПисьмо #{i+1}:")
                #print(f"От: {email._from}")
                print(f"Тема: {email.subject}")
                print(f"Дата: {email.created_at}")
                email_controller = mailslurp_client.EmailControllerApi(api_client)
                email_content = email_controller.get_email(email.id)
                text_content = email_content.body
                
                d=3
                print(f"Содержание:\n{text_content}")
        else:
            print("В ящике нет писем.")
    
   


# Функция для проверки всех писем в ящике
def check_inbox(inbox_id):
    MAILSLURP_API_KEY = "f1d6106c5464c6751a87cbee9cdee5290403ce9874fa9e4c4d4e3cc501caa6a9"  # Замените на ваш API ключ
    
    config = Configuration()
    config.api_key['x-api-key'] = MAILSLURP_API_KEY
    api_client = ApiClient(config)
    
    inbox_controller = InboxControllerApi(api_client)
    
    # Получаем все письма  e737762b-6b1a-45c8-900b-ab826e1208f0
    emails = inbox_controller.get_emails(inbox_id)
    #emails = inbox_controller.get_emails("e737762b-6b1a-45c8-900b-ab826e1208f0")
    print(f"Найдено {len(emails)} писем в ящике")
    
    for i, email in enumerate(emails):
        print(f"\nПисьмо #{i+1}:")
        print(f"ID: {email.id}")
        print(f"От: {email.from_}")
        print(f"Тема: {email.subject}")
        print(f"Получено: {email.created_at}")
        

        #emails = inbox_controller.get_emails(inbox_id)
        # Получить полное содержание письма
        email_controller = mailslurp_client.EmailControllerApi(api_client)
        email_content = email_controller.get_email(email.id)
        text_content = email_content.body
        print(f"Содержание:\n{text_content}")

if __name__ == "__main__":
    # Исполняем пример создания почты
    inbox_info = create_email_example()
    
    # Дополнительные операции с созданным ящиком
    while True:
        print("\nДополнительные действия:")
        print("1. Создать почту")
        print("2. Проверить входящие письма")
        print("3. Выйти")
        
        choice = input("Выберите действие (1-3): ")
        
        if choice == "1":
            inbox_info = create_email_example()
        elif choice == "2":
            check_inbox(inbox_info["inbox_id"])
        elif choice == "3":
            print("Завершение программы...")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")