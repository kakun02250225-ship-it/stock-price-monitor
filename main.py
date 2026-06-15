import functions_framework
import yfinance as yf
from datetime import datetime
import json

# 設定
RECIPIENT_EMAIL = "yuum445@gmail.com"
SOXL_BUY_PRICE = 41726  # 購入時の価格（円）

@functions_framework.http
def stock_monitor(request):
    """毎日朝9時に実行される株価監視関数"""
    
    try:
        # 1. 株価取得
        soxl = yf.Ticker("SOXL")
        soxl_data = soxl.history(period="5d")
        soxl_current = soxl_data['Close'].iloc[-1]
        soxl_prev = soxl_data['Close'].iloc[-2]
        soxl_change = ((soxl_current - soxl_prev) / soxl_prev) * 100
        soxl_total_change = ((soxl_current * 160.36 - SOXL_BUY_PRICE) / SOXL_BUY_PRICE) * 100
        
        # 2. 判定ロジック
        actions = []
        
        # SOXL 売却判定（+25% または 業界下げ）
        if soxl_total_change >= 25:
            actions.append({
                "銘柄": "SOXL（半導体チャレンジ）",
                "アクション": "🔴 売却推奨",
                "理由": f"目標リターン達成（+{soxl_total_change:.1f}%）",
                "現在値": f"${soxl_current:.2f}",
                "日次変化": f"{soxl_change:.2f}%"
            })
        elif soxl_change < -5:
            actions.append({
                "銘柄": "SOXL（半導体チャレンジ）",
                "アクション": "⚠️ 警戒",
                "理由": f"1日で{abs(soxl_change):.2f}%下落",
                "現在値": f"${soxl_current:.2f}",
                "日次変化": f"{soxl_change:.2f}%"
            })
        else:
            actions.append({
                "銘柄": "SOXL（半導体チャレンジ）",
                "アクション": "📈 保有継続",
                "理由": f"調整局面。リターン +{soxl_total_change:.1f}%",
                "現在値": f"${soxl_current:.2f}",
                "日次変化": f"{soxl_change:.2f}%"
            })
        
        return {"status": "success", "message": "監視完了", "actions": actions}, 200
        
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
