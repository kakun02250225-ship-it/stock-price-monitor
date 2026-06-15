import yfinance as yf
from datetime import datetime

SOXL_BUY_PRICE = 41726

soxl = yf.Ticker("SOXL")
soxl_data = soxl.history(period="5d")
soxl_current = soxl_data['Close'].iloc[-1]
soxl_prev = soxl_data['Close'].iloc[-2]
soxl_change = ((soxl_current - soxl_prev) / soxl_prev) * 100
soxl_total_change = ((soxl_current * 160.36 - SOXL_BUY_PRICE) / SOXL_BUY_PRICE) * 100

print(f"SOXL 現在値: ${soxl_current:.2f}")
print(f"本日変化: {soxl_change:.2f}%")
print(f"トータルリターン: {soxl_total_change:.1f}%")

if soxl_total_change >= 25:
    print("🔴 売却推奨")
elif soxl_change < -5:
    print("⚠️ 警戒")
else:
    print("📈 保有継続")
