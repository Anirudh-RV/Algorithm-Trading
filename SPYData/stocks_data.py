import os
import sys

sys.path.append(os.path.abspath(".."))

import traceback
from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd
import requests

from constants import POLYGON_API_ADJUSTED, POLYGON_API_KEY
from SPYData.market_cap_list import MARKET_CAP
from SPYData.ticker_symbols import spy_tickers
from StockMarketData.market_information import (
    convert_stock_list_to_dictionary, stock_market_stocks)
from StockMarketData.stock_market_default_prices import SANDBOX_STOCK_MARKET


def spy_ticker_market_cap(
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
        return MARKET_CAP[ticker_symbol], True
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


def spy_stock_data(sandbox: bool = False) -> Tuple[pd.DataFrame, bool]:
    """
    Provides the SPY stocks data

    If, sandbox, the function will return the same values but with fixed
    historical stock prices

    Defaults to sandbox=False

    Args:
        sandbox(str): If we need to use sandbox.

    Returns:
        Tuple[pd.DataFrame, bool]: The SPY stock data and status
        pd.DataaFrame columns: ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Purchase']
    """

    stock_market_data = SANDBOX_STOCK_MARKET
    if not sandbox:
        last_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        stock_market_data, status = stock_market_stocks(
            date=last_date, sandbox=sandbox
        )
        if not status:
            print("Issue getting stock market information")
            return pd.DataFrame(), False

    spy_tickers_data_frame, status = spy_tickers()
    if not status:
        print("SPY tickers not found")
        return pd.DataFrame(), False

    dataframe_columns = [
        "Ticker",
        "Stock Price",
        "Market Capitalization",
        "Number of Shares to Purchase",
    ]
    spy_data_frame = pd.DataFrame(columns=dataframe_columns)
    stock_market_dictionary = convert_stock_list_to_dictionary(
        stock_market_list=stock_market_data["results"]
    )

    for _, row in spy_tickers_data_frame.iterrows():
        market_cap, status = spy_ticker_market_cap(
            row["Symbol"], sandbox=sandbox
        )
        if not status:
            print(f"Could not find market cap for: {row['Symbol']}")
            return pd.DataFrame(), False
        spy_data_frame.loc[len(spy_data_frame)] = [
            row["Symbol"],
            stock_market_dictionary[row["Symbol"]]["c"],
            market_cap,
            "N/A",
        ]

    return spy_data_frame, True
