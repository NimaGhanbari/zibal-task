from zibal_project.settings import db_client_io, DB_NAME


class UserRepository:
    def __init__(self):
        self.db = db_client_io[DB_NAME]
        self.users_collection = self.db["users"]

    async def get_user_contact(self, merchant_id: str, types: list) -> dict:

        user = await self.users_collection.find_one({"merchant_id": merchant_id},
                                                    {"email": 1, "phone": 1, "fcm_token": 1, "_id": 0})
        if not user:
            raise ValueError(f"No user found with merchant_id {merchant_id}")

        result = {}

        if 'email' in types and 'email' in user and user['email']:
            result['email'] = user['email']
        if 'phone' in types and 'phone' in user and user['phone']:
            result['phone'] = user['phone']
        if 'web_push' in types and 'fcm_token' in user and user['fcm_token']:
            result['fcm_token'] = user['fcm_token']

        return result
