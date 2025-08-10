import pandas as pd
import json
import re

def sheet_to_json_file(url, filename="sheet_data.json"):
    # URLからsheet_idとgidを抽出
    sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    gid_match = re.search(r'gid=(\d+)', url)

    if not sheet_id_match:
        raise ValueError("シートIDがURLから取得できません")
    sheet_id = sheet_id_match.group(1)
    gid = gid_match.group(1) if gid_match else "0"

    # CSVのURL作成
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    # CSV読み込み（日本語対応）
    df = pd.read_csv(csv_url, encoding="utf-8-sig")
    df = df.iloc[:, 0:14]  # A列～N列

    # NaNをnullにして辞書化
    json_data = df.where(pd.notnull(df), None).to_dict(orient="records")

    # JSONファイルに保存
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"JSONファイルとして保存しました: {filename}")

url = "https://docs.google.com/spreadsheets/d/18jstlxLyUPNrTM6uuH0Vmtq-XRgYKl8b1WRWwCFMRts/edit?pli=1&gid=397997272#gid=397997272"
sheet_to_json_file(url, "sheet_data.json")
