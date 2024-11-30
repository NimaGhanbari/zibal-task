import re
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.transactions.serializers.transaction_serializer import TransactionResultSerializer
from zibal_project.settings import db_client


class GetTransactionData(APIView):
    transaction_collection = db_client['transaction']
    merchant_collection = db_client['users']
    serializer_class = TransactionResultSerializer

    def get(self, request, *args, **kwargs):
        mode = request.query_params.get('mode')
        transaction_type = request.query_params.get('type')
        merchant_id = request.query_params.get('merchant_id')

        if mode not in ['daily', 'weekly', 'monthly']:
            return Response({"detail": "Invalid mode. Must be 'daily', 'weekly', or 'monthly'."},
                            status=status.HTTP_400_BAD_REQUEST)

        if transaction_type not in ['count', 'amount']:
            return Response({"detail": "Invalid type. Must be 'count' or 'amount'."},
                            status=status.HTTP_400_BAD_REQUEST)

        filter_query = {}
        if merchant_id:
            if len(merchant_id) != 24 or not re.match('^[0-9a-fA-F]{24}$', merchant_id):
                return Response({"detail": "Invalid merchant_id format. Must be a 24-character hex string."},
                                status=status.HTTP_400_BAD_REQUEST)
            merchant_object_id = ObjectId(merchant_id)
            if not self.merchant_collection.find_one({"_id": merchant_object_id}):
                return Response({"detail": "Merchant with the given ID not found."}, status=status.HTTP_404_NOT_FOUND)
            filter_query['user_merchantid'] = merchant_object_id

        now = datetime.now()
        date_config = {
            'daily': {
                'start_date': now - timedelta(days=30),
                'group_by': {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"},
                },
            },
            'weekly': {
                'start_date': now - timedelta(weeks=24),
                'group_by': {
                    "year": {"$year": "$created_at"},
                    "week": {"$week": "$created_at"},
                },
            },
            'monthly': {
                'start_date': now - timedelta(days=365),
                'group_by': {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                },
            },
        }

        config = date_config[mode]
        filter_query['created_at'] = {"$gte": config['start_date']}

        pipeline = [
            {"$match": filter_query},
            {
                "$group": {
                    "_id": config['group_by'],
                    "result": {"$sum": "$amount"} if transaction_type == 'amount' else {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}}
        ]

        results = list(self.transaction_collection.aggregate(pipeline))
        serializer = self.serializer_class(results, many=True, context={"mode": mode})
        return Response(serializer.data, status=status.HTTP_200_OK)
