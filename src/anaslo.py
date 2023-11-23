from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import datetime


class Anaslo():

    def __init__(self, shop_name, year, date, area="東京都"):
        self.shop_name = shop_name
        self.url_host = "https://ana-slo.com/"
        self.url_path_from_pref = "ホールデータ/{}/{}-データ一覧/".format(area, self.shop_name)
        self.date_str = self._get_date(year_string=year, date_string=date)
        self.url_path_from_shop = "ホールデータ/{}-{}-data/".format(self.date_str, self.shop_name).replace(" ", "")
        self._log("URLの初期化が完了しました。")

    def _get_header(self, mode="safari"):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/62.0.3202.94 Safari/537.36"}
        return header

    def _get_date(self, year_string, date_string):
        try:
            year = year_string if len(date_string) != 7 else date_string[:4]
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
        raw_data = self._req(target=target)
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
                    row = [self.date_str, section_name]
                    row.extend(datas)
                    rows.append(row)
            else:
                # 一台設置
                section_datas = section_datas_table.find_all("tr")[1:]
                for section_data in section_datas:
                    data_doms = section_data.find_all("td")
                    datas = [dom.text.replace(',', '') for dom in data_doms]
                    row = [self.date_str]
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