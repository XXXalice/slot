from src.anaslo import Anaslo
from src.command import suggest

shop = "アット小平"

def main():
    print("アナスロゲッター ver1.3.1")
    print("現在のターゲット店舗：{}".format(shop))
    data = suggest()
    get_data(data)


def get_data(data):
    anaslo = Anaslo(shop_name=shop, year=data.get("year"), date=data.get("date"), month_mode=data.get("month_mode"))
    anaslo.fetch_all()


if __name__ == '__main__':
    main()
