import yfinance as yf

# ===== 保有情報 =====
# SOXL(米国株・株数×為替で計算)
SOXL_BUY_PRICE = 41726
SOXL_SHARES = 160.36

# 日本株(PayPay証券・投資元本で計算)
NINTENDO_COST = 10000      # 任天堂 投資元本(円)
NINTENDO_SHARES = 1.0035545904
HITACHI_COST = 4500        # 日立 投資元本(円)
HITACHI_SHARES = 0.9075014067


def check_us(name, ticker, buy_price, shares):
    data = yf.Ticker(ticker).history(period="5d")
    if len(data) < 2:
        return f"【{name}】データ取得失敗\n"
    current = data['Close'].iloc[-1]
    prev = data['Close'].iloc[-2]
    change = ((current - prev) / prev) * 100
    total = ((current * shares - buy_price) / buy_price) * 100
    msg = f"【{name}】\n"
    msg += f"  現在値: ${current:.2f}\n"
    msg += f"  本日変化: {change:+.2f}%\n"
    msg += f"  トータルリターン: {total:+.1f}%\n"
    if total >= 25:
        msg += "  🔴 売却推奨\n"
    elif change < -5:
        msg += "  ⚠️ 警戒\n"
    else:
        msg += "  📈 保有継続\n"
    return msg


def check_jp(name, ticker, cost, shares):
    data = yf.Ticker(ticker).history(period="5d")
    if len(data) < 2:
        return f"【{name}】データ取得失敗\n"
    current = data['Close'].iloc[-1]
    prev = data['Close'].iloc[-2]
    change = ((current - prev) / prev) * 100
    value = current * shares          # 現在の評価額(円)
    profit = value - cost             # 損益(円)
    total = (profit / cost) * 100     # リターン(%)
    msg = f"【{name}】\n"
    msg += f"  株価: {current:,.1f}円\n"
    msg += f"  評価額: {value:,.0f}円\n"
    msg += f"  損益: {profit:+,.0f}円 ({total:+.2f}%)\n"
    msg += f"  本日変化: {change:+.2f}%\n"
    if change < -5:
        msg += "  ⚠️ 警戒\n"
    else:
        msg += "  📈 保有継続\n"
    return msg


report = ""
report += check_us("SOXL", "SOXL", SOXL_BUY_PRICE, SOXL_SHARES)
report += "\n"
report += check_jp("任天堂", "7974.T", NINTENDO_COST, NINTENDO_SHARES)
report += "\n"
report += check_jp("日立製作所", "6501.T", HITACHI_COST, HITACHI_SHARES)

print(report)
