from src.anaslo import Anaslo
from src.command import suggest

shop = "アット小平"

def main():
    print("アナスロゲッター ver2.0")
    print("現在のターゲット店舗：{}".format(shop))
    target_date = suggest()
    get_data(target_date)


def get_data(target_date):
    anaslo = Anaslo(shop_name=shop, year=target_date[:4], date=target_date[5:])
    rows = anaslo.fetch()
    anaslo.to_csv(rows=rows)


if __name__ == '__main__':
    main()
