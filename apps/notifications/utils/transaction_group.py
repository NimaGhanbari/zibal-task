class TransactionGroup:

    @staticmethod
    def group_transactions(data):
        grouped = []

        for transaction in data:
            key = (transaction["types"], transaction["merchant_id"])
            types = transaction["types"].split(",")

            if key not in grouped:
                grouped.append({
                    "types": types,
                    "merchant_id": transaction["merchant_id"],
                    "count": 0,
                    "amount": 0,
                })
            grouped[-1]["count"] += 1
            grouped[-1]["amount"] += transaction["amount"]

        return grouped
