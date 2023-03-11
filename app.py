import calendar

from src.anaslo import Anaslo

default_shop = "アット小平"
default_year = "2023"


def main():
    print("アナスロゲッター ver1.0")
    print("現在のターゲット店舗：{}".format(default_shop))
    print("現在のターゲット西暦：{}".format(default_year))
    date = input("取得したい日付（4桁）もしくは月（1桁）を入力してください（例 0311 or 2）：").strip()
    command(date=date)


def get_data(date):
    anaslo = Anaslo(shop_name=default_shop, date=date)
    rows = anaslo.fetch()
    anaslo.to_csv(rows=rows)


def command(date):
    if len(date) == 1:
        month = date
        print("月単位モードで取得します。取得月:{}".format(date))
        date_range = calendar.monthrange(int(default_year), int(month))[1]
        date_list = ["{:02}{:02}".format(int(month), day) for day in range(1, date_range + 1)]
        for d in date_list:
            get_data(date=d)
    else:
        get_data(date=date)


if __name__ == '__main__':
    main()
