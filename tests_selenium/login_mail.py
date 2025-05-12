import logging
import mailslurp_client
from mailslurp_client import ApiClient, Configuration, InboxControllerApi, WaitForControllerApi

# Замените на свой API-ключ MailSlurp
MAILSLURP_API_KEY = "f493f0ce89a668a6b6d9a4347e9d99ab705be5f96e8cf4cd04c3a818f37cc011"


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("market_kg_test.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


class MailSlurpClient:
    """Класс для работы с MailSlurp API"""

    def __init__(self):
        self.config = Configuration()
        self.inbox_id = None
        self.config = Configuration()
        self.config.api_key['x-api-key'] = MAILSLURP_API_KEY
        self.api_client = ApiClient(self.config)
        self.inbox_controller = InboxControllerApi(self.api_client)
        self.wait_controller = WaitForControllerApi(self.api_client)

    def create_email(self):
        """Создает временный почтовый ящик и возвращает его адрес электронной почты"""
        try:
            logger.info("Создание нового временного почтового ящика...")
            inbox = self.inbox_controller.create_inbox()
            self.inbox_id = inbox.id
            email_address = inbox.email_address
            logger.info(f"Создан почтовый ящик:")
            logger.info(f"- ID: {self.inbox_id}")
            logger.info(f"- Email адрес: {email_address}")
            return email_address
        except mailslurp_client.ApiException as e:
            logger.error(f"Ошибка при создании почтового ящика: {e}")
            return None

    def check_inbox(self):
        """Проверяет наличие писем в почтовом ящике"""
        try:
            emails = self.inbox_controller.get_emails(self.inbox_id)
        
        except mailslurp_client.ApiException as e:
            logger.error(f"Ошибка при получении писем: {e}")
            return None

        if emails and len(emails) > 0:
            for i, email in enumerate(emails):
                email_controller = mailslurp_client.EmailControllerApi(
                    self.api_client)
                email_content = email_controller.get_email(email.id)
                text_content = email_content.body
                logger.info(f"Письмо получено")
                return text_content
        else:
            logger.info("Почтовый ящик пуст")
            return None
