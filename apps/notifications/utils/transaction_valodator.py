import re


class TransactionValidator:

    @staticmethod
    def is_valid_phone_number(phone: str) -> bool:
        phone_pattern = r'^(?:\+98|0)?9\d{9}$'
        return bool(re.match(phone_pattern, phone))

    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
