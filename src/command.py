import datetime

def suggest():
    year = input("西暦を入力してください:").strip()
    date = input("日付を4桁で入力してください:").strip()
    # try:
    #     target_date = datetime.date(year=year, month=date[:2], day=date[2:])
    # except ValueError:
    #     print("[ERROR] 入力された日付が無効です")
    #     exit()

    return year + date

