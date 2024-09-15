import json
from datetime import datetime

import requests

from utils.class_init import InitClass

api_key = open(r"C:\Users\rrenard\OneDrive - Arkus\Desktop\Python\AlphaVantage_API_Key.txt", "r").read()

template_path = {"Balance Sheet": r"C:\Users\rrenard\Arkus_python\prototype\template\tp_all.yml"}

dict_path = {
    "Balance Sheet": r"C:\Users\rrenard\Arkus_python\prototype\data\raw\balance_sheet",
    "Cash Flow": r"C:\Users\rrenard\Arkus_python\prototype\data\raw\cash_flow",
    "Income Statement": r"C:\Users\rrenard\Arkus_python\prototype\data\raw\income_statement",
    "Earnings": r"C:\Users\rrenard\Arkus_python\prototype\data\raw\earnings",
    "Overview": r"C:\Users\rrenard\Arkus_python\prototype\data\raw\overview",
    "Quotes": r"C:\Users\rrenard\Arkus_python\prototype\data\raw\quotes",
}


class FundamentalsDataDownloader_to_Json(InitClass):

    def __str__(self) -> str:
        return f"FundamentalsDataDownloader({self.statements!r})"

    def __repr__(self) -> str:
        return f"FundamentalsDataDownloader({self.statements!r})"

    def __init__(self, statements="ALL"):
        super().__init__()
        self.statements = statements

    def get_financial_statement(self):
        if self.statements == "ALL":
            self.statements = ["INCOME_STATEMENT", "BALANCE_SHEET", "CASH_FLOW", "EARNINGS", "OVERVIEW"]
            try:
                for j in self.tickers:
                    for i in self.statements:
                        url = "https://www.alphavantage.co/query?function=" + i + "&symbol=" + j + "&apikey=" + api_key
                        try:
                            r = requests.get(url)
                            r.raise_for_status()
                        except requests.exceptions.HTTPError as e:
                            print(e)
                        match i:
                            case "INCOME_STATEMENT":
                                with open(dict_path["Income Statement"] + "\\" + j + "_" + i + ".json", "w") as outfile:
                                    outfile.write(json.dumps(r.json(), indent=4))
                            case "BALANCE_SHEET":
                                with open(dict_path["Balance Sheet"] + "\\" + j + "_" + i + ".json", "w") as outfile:
                                    outfile.write(json.dumps(r.json(), indent=4))
                            case "CASH_FLOW":
                                with open(dict_path["Cash Flow"] + "\\" + j + "_" + i + ".json", "w") as outfile:
                                    outfile.write(json.dumps(r.json(), indent=4))
                            case "EARNINGS":
                                with open(dict_path["Earnings"] + "\\" + j + "_" + i + ".json", "w") as outfile:
                                    outfile.write(json.dumps(r.json(), indent=4))
                            case "OVERVIEW":
                                with open(dict_path["Overview"] + "\\" + j + "_" + i + ".json", "w") as outfile:
                                    outfile.write(json.dumps(r.json(), indent=4))
                            case _:
                                print(f"Invalid statement or not added ({self.statements})")
            except Exception as e:
                print("Error getting data:", str(e))
        else:
            try:
                for i in self.tickers:
                    url = (
                        "https://www.alphavantage.co/query?function="
                        + str(self.statements)
                        + "&symbol="
                        + i
                        + "&apikey="
                        + self.api_key
                    )
                    r = requests.get(url)
                    match self.statements:
                        case "INCOME_STATEMENT":
                            with open(dict_path["Income Statement"] + "\\" + i + ".json", "w") as outfile:
                                outfile.write(json.dumps(r.json(), indent=4))
                        case "BALANCE_SHEET":
                            with open(dict_path["Balance Sheet"] + "\\" + i + ".json", "w") as outfile:
                                outfile.write(json.dumps(r.json(), indent=4))
                        case "CASH_FLOW":
                            with open(dict_path["Cash Flow"] + "\\" + i + ".json", "w") as outfile:
                                outfile.write(json.dumps(r.json(), indent=4))
                        case "EARNINGS":
                            with open(dict_path["Earnings"] + "\\" + i + ".json", "w") as outfile:
                                outfile.write(json.dumps(r.json(), indent=4))
                        case "OVERVIEW":
                            with open(dict_path["Overview"] + "\\" + i + ".json", "w") as outfile:
                                outfile.write(json.dumps(r.json(), indent=4))
                        case _:
                            print(f"Invalid statement or not added ({self.statements})")
            except Exception as e:
                print("Error getting data:", str(e))

    def get_list_of_reports_dates(self, file_path: str) -> list[datetime]:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print("Error getting data:", e)
        try:
            dates_list = []
            for i in range(len(data["quarterlyReports"])):
                dates_list.append(data["quarterlyReports"][i]["fiscalDateEnding"])
        except Exception as e:
            print("Error occured:", e)
        try:
            datetime_list = []
            for j in dates_list:
                coverted_string = [datetime.strptime(j, "%Y-%m-%d")]
                datetime_list.append(coverted_string)
        except Exception as e:
            print("Error occured:", e)
        return datetime_list
