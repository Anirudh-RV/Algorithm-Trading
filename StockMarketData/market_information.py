import os
import random
import sys
import traceback
from typing import Tuple

sys.path.append(os.path.abspath(".."))

import requests

from constants import POLYGON_API_ADJUSTED, POLYGON_API_KEY
from StockMarketData.stock_market_default_prices import SANDBOX_STOCK_MARKET


def convert_stock_list_to_dictionary(stock_market_list: list) -> dict:
    """
    Converts the list of stocks into a dictionary for quick look up

    Args:
        stock_market_list(list): The list of stock information

    Returns:
        dict: The same data in dictionary form for quick access
    """
    return {stock_data["T"]: stock_data for stock_data in stock_market_list}


def stock_market_stocks(date: str, sandbox: bool = False) -> Tuple[dict, bool]:
    """
    Provides the stock market information for a particular date
    If, sandbox, the function will return the stock market price for a default date
    Defaults to sandbox=False

    Args:
        date (str): The date for the stock market data.
        sandbox (bool): If we need to use sandbox.

    Returns:
        Tuple[dict, bool]: Stock market data and a Status
    """
    if sandbox:
        return SANDBOX_STOCK_MARKET
    try:
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted={POLYGON_API_ADJUSTED}&apiKey={POLYGON_API_KEY}"
        )
        return response.json(), True
    except Exception:
        print(traceback.format_exc())
        return dict(), False


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
