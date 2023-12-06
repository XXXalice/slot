from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import datetime
import calendar
import re


class Anaslo():

    def __init__(self, shop_name, year, date, month_mode, area="東京都"):
        self.shop_name = shop_name
        self.url_host = "https://ana-slo.com/"
        self.target_date_list = []
        self.target_url_list = []
        self.year = year
        self.month = date[:2]
        # 日単位での取得or月単位
        self.month_mode = month_mode
        if month_mode:
            self.target_date_list = self._get_days_list_from_month()
        else:
            self.date = date[2:]
            self.target_date_list.append(self._get_date())

        for target_date in self.target_date_list:
            url = self.url_host + f"ホールデータ/{target_date}-{self.shop_name}-data/".replace(" ", "")
            self.target_url_list.append(url)
        self._log("URLの初期化が完了しました。")

    def _get_header(self, mode="safari"):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/62.0.3202.94 Safari/537.36"}
        return header

    def _get_days_list_from_month(self):
        try:
            day_num = calendar.monthrange(self.year, self.month)
            target_day_list = []
            for day in range(1, day_num+1):
                target_day_list.append(f"{self.year}-{self.month}-{day}")
        except:
            # TODO 2,5など正しい月でも1桁だと落ちる
            print("[ERROR] 日付変換に失敗しました。\n"
                  "正しい日付を入力してください。")
            exit()
        return target_day_list

    def _get_date(self):
        return f"{self.year}-{self.month}-{self.date}"

    def fetch_all(self):
        for target_url in self.target_url_list:
            self.fetch(target_url)

    def fetch(self, target_url):
        date = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", target_url).group()
        raw_data = self._req(target=target_url)
        data = BeautifulSoup(raw_data.content, "lxml")
        tables = data.find("table", class_="unit_get_medals_table") \
            .find_all("td", class_="table_cells")

        # セクション名及び機種名の取得
        sections = {}
        for sect_dom in tqdm(tables):
            sect_id = sect_dom.find("a")["href"].replace("#section", "")
            if sect_dom.find("a").text == "1台設置機種":
                sect_id = "variety"
            sections[sect_id] = sect_dom.find("a").text
        self._log("機種一覧の取得に成功しました。")

        rows = []
        first_row = ["日付", "機種名", "台番号", "G数", "差枚", "BB", "RB", "合成確率", "BB確率", "RB確率"]
        rows.append(first_row)
        for section_id, section_name in tqdm(sections.items()):
            section_datas_table = data.find("div", id="tab01_{}".format(section_id))
            if section_id != "variety":
                # 1台設置以外
                section_datas = section_datas_table.find_all("tr")[1:]
                for section_data in section_datas:
                    data_doms = section_data.find_all("td", class_="table_cells")
                    datas = [dom.text.replace(',', '') for dom in data_doms]
                    row = [date, section_name]
                    row.extend(datas)
                    rows.append(row)
            else:
                # 一台設置
                section_datas = section_datas_table.find_all("tr")[1:]
                for section_data in section_datas:
                    data_doms = section_data.find_all("td")
                    datas = [dom.text.replace(',', '') for dom in data_doms]
                    row = [date]
                    row.extend(datas)
                    rows.append(row)
        self._log("全機種データの処理に成功しました。")
        self._sanitize(rows=rows)
        return rows

    # 平均がいらないため除外していく
    def _sanitize(self, rows):
        for row in rows:
            if row[2] == "平均":
                # 平均値を抜きます
                rows.remove(row)

        return rows



    def _req(self, target):
        raw_data = requests.get(url=target, headers=self._get_header())
        self._log("ページのリクエストに成功しました。")
        return raw_data

    def _log(self, msg):
        print("[正常] {}".format(msg))

    def to_csv(self, rows):
        path = "./files/{}-{}.csv".format(self.date_str, self.shop_name)
        with open(path, mode='w', encoding="utf_8_sig") as f:
            for row in rows:
                f.write(','.join(row) + "\n")
        self._log("ファイルの作成が完了しました。ファイル名:{}".format(path.split("/")[-1]))