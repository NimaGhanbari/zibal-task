from datetime import datetime
from logging import getLogger

from apps.notifications.services.base_email_provider import EmailProvider
from apps.notifications.services.base_sms_provider import SMSProvider
from apps.notifications.utils.create_sms_message import create_message
from zibal_project.settings import db_client

logger = getLogger(__name__)


class BaseNotifier:

    async def send(self, merchant_id: str, count: int, amount: float):
        raise NotImplementedError("Send method must be implemented by subclasses.")


class SMSNotifier(BaseNotifier):

    def __init__(self):
        self.providers = [
            SMSProvider("kavenegar"),
            SMSProvider("farazsms"),
            SMSProvider("payamfa")
        ]
        self.provider_index = 0

    def _get_next_provider(self) -> SMSProvider:

        provider = self.providers[self.provider_index]
        self.provider_index = (self.provider_index + 1) % len(self.providers)
        return provider

    async def _send_with_retry(self, phone: str, message: str, retries: int = 3) -> bool:

        sms_log_collection = db_client["sms_log"]

        for attempt in range(retries):
            provider = self._get_next_provider()
            status = await provider.send_sms(phone, message)

            report = {
                "phone": phone,
                "message": message,
                "attempt": attempt + 1,
                "provider": provider.name,
                "is_sent": status,
                "timestamp": datetime.now(),
            }

            sms_log_collection.insert_one(report)

            if status:
                return True

        return False

    async def send(self, phone, count, amount):
        message = create_message(count, amount)
        for _ in range(len(self.providers)):
            await self._send_with_retry(phone, message)


class EmailNotifier(BaseNotifier):

    def __init__(self):
        self.providers = [
            EmailProvider("SMTP"),
            EmailProvider("IMAP")
        ]
        self.provider_index = 0

    def _get_next_provider(self) -> EmailProvider:

        provider = self.providers[self.provider_index]
        self.provider_index = (self.provider_index + 1) % len(self.providers)
        return provider

    async def _send_with_retry(self, email: str, message: str, retries: int = 2) -> bool:

        email_log_collection = db_client["email_log"]
        for attempt in range(retries):
            provider = self._get_next_provider()
            status = await provider.send_email(email, message)

            report = {
                "email": email,
                "message": message,
                "attempt": attempt + 1,
                "provider": provider.name,
                "is_sent": status,
                "timestamp": datetime.now(),
            }

            email_log_collection.insert_one(report)

            if status:
                return True

        return False

    async def send(self, email, count, amount):
        message = create_message(count, amount)
        for _ in range(len(self.providers)):
            await self._send_with_retry(email, message)


class WebPushNotifier(BaseNotifier):
    def send(self, fcm_token, count, amount):
        print(f"Sending WebPush to merchant {fcm_token}: Count={count}, Amount={amount}")
        pass
