from zibal_project.settings import KAVENEGAR_APP
from logging import getLogger
import aiohttp

logger = getLogger(__name__)


class SMSProvider:
    def __init__(self, name: str):
        self.name = name
        self.provider = self._get_provider(name)

    @classmethod
    def _get_provider(cls, name: str):
        if name == "kavenegar":
            return KavenegarProvider(name)
        elif name == "farazsms":
            return FarazSMSProvider(name)
        elif name == "payamfa":
            return PayamFaProvider(name)
        else:
            raise ValueError(f"Unsupported SMS provider: {name}")

    async def send_sms(self, phone: str, message: str) -> bool:
        raise NotImplementedError("Subclasses must implement the send_sms method.")


class KavenegarProvider(SMSProvider):

    def __init__(self, name: str):
        super().__init__(name)

    async def send_sms(self, phone: str, message: str) -> bool:

        params = {
            'sender': '90003723',
            'receptor': phone,
            'message': message + '\n' + 'لغو 11',
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.kavenegar.com/v1/YOUR_API_KEY/sms/send.json',
                                        data=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        is_send_list_value = [1, 2, 4, 5]  # Kavenegar successful statuses
                        if data[0]['status'] in is_send_list_value:
                            logger.info(f"Message sent successfully to {phone}")
                            return True
                        else:
                            logger.error(f"Failed to send message to {phone}. Status: {data[0]['status']}")
        except Exception as e:
            logger.error(f"Unexpected error while sending SMS: {e}")

        return False


class FarazSMSProvider(SMSProvider):

    def __init__(self, name: str):
        super().__init__(name)

    async def send_sms(self, phone: str, message: str) -> bool:
        # Send SMS using FarazSMS API.
        pass


class PayamFaProvider(SMSProvider):

    def __init__(self, name: str):
        super().__init__(name)

    async def send_sms(self, phone: str, message: str) -> bool:
        # Send SMS using PayamFa API.
        pass