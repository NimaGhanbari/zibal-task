from apps.notifications.services.notificatoin_sender_service import SMSNotifier, EmailNotifier, WebPushNotifier


class NotificationService:
    _notifier_mapping = {
        "sms": SMSNotifier,
        "email": EmailNotifier,
        "webpush": WebPushNotifier,
    }

    @staticmethod
    def send_notification(notifier, receiver, count, amount):
        notifier.send(receiver=receiver, count=count, amount=amount)

