import json
import os
import sqlite3


import os


class TableCreator:
    def __init__(self, con, cur):
        self.con = con
        self.cur = cur

    def create_company_TStable(self, dir):
        for file in os.listdir(dir):
            try:
                self.cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS {file.split(
                        ".")[0]} (Date TEXT PRIMARY KEY, Open REAL, High REAL, Low REAL, Close REAL, Volume INTEGER);"""
                )
                self.con.commit()
            except Exception as e:
                print(e)


class DataLoader:
    def __init__(self, con, cur):
        self.con = con
        self.cur = cur

    def insert_company_time_series(self, df, dir):
        for file in os.listdir(dir):
            try:
                self.cur.executemany(f"INSERT OR REPLACE INTO {file.split(
                    '.')[0]} VALUES (?, ?, ?, ?, ?, ?);", df.itertuples())
                self.con.commit()
            except Exception as e:
                print(e)
