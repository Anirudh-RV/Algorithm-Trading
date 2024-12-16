import random
import traceback
from typing import Tuple

import requests
from constants import POLYGON_API_ADJUSTED, POLYGON_API_KEY
from spy_market_cap_list import MARKET_CAP


def previous_low_high_close_prices(
    ticker_symbol: str, sandbox: bool = False
) -> Tuple[Tuple[float, float, float], bool]:
    """
    Provides the previous day's low, high and close price for the Ticker symbol
    If, sandbox, the function will return the same values but with random data
    Defaults to sandbox=False

    Args:
        ticker_symbol (str): The ticker symbol.
        sandbox (bool): If we need to use sandbox.

    Returns:
        Tuple[Tuple[float, float, float], bool]:
        The tuple of (low, high, close) stock prices and a Status
    """

    if sandbox:
        random_stock_price = round(random.uniform(10.0, 300.0), 2)
        random_average_movement_percentage = round(random.uniform(1.0, 2.0), 4)
        max_movement = round(
            (random_stock_price / 100) * random_average_movement_percentage, 2
        )
        movement_down = round(random.uniform(0.0, max_movement), 2)
        movement_up = round(random.uniform(0.0, max_movement), 2)
        close_price_randomness = round(random.uniform(0.0, max_movement), 2)
        priceLow = round(random_stock_price - movement_down, 2)
        priceHigh = round(random_stock_price + movement_up, 2)
        priceClose = round(priceLow + close_price_randomness, 2)
        return (priceLow, priceHigh, priceClose), True
    else:
        try:
            response = requests.get(
                f"https://api.polygon.io/v2/aggs/ticker/{ticker_symbol}/prev?adjusted={POLYGON_API_ADJUSTED}&apiKey={POLYGON_API_KEY}"
            )
            if response.status_code == 200:
                json_response = response.json()
                stockPriceResults = json_response["results"][0]
                priceLow, priceHigh, priceClose = (
                    float(stockPriceResults["l"]),
                    float(stockPriceResults["h"]),
                    float(stockPriceResults["c"]),
                )
                return (priceLow, priceHigh, priceClose), True
            else:
                print(
                    f"API Response: {response}\nResponse Code: {response.status_code}"
                )
                return (0.0, 0.0, 0.0), False
        except Exception:
            print(traceback.format_exc())
            return (0.0, 0.0, 0.0), False


def market_cap(
    ticker_symbol: str, sandbox: bool = False
) -> Tuple[float, bool]:
    """
    Provides the market capitalization for the Ticker symbol
    If, sandbox, the function will return the same values but with fixed
    historical market cap
    Defaults to sandbox=False

    Args:
        ticker_symbol (str): The ticker symbol.
        sandbox(str): If we need to use sandbox.

    Returns:
        Tuple[float, bool]: The tuple of the Market Capitalization and Status
    """

    if sandbox:
        print(MARKET_CAP[ticker_symbol])
        return MARKET_CAP[ticker_symbol]
    else:
        try:
            response = requests.get(
                f"https://api.polygon.io/v3/reference/tickers/{ticker_symbol}?apiKey={POLYGON_API_KEY}"
            )
            if response.status_code == 200:
                json_response = response.json()
                return float(json_response["results"]["market_cap"]), True
            else:
                print(
                    f"API Response: {response}\nResponse Code: {response.status_code}"
                )
                return 0.0, False
        except Exception:
            print(traceback.format_exc())
            return 0.0, False
