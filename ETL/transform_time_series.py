import logging
import time
import json
import pandas as pd


class TimeSeriesTransformer:
    def __init__(self, Company_name: str):
        now = time.strftime("%Y%m%d-%H%M%S")
        self.logger = logging.getLogger(Company_name)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(rf"C:\Users\renar\PythonRobotAdv\logs\Transform_{Company_name}_{now}.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.Company_name = Company_name

    def transformer(self, path: str) -> pd.DataFrame:
        self.logger.info(f"Loading data from {path}")
        data = json.load(open(path))
        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df.rename(
            columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume",
            },
            inplace=True,
        )
        df.index = pd.to_datetime(df.index)
        df.sort_index(ascending=True, inplace=True)
        df = df.astype(float)
        return df

    def get_split(self, path: str) -> pd.DataFrame:
        self.logger.info(f"Loading splits from {path}")
        data = json.load(open(path))
        df = pd.DataFrame(data["data"])
        df.set_index("effective_date", inplace=True)
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df

    def get_dividends(self, path: str) -> pd.DataFrame:
        self.logger.info(f"Loading dividends from {path}")
        data = json.load(open(path))
        df = pd.DataFrame(data["data"])
        if df.empty:
            self.logger.info("No dividends found")
            return df
        df = df[["ex_dividend_date", "amount"]]
        df.set_index("ex_dividend_date", inplace=True)
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df

    def adjust_data(self, data, splits, dividends) -> pd.DataFrame:
        self.logger.info("Starting adjust_data function")
        adjusted_parts = []
        # Adjust data for dividends
        data.index = pd.to_datetime(data.index)
        self.logger.info("Processing dividends")
        for date, dividend in dividends.iterrows():
            self.logger.info(f"Processing dividend for date: {date}, amount: {dividend['amount']}")
            date = pd.to_datetime(date)  # type: ignore
            factor_condition = data.index == date
            condition = data.index <= date
            dividend_amount = pd.to_numeric(dividend["amount"])
            dividend_factor = data.loc[factor_condition, "Close"] / \
                (data.loc[factor_condition, "Close"] - dividend_amount)
            self.logger.info(f"Calculated dividend_factor: {dividend_factor.values[0]}")
            data.loc[condition, "Close"] = data.loc[condition, "Close"] / dividend_factor.values[0]
            self.logger.info(f"Adjusted Close prices for Dividend up to date: {date}")
        self.logger.info("Finished processing dividends")

        # Assuming `data` and `splits` are already defined DataFrames
        for i in range(len(splits)):
            if i == 0:
                condition = data.index < splits.index[-1]
                part = data["Close"].where(condition).dropna()
                adjustment_factor = pd.to_numeric(splits["split_factor"].prod())
                adjusted_part = part / adjustment_factor
            else:
                condition = (data.index > splits.index[-i]) & (data.index < splits.index[-i - 1])
                part = data["Close"].where(condition).dropna()
                adjustment_factor = pd.to_numeric(splits["split_factor"].iloc[:-i].prod())
                adjusted_part = part / adjustment_factor
            adjusted_parts.append(adjusted_part)
            self.logger.info(f"Processed part {i}, adjustment_factor: {adjustment_factor}")

        # Handle the last part separately
        condition_last = data.index > splits.index[-len(splits)]
        last_part = data["Close"].where(condition_last).dropna()
        adjusted_parts.append(last_part)
        # Concatenate all adjusted parts
        adjusted_data = pd.concat(adjusted_parts)
        save_path = rf"C:\Users\renar\PythonRobotAdv\data\transformed\{self.Company_name}.csv"
        adjusted_data.to_csv(save_path)
        self.logger.info("Finished processing splits")
        self.logger.info(f"Adjusted data saved to {save_path}")
        self.logger.info("Finished adjust_data function")
        return adjusted_data
