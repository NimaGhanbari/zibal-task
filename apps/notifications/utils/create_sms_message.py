import jdatetime


def create_message(count, amount) -> str:
    today_jalali_date = jdatetime.datetime.today().strftime('%d %B %Y')

    message = (
        f"با سلام و احترام،\n\n"
        f"مبلغ {amount} ریال برای {count} مورد به ثبت رسید.\n"
        f"تاریخ امروز: {today_jalali_date}\n\n"
        f"با تشکر از شما\n"
        f"تیم پشتیبانی"
    )

    return message
