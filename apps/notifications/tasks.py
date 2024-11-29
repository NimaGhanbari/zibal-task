import asyncio
from datetime import datetime
from logging import getLogger

from celery import shared_task

from apps.notifications.services.notificatoin_sender_service import SMSNotifier, EmailNotifier, WebPushNotifier
from apps.notifications.services.transaction_information_service import TransactionRepository
from apps.notifications.services.user_repository import UserRepository
from apps.notifications.utils.transaction_valodator import TransactionValidator

logger = getLogger(__name__)


@shared_task(bind=True)
async def send_notification_task():
    # The comments aren't very good, which is why I don't use code comment.

    today_date = datetime.now().date()
    transactions = await TransactionRepository.get_today_transactions(today_date)
    user_repo = UserRepository()

    async def process_transaction(transaction):
        user_contact = await user_repo.get_user_contact(transaction['merchant_id'], transaction['types'])

        notifier_dict = {
            'email': {
                'valid_condition': lambda: 'email' in user_contact and user_contact[
                    'email'] and TransactionValidator.is_valid_email(user_contact['email']),
                'notifier': EmailNotifier(),
                'send': lambda: EmailNotifier().send(email=user_contact['email'], count=transaction['count'],
                                                     amount=transaction['amount'])
            },
            'phone': {
                'valid_condition': lambda: 'phone' in user_contact and user_contact[
                    'phone'] and TransactionValidator.is_valid_phone_number(user_contact['phone']),
                'notifier': SMSNotifier(),
                'send': lambda: SMSNotifier().send(phone=user_contact['phone'], count=transaction['count'],
                                                   amount=transaction['amount'])
            },
            'web_push': {
                'valid_condition': lambda: 'fcm_token' in user_contact and user_contact['fcm_token'],
                'notifier': WebPushNotifier(),
                'send': lambda: WebPushNotifier().send(fcm_token=user_contact['fcm_token'], count=transaction['count'],
                                                       amount=transaction['amount'])
            }
        }

        for medium_type in transaction['types']:
            if notifier_dict[medium_type]['valid_condition']():
                try:
                    await notifier_dict[medium_type]['send']()
                except Exception as e:
                    logger.error(f"Error sending {medium_type} notification: {str(e)}")

            else:
                logger.error(f"Invalid {user_contact.get(medium_type)}")

    await asyncio.gather(*(process_transaction(transaction) for transaction in transactions))
