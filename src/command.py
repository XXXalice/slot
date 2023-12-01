def suggest():
    year = input("西暦を入力してください:").strip()
    date = input("日付を4桁で入力してください。日を00にすることで該当月を全取得します:").strip()
    if len(date) != 4:
        print("[ERROR] 入力された日付が無効です")
        exit()

    month_mode = False
    if date[-2:] == "00":
        print("月一覧集計モードで起動します。")
        month_mode = True

    data = {
        "year": year,
        "date": date,
        "month_mode": month_mode
    }

    return data

