import json
import requests
import time
import logging
from .utils.class_init import InitClass


class SplitDividendDownloader(InitClass):
    def __str__(self) -> str:
        return "SplitDividendDownloader()"

    def __repr__(self) -> str:
        return "SplitDividendDownloader()"

    def __init__(self):
        super().__init__()
        now = time.strftime("%Y%m%d-%H%M%S")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(rf"C:\Users\renar\PythonRobotAdv\logs\Downloader_splitdiv_{now}.log")],
        )
        logging.info(f"Initialized SplitDividendDownloader")
        dict_path = {
            "Splits": r"C:\Users\renar\PythonRobotAdv\data\raw\splits",
            "Dividends": r"C:\Users\renar\PythonRobotAdv\data\raw\dividends",
        }
        self.path = dict_path

    def get_split_data(self):
        try:
            for i in self.tickers:
                url = "https://www.alphavantage.co/query?function=SPLITS&symbol=" + i + "&apikey=" + self.api_key
                logging.info(f"Requesting data for ticker {i} with URL {url}")
                r = requests.get(url)
                with open(self.path["Splits"] + "\\" + i + ".json", "w") as outfile:
                    outfile.write(json.dumps(r.json(), indent=4))
                    logging.info(f"Data for {i} saved in {self.path["Splits"]}")
        except Exception as e:
            logging.error("Error getting data: %s", str(e))

    def get_dividend_data(self):
        try:
            for i in self.tickers:
                url = "https://www.alphavantage.co/query?function=DIVIDENDS&symbol=" + i + "&apikey=" + self.api_key
                logging.info(f"Requesting data for ticker {i} with URL {url}")
                r = requests.get(url)
                with open(self.path["Dividends"] + "\\" + i + ".json", "w") as outfile:
                    outfile.write(json.dumps(r.json(), indent=4))
                    logging.info(f"Data for {i} saved in {self.path["Dividends"]}")
        except Exception as e:
            logging.error("Error getting data: %s", str(e))
