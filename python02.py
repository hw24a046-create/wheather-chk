# pyright: ignore[reportMissingImports]
import pandas as pd
import plotly.express as px
import sys

print("=========================================")
print("[INFO] 天気データ グラフ生成スクリプト 開始")
print("=========================================")

# CSVファイルのパス
csv_path = "kobe.csv"

try:
    print(f"[INFO] {csv_path} を読み込んでいます...")
    
    # 気象庁のCSVはヘッダーより上に説明行などがあるため、不要な行をスキップして読み込む
    df = pd.read_csv(
        csv_path,
        encoding="shift_jis",
        skiprows=[0, 1, 2, 4, 5],  # 授業資料通りのスキップ設定
        header=0
    )
    
    # 型変換（文字列の日付をPythonが理解できる日付型に変換）
    df["年月日"] = pd.to_datetime(df["年月日"], format="%Y/%m/%d", errors="coerce")
    df["平均気温(℃)"] = pd.to_numeric(df["平均気温(℃)"], errors="coerce")
    
    print("[INFO] グラフ（Plotly）を生成中...")
    
    # 授業指定のPlotlyを使って、インタラクティブな折れ線グラフを作成
    fig = px.line(df, x="年月日", y="平均気温(℃)", title="平均気温の推移")
    
    # Jenkins上でポップアップ画面を出さずに、HTMLファイルとして保存する
    output_html = "temperature.html"
    fig.write_html(output_html)
    
    print("=========================================")
    print(f"===== [SUCCESS] グラフの生成に成功しました =====")
    print(f"[生成ファイル] {output_html}")
    print("=========================================")

except Exception as e:
    print("=========================================")
    print(f"===== [FAILED] グラフ生成に失敗しました =====")
    print(f"[エラー内容] {e}")
    print("=========================================")
    sys.exit(1)