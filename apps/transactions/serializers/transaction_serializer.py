from rest_framework import serializers


class TransactionResultSerializer(serializers.Serializer):
    date = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_date(self, obj):
        date_parts = obj["_id"]
        date_type = self.context.get("date_type")

        date_formatters = {
            'daily': lambda dp: f"{dp['year']}/{dp['month']:02d}/{dp['day']:02d}",
            'weekly': lambda dp: f"{dp['year']} هفته {dp['week']} سال ",
            'monthly': lambda dp: f"{dp['year']}-{dp['month']:02d}",
        }

        return date_formatters.get(date_type, lambda _: "")(date_parts)

    def get_value(self, obj):
        return obj.get("result", 0)