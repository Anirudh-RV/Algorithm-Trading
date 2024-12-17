import math
import os
import sys

sys.path.append(os.path.abspath(".."))
import pandas as pd

from constants import sandbox
from SPYData import stocks_data as spy


def equal_weight_spy_portfolio(portfolio_size: float, sandbox: bool = False):
    """
    Converts the list of stocks into a dictionary for quick look up

    Args:
        portfolio_size(float): The '$' amount of the portfolio
        sandbox(bool): If we should use the sandbox or not

    Returns:
        Outputs a CSV sheet with the portfolio suggestion
    """

    spy_stock_dataframe, status = spy.spy_stock_data(sandbox=sandbox)
    if not status:
        print("Could not get the SPY Stock data")
        return

    position_size = portfolio_size / len(spy_stock_dataframe)

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

    spy_stock_dataframe.loc[len(spy_stock_dataframe)] = [
        "Total Capital:",
        portfolio_size,
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
        round(portfolio_size - capital_invested, 2),
        "",
        "",
    ]

    spy_stock_dataframe.to_csv("S&P 500 Recommendations.csv", index=False)


equal_weight_spy_portfolio(portfolio_size=10000000, sandbox=sandbox)
