from datetime import datetime
from typing import Tuple

from dateutil.relativedelta import relativedelta


def get_dates_in_format_for_change_window(
    change_window: str,
) -> Tuple[str, str]:
    """
    Returns current date and the past date based on the change window

    Args:
        change_window (str): The change window for the dates

        change_window options:
                'maxChange': 20 year change
                '5year': 5 year change
                '1year': 1 year change
                'ytd': Year to date change
                '6month': 6 month change
                '3month': 3 month change
                '1month': 1 month change
                '30day': 30 day change
                '15day': 15 day change
                '5day': 5 day change
                '1day': 1 day change

    Returns:
        Outputs a CSV sheet with the portfolio suggestion
    """

    current_date = datetime.now() - relativedelta(days=1)
    current_date_in_format = current_date.strftime("%Y-%m-%d")
    if change_window == "maxChange":
        past_date = current_date - relativedelta(years=20)
    elif change_window == "5year":
        past_date = current_date - relativedelta(years=5)
    elif change_window == "1year":
        past_date = current_date - relativedelta(years=1)
    elif change_window == "ytd":
        past_date = datetime(current_date.year, 1, 1)
    elif change_window == "6month":
        past_date = current_date - relativedelta(months=6)
    elif change_window == "3month":
        past_date = current_date - relativedelta(months=3)
    elif change_window == "1month":
        past_date = current_date - relativedelta(months=1)
    elif change_window == "30day":
        past_date = current_date - relativedelta(days=30)
    elif change_window == "15day":
        past_date = current_date - relativedelta(days=15)
    elif change_window == "5day":
        past_date = current_date - relativedelta(days=5)
    elif change_window == "1day":
        past_date = current_date - relativedelta(days=1)
    past_date_in_format = past_date.strftime("%Y-%m-%d")

    return current_date_in_format, past_date_in_format
