from datetime import datetime
from logging import getLogger

import aiohttp

from apps.notifications.utils.transaction_group import TransactionGroup
from zibal_project.settings import EXTERNAL_API_URL, EXTERNAL_API_KEY

logger = getLogger(__name__)


class TransactionRepository:

    @staticmethod
    async def get_today_transactions(today: datetime.date):
        url = f"{EXTERNAL_API_URL}/transactions"
        headers = {"Authorization": EXTERNAL_API_KEY}
        params = {
            "start_date": f"{today}T00:00:00",
            "end_date": f"{today}T23:59:59",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

        try:
            transactions = TransactionGroup.group_transactions(data)
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return []

        return transactions
