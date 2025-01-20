from datetime import datetime


def style(date: datetime) -> str:
    """
    This function is used to style the date
    """
    return date.strftime("%d-%m-%Y")
