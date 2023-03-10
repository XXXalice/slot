from bs4 import BeautifulSoup
import requests
import datetime


class Anaslo():

    def __init__(self, shop_name, date, area="東京都"):
        self.url_host = "https://ana-slo.com/"
        self.url_path_from_pref = "ホールデータ/{}/{}-データ一覧/".format(area, shop_name)
        date_str = self._get_date(date_string=date)
        self.url_path_from_shop = "ホールデータ/{}-{}-data/".format(date_str, shop_name).replace(" ", "")

    def _get_ua(self, mode="safari"):
        ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/62.0.3202.94 Safari/537.36"}
        return ua

    def _get_date(self, date_string):
        try:
            year = "2023" if len(date_string) != 7 else date_string[:4]
            month = date_string[:2] if len(date_string) != 7 else date_string[5:7]
            day = date_string[2:4] if len(date_string) != 7 else date_string[7:8]
            dt = datetime.datetime(year=int(year), month=int(month), day=int(day))
            return dt.strftime("%Y-%m-%d")
        except:
            print("[ERROR] 日付変換に失敗しました.\n"
                  "MMDDの4桁もしくは YYYYMMDDの8桁の数字形式で入力してください.")
            exit()

    def fetch(self):
        target = self.url_host + self.url_path_from_shop
