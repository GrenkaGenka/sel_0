import time
from mailslurp_client import ApiClient, Configuration, InboxControllerApi, WaitForControllerApi
import mailslurp_client

class MailSlurpClient:
    def __init__(self):
        self.config = Configuration()
        self.inbox_id = None
        #self.config.api_key['x-api-key'] = self.api_key
        MAILSLURP_API_KEY = "f1d6106c5464c6751a87cbee9cdee5290403ce9874fa9e4c4d4e3cc501caa6a9"
        self.config = Configuration()
        self.config.api_key['x-api-key'] = MAILSLURP_API_KEY
        self.api_client = ApiClient(self.config)
        self.inbox_controller = InboxControllerApi(self.api_client)
        self.wait_controller = WaitForControllerApi(self.api_client)



    def create_email(self):


        # 1. Настройка MailSlurp API
        # MAILSLURP_API_KEY = "f1d6106c5464c6751a87cbee9cdee5290403ce9874fa9e4c4d4e3cc501caa6a9"
        # config = Configuration()
        # config.api_key['x-api-key'] = MAILSLURP_API_KEY
        # api_client = ApiClient(config)
        # inbox_controller = InboxControllerApi(api_client)
        # wait_controller = WaitForControllerApi(api_client)
        


        # 3. Создание нового почтового ящика
        print("Создание нового временного почтового ящика...")
        inbox = self.inbox_controller.create_inbox()
        
        # 4. Получение данных почтового ящика
        self.inbox_id = inbox.id
        email_address = inbox.email_address 
        print(f"Создан почтовый ящик:")
        print(f"- ID: {self.inbox_id}")
        print(f"- Email адрес: {email_address}")
        

    def check_inbox(self):


        # MAILSLURP_API_KEY = "f1d6106c5464c6751a87cbee9cdee5290403ce9874fa9e4c4d4e3cc501caa6a9"
        # config = Configuration()
        # config.api_key['x-api-key'] = MAILSLURP_API_KEY
        # api_client = ApiClient(config)
        # inbox_controller = InboxControllerApi(api_client)
        # wait_controller = WaitForControllerApi(api_client)



        emails = self.inbox_controller.get_emails(self.inbox_id)
        
        if emails and len(emails) > 0:
            print(f"\nВсего писем в ящике: {len(emails)}")
            for i, email in enumerate(emails):
                print(f"\nПисьмо #{i+1}:")
                #print(f"От: {email._from}")
                print(f"Тема: {email.subject}")
                print(f"Дата: {email.created_at}")
                email_controller = mailslurp_client.EmailControllerApi(self.api_client)
                email_content = email_controller.get_email(email.id)
                text_content = email_content.body
                
                d=3
                print(f"Содержание:\n{text_content}")
        else:
            print("В ящике нет писем.")
    
   