from django.urls import path

from apps.transactions.apis.transaction_view import GetTransactionData

urlpatterns = [
    path("get-list", GetTransactionData.as_view(), name="get-list"),
]
