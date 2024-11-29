from logging import getLogger

logger = getLogger(__name__)


class EmailProvider:
    def __init__(self, name: str):
        self.name = name
        self.provider = self._get_provider(name)

    @classmethod
    def _get_provider(cls, name: str):
        if name == "SMTP":
            return SMTPProvider(name)
        elif name == "IMAP":
            return IMAPProvider(name)
        else:
            raise ValueError(f"Unsupported Email provider: {name}")
    async def send_email(self, email: str, message: str) -> bool:
        raise NotImplementedError("Subclasses must implement the send_email method.")


class SMTPProvider(EmailProvider):

    def __init__(self, name: str):
        super().__init__(name)

    async def send_email(self, email: str, message: str) -> bool:
        pass


class IMAPProvider(EmailProvider):

    def __init__(self, name: str):
        super().__init__(name)

    async def send_email(self, email: str, message: str) -> bool:
        # Send Email using IMAP Protocol.
        pass

