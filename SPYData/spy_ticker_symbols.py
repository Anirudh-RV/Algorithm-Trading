import traceback
from typing import Tuple

import pandas as pd
import requests


def spy_tickers() -> Tuple[pd.DataFrame, bool]:
    """
    Provides all the tickers in the S&P 500 Index

    Args:
        None

    Returns:
        Tuple[pd.DataFrame, bool]: A pandas dataframe of all the ticker prices and a Status
    """

    try:
        response = requests.get(
            "https://www.wikitable2json.com/api/List_of_S%26P_500_companies#S&P_500_component_stocks?table=0"
        )
        if response.status_code == 200:
            json_response = response.json()
            headers = json_response[0][0]
            data = json_response[0][1:]
            spy_df = pd.DataFrame(data, columns=headers)
            spy_ticker_df = spy_df[["Symbol"]]
            return spy_ticker_df, True
        else:
            print(
                f"Response from API: {response}\nResponse Code: {response.status_code}"
            )
            return pd.DataFrame(), False
    except Exception:
        print(traceback.format_exc())
        return pd.DataFrame(), False
