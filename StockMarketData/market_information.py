import os
import random
import sys
import traceback
from typing import Tuple

sys.path.append(os.path.abspath(".."))

import requests
from stock_market_default_prices import SANDBOX_STOCK_MARKET

from constants import POLYGON_API_ADJUSTED, POLYGON_API_KEY


def ticker_stock_price_data(
    ticker_symbol: str, sandbox: bool = False
) -> Tuple[Tuple[float, float, float], bool]:
    """
    Provides the previous day's low, high and close price for the Ticker symbol
    If, sandbox, the function will return the same values but with default data
    Defaults to sandbox=False

    Args:
        ticker_symbol (str): The ticker symbol.
        sandbox (bool): If we need to use sandbox.

    Returns:
        Tuple[Tuple[float, float, float], bool]:
        The tuple of (low, high, close) stock prices and a Status
    """

    if sandbox:
        sandbox_stocks = SANDBOX_STOCK_MARKET["results"]
        for sandbox_stock in sandbox_stocks:
            if sandbox_stock["T"] == ticker_symbol:
                price_low, price_high, price_close = (
                    sandbox_stock["l"],
                    sandbox_stock["h"],
                    sandbox_stock["c"],
                )
        return (price_low, price_high, price_close), True
    else:
        try:
            response = requests.get(
                f"https://api.polygon.io/v2/aggs/ticker/{ticker_symbol}/prev?adjusted={POLYGON_API_ADJUSTED}&apiKey={POLYGON_API_KEY}"
            )
            if response.status_code == 200:
                json_response = response.json()
                stock_price_results = json_response["results"][0]
                price_low, price_high, price_close = (
                    float(stock_price_results["l"]),
                    float(stock_price_results["h"]),
                    float(stock_price_results["c"]),
                )
                return (price_low, price_high, price_close), True
            else:
                print(
                    f"API Response: {response}\nResponse Code: {response.status_code}"
                )
                return (0.0, 0.0, 0.0), False
        except Exception:
            print(traceback.format_exc())
            return (0.0, 0.0, 0.0), False
