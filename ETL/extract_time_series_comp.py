import json
import logging
import time
import requests
from .utils.class_init import InitClass


class TimeSeriesDownloader_to_Json(InitClass):
    """
    A class for downloading time series data and saving it as JSON files.
    Args:
        outputsize (str, optional): The size of the output data. Defaults to "compact".
    Attributes:
        outputsize (str): The size of the output data.
    Methods:
        get_time_series_data: Downloads time series data and saves it as JSON files.
    """

    def __str__(self) -> str:
        return f"TimeSeriesDownloader({self.outputsize!r})"

    def __repr__(self) -> str:
        return f"TimeSeriesDownloader({self.outputsize!r})"

    def __init__(self, outputsize="compact"):
        super().__init__()
        self._outputsize = outputsize
        now = time.strftime("%Y%m%d-%H%M%S")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(rf"C:\Users\renar\PythonRobotAdv\logs\Downloader_{now}.log")],
        )
        logging.info(f"Initialized TimeSeriesDownloader_to_Json with outputsize={self._outputsize}")
        dict_path = {
            "Quotes": r"C:\Users\renar\PythonRobotAdv\data\raw\quotes",
        }
        self.path = dict_path

    @property
    def outputsize(self) -> str:
        return self._outputsize

    @outputsize.setter
    def outputsize(self, value: str) -> None:
        if value not in ("compact", "full"):
            logging.error("Invalid outputsize value: %s", value)
            raise ValueError("Invalid outputsize value")
        logging.info(f"Setting outputsize to {value}")
        self._outputsize = value

    def get_time_series_data(self):
        try:
            for i in self.tickers:
                url = (
                    "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
                    + i
                    + "&outputsize="
                    + self.outputsize
                    + "&apikey="
                    + self.api_key
                )
                logging.info(f"Requesting data for ticker {i} with URL: {url}")
                r = requests.get(url)
                with open(self.path["Quotes"] + "\\" + i + ".json", "w") as outfile:
                    outfile.write(json.dumps(r.json(), indent=4))
                logging.info(f"Saved data for ticker {i} to {self.path["Quotes"]}")
        except Exception as e:
            logging.error("Error getting data: %s", str(e))
