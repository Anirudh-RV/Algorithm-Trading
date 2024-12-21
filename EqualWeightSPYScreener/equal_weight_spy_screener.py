import math
import os
import sys

sys.path.append(os.path.abspath(".."))
import pandas as pd

from constants import sandbox
from SPYData import stocks_data as spy


def append_additional_stats(
    spy_stock_dataframe: pd.DataFrame,
    portfolio_amount: float,
    capital_invested: float,
) -> None:
    """
    Does in place update of the spy_stock_dataframe to add additional statistics of the portfolio

    Args:
        spy_stock_dataframe (pd.DataFrame): The DataFrame to be modified
        portfolio_amount (float): The portfolio amount
        capital_invested (float): The total capital invested

    Returns:
        None
        In place change to DataFrame
    """

    spy_stock_dataframe.loc[len(spy_stock_dataframe)] = [
        "Total Capital:",
        portfolio_amount,
        "",
        "",
    ]
    spy_stock_dataframe.loc[len(spy_stock_dataframe)] = [
        "Capital invested:",
        round(capital_invested, 2),
        "",
        "",
    ]
    spy_stock_dataframe.loc[len(spy_stock_dataframe)] = [
        "Capital remaining:",
        round(portfolio_amount - capital_invested, 2),
        "",
        "",
    ]


def equal_weight_spy_portfolio(portfolio_amount: float, sandbox: bool = False):
    """
    Equal weight SPY portfolio

    Args:
        portfolio_amount(float): The '$' amount of the portfolio
        sandbox(bool): If we should use the sandbox or not

    Returns:
        Outputs a CSV sheet with the portfolio suggestion
    """

    spy_stock_dataframe, status = spy.spy_stock_data(sandbox=sandbox)
    if not status:
        print("Could not get the SPY Stock data")
        return

    position_size = portfolio_amount / len(spy_stock_dataframe)

    capital_invested = 0
    for index, row in spy_stock_dataframe.iterrows():
        spy_stock_dataframe.loc[index, "Number of Shares to Purchase"] = (
            math.floor(position_size / row["Stock Price"])
        )
        capital_invested += round(
            math.floor(position_size / row["Stock Price"])
            * row["Stock Price"],
            2,
        )

    append_additional_stats(
        spy_stock_dataframe=spy_stock_dataframe,
        portfolio_amount=portfolio_amount,
        capital_invested=capital_invested,
    )

    spy_stock_dataframe.to_csv("S&P 500 Recommendations.csv", index=False)
