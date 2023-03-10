from src.anaslo import Anaslo

default_shop = "四谷タイガー"
default_year = "2023"

def main():
    print("アナスロゲッター ver1.0")
    print("現在のターゲット店舗：{}".format(default_shop))
    print("現在のターゲット西暦：{}".format(default_year))
    date = input("取得したい日付を入力してください（例 0311）：").strip()
    get_data(date=date)

def get_data(date):
    anaslo = Anaslo(shop_name=default_shop, date=date)
    anaslo.fetch()
if __name__ == '__main__':
    main()
