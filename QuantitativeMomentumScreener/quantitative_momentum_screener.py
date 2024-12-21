import os
import sys
import traceback

sys.path.append(os.path.abspath(".."))

import math
from typing import Tuple

import pandas as pd

from SPYData.ticker_symbols import spy_tickers
from StockMarketData.market_information import (
    convert_stock_list_to_dictionary, stock_market_stocks)
from StockMarketData.stock_market_default_year_prices import (
    STOCK_MARKET_DAY_0_PRICES, STOCK_MARKET_YEAR_AGO_PRICES)
from Utils.date_utils import get_dates_in_format_for_change_window


def price_return_for_stocks(
    change_window: str,
    portfolio_size: int,
    current_date: str,
    past_date: str,
    spy_only: bool = False,
    sandbox: bool = False,
) -> Tuple[pd.DataFrame, list, bool]:
    """
    Calculates the price return for all stocks between the past_date and current_date
    If sandbox=True, uses sandbox stocks
    If spy_only=True, uses only SPY Stocks

    Args:
        change_window (str): Change window
        portfolio_size (int): Size of portfolio
        spy_only (bool): If we need to use only SPY stocks
        current_date (str): Current date
        past_date (str): Past date
        sandbox(bool): If we need to use Sandbox

    Returns:
        Tuple[pd.DataFrame, list, bool]:
        A DataFrame ['Ticker', 'Price', 'Price Rerturn for TimePeriod', ' Number of shares to Buy']
        and a List of unavailable stocks
        and a Status
    """

    spy_stocks_set = set()
    if spy_only:
        spy_stocks_list, status = spy_tickers()
        if not status:
            print("Could not get SPY tickers")
            return pd.DataFrame(), False
        spy_stocks_set = set(spy_stocks_list["Symbol"].to_list())

    stocks_at_current_date = STOCK_MARKET_DAY_0_PRICES
    stocks_at_past_date = STOCK_MARKET_YEAR_AGO_PRICES
    if not sandbox:
        stocks_at_current_date, status = stock_market_stocks(
            date=current_date, sandbox=sandbox
        )
        if not status:
            print("Could not get stock data for current date")
            return pd.DataFrame(), False
        stocks_at_past_date, status = stock_market_stocks(
            date=past_date, sandbox=sandbox
        )
        if not status:
            print("Could not get stock data for past date")
            return pd.DataFrame(), False

    stocks_at_current_date_dictionary = convert_stock_list_to_dictionary(
        stock_market_list=stocks_at_current_date["results"]
    )
    stocks_at_past_date_dictionary = convert_stock_list_to_dictionary(
        stock_market_list=stocks_at_past_date["results"]
    )

    dataframe_columns = [
        "Ticker",
        "Stock Price",
        f"Percent Change over: {change_window}",
        "Number of Shares to Purchase",
    ]
    portfolio_data_frame = pd.DataFrame(columns=dataframe_columns)

    stocks_unavailable_in_the_past = []
    for key, values in stocks_at_current_date_dictionary.items():
        try:
            if spy_only and key not in spy_stocks_set:
                continue
            if not stocks_at_past_date_dictionary.get(key):
                stocks_unavailable_in_the_past.append(key)
                continue
            past_price = stocks_at_past_date_dictionary[key]["c"]
            current_price = values["c"]
            percentage_change = (
                (current_price - past_price) / past_price
            ) * 100
            portfolio_data_frame.loc[len(portfolio_data_frame)] = [
                key,
                current_price,
                round(percentage_change, 2),
                "N/A",
            ]
        except Exception:
            print(traceback.format_exc())
            return pd.DataFrame(), False

    portfolio_data_frame.sort_values(
        f"Percent Change over: {change_window}", ascending=False, inplace=True
    )
    portfolio_data_frame.reset_index(drop=True, inplace=True)
    portfolio_data_frame = portfolio_data_frame[:portfolio_size]

    return portfolio_data_frame, stocks_unavailable_in_the_past, True


def append_additional_stats(
    portfolio_data_frame: pd.DataFrame,
    portfolio_amount: float,
    capital_invested: float,
    stocks_unavailable_in_the_past: list,
) -> None:
    """
    Does in place update of the portfolio_data_frame to add additional statistics of the portfolio

    Args:
        portfolio_data_frame (pd.DataFrame): The DataFrame to be modified
        portfolio_amount (float): The portfolio amount
        capital_invested (float): The total capital invested
        stocks_unavailable_in_the_past (list): The stocks which were unavailable in the past to calculate

    Returns:
        None
        In place change to DataFrame
    """

    portfolio_data_frame.loc[len(portfolio_data_frame)] = [
        "",
        "",
        "",
        "",
    ]

    portfolio_data_frame.loc[len(portfolio_data_frame)] = [
        "Total Capital:",
        portfolio_amount,
        "",
        "",
    ]
    portfolio_data_frame.loc[len(portfolio_data_frame)] = [
        "Capital invested:",
        round(capital_invested, 2),
        "",
        "",
    ]
    portfolio_data_frame.loc[len(portfolio_data_frame)] = [
        "Capital remaining:",
        round(portfolio_amount - capital_invested, 2),
        "",
        "",
    ]

    portfolio_data_frame.loc[len(portfolio_data_frame)] = [
        "Stocks not available in the past to evaluate (Count):",
        len(stocks_unavailable_in_the_past),
        "",
        "",
    ]

    portfolio_data_frame.loc[len(portfolio_data_frame)] = [
        "Stocks not available in the past to evaluate (List):",
        str(stocks_unavailable_in_the_past),
        "",
        "",
    ]


def quantitative_momentum_portfolio(
    portfolio_amount: float,
    portfolio_size: int,
    change_window: str = "1year",
    spy_only: bool = False,
    sandbox: bool = False,
):
    """
    Quantitative Momentum Portfolio for a given time window

    Args:
        portfolio_amount(float): The '$' amount of the portfolio
        portfolio_size(int): The number of stocks we want in our portfolio
        change_window (str): The time window to be used to calculate Quantitative Momentum
        spy_only (bool): If we should use only SPY stocks
        sandbox(bool): If we should use the sandbox or not

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

    current_date_in_format, past_date_in_format = (
        get_dates_in_format_for_change_window(change_window=change_window)
    )

    portfolio_data_frame, stocks_unavailable_in_the_past, status = (
        price_return_for_stocks(
            change_window=change_window,
            portfolio_size=portfolio_size,
            current_date=current_date_in_format,
            past_date=past_date_in_format,
            spy_only=spy_only,
            sandbox=sandbox,
        )
    )
    if not status:
        print("Could not get percent change data")
        return

    capital_invested = 0
    position_size = portfolio_amount / portfolio_size
    for index, row in portfolio_data_frame.iterrows():
        portfolio_data_frame.loc[index, "Number of Shares to Purchase"] = (
            math.floor(position_size / row["Stock Price"])
        )
        capital_invested += round(
            math.floor(position_size / row["Stock Price"])
            * row["Stock Price"],
            2,
        )

    append_additional_stats(
        portfolio_data_frame=portfolio_data_frame,
        portfolio_amount=portfolio_amount,
        capital_invested=capital_invested,
        stocks_unavailable_in_the_past=stocks_unavailable_in_the_past,
    )

    portfolio_data_frame.to_csv(
        f"Quantitative Momentum over - S{change_window}.csv", index=False
    )


quantitative_momentum_portfolio(
    portfolio_amount=10000000, portfolio_size=50, spy_only=True, sandbox=True
)
