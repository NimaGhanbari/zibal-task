from django.urls import path,include

urlpatterns = [
    path("transaction/", include("apps.transactions.apis.urls")),
]
