import sqlite3
import json
import os
import sys
import pandas as pd

from ETL.extract_time_series_comp import TimeSeriesDownloader_to_Json
from ETL.extract_split_divid import SplitDividendDownloader
from ETL.transform_time_series import TimeSeriesTransformer
from ETL.utils.class_init import InitClass


# from questdb.ingress import Sender


# import yaml

api_key = open(r"C:\Users\renar\PythonRobotAdv\keys\AlphaVantage.txt", "r").read()

if __name__ == "__main__":
    # # Download Time Series Data
    downloader_ts = TimeSeriesDownloader_to_Json()
    downloader_ts.api_key = api_key
    downloader_ts.tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "TSLA"]
    downloader_ts.outputsize = "full"
    downloader_ts.get_time_series_data()

    # Download Split and Dividend Data
    downloader_sd = SplitDividendDownloader()
    downloader_sd.api_key = api_key
    downloader_sd.tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "TSLA"]
    downloader_sd.get_split_data()
    downloader_sd.get_dividend_data()

    # Transform Time Series Data
    try:
        for ticker in ["NVDA", "AAPL", "MSFT", "GOOGL", "TSLA"]:
            transformer = TimeSeriesTransformer(ticker)
            path = rf"C:\Users\renar\PythonRobotAdv\data\raw\quotes\{ticker}" + ".json"
            df = transformer.transformer(path)
            splits = transformer.get_split(rf"C:\Users\renar\PythonRobotAdv\data\raw\splits\{ticker}" + ".json")
            dividends = transformer.get_dividends(
                rf"C:\Users\renar\PythonRobotAdv\data\raw\dividends\{ticker}" + ".json")
            df = transformer.adjust_data(df, splits, dividends)
    except Exception as e:
        print(f"Error: {e}")

    # # Push to database (SQLite) !
    # con = sqlite3.connect(r".\test.db")
    # cur = con.cursor()
    # # Create table for NVDA if not exists
    # create_company_TStable(con, cur, r".\data\raw\quotes")
    # # Insert data to NVDA table
    # insert_company_time_series(con, cur, r".\data\raw\quotes")

    # # Query data from NVDA table
    # cur.execute("SELECT * FROM NVDA;")
    # print(cur.fetchall())
