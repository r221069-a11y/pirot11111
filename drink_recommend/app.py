from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# ===== 簡易インメモリDB =====
MENU = [
    {"id": "1", "name": "コーラ",         "type": "soft_drink", "price": 300, "description": "定番の炭酸飲料",       "tags": ["炭酸", "甘い"]},
    {"id": "2", "name": "紅茶",           "type": "soft_drink", "price": 300, "description": "香り豊かな紅茶",       "tags": ["リラックス", "食事に合う"]},
    {"id": "3", "name": "コーヒー",       "type": "soft_drink", "price": 350, "description": "食後の一杯に",         "tags": ["リラックス", "苦い"]},
    {"id": "4", "name": "オレンジジュース","type": "soft_drink", "price": 300, "description": "果汁100%",            "tags": ["甘い", "子ども向け"]},
    {"id": "5", "name": "レモネード",     "type": "soft_drink", "price": 350, "description": "さっぱりした味わい",   "tags": ["酸味", "さっぱり"]},
    {"id": "6", "name": "生ビール",       "type": "alcohol",    "price": 500, "description": "キンキンに冷えてます", "tags": ["お酒", "炭酸", "定番"]},
    {"id": "7", "name": "赤ワイン",       "type": "alcohol",    "price": 600, "description": "お肉料理に合います",   "tags": ["お酒", "芳醇"]},
    {"id": "8", "name": "白ワイン",       "type": "alcohol",    "price": 600, "description": "お魚料理に合います",   "tags": ["お酒", "さっぱり"]},
    {"id": "9", "name": "日本酒",         "type": "alcohol",    "price": 700, "description": "地元の銘酒",           "tags": ["お酒", "和食に合う"]},
    {"id": "10","name": "レモンサワー",   "type": "alcohol",    "price": 450, "description": "爽やかな果実感",       "tags": ["お酒", "果実酒", "さっぱり"]},
]

orders = []  # 注文履歴を保持


@app.route("/")
def welcome():
    # トップページ（QRコードで最初にアクセスする場所）は Welcome画面
    return render_template("welcome.html")

@app.route("/menu")
def index():
    # 「注文を始める」を押したら、いつものメニュー画面を表示
    return render_template("index.html")


@app.route("/api/menu")
def get_menu():
    return jsonify(MENU)


@app.route("/api/recommend")
def recommend():
    """タグで絞り込みレコメンド"""
    alcohol_type = request.args.get("type")   # "soft_drink" or "alcohol"
    mood_tag = request.args.get("mood")       # "さっぱり" etc.

    results = [
        item for item in MENU
        if item["type"] == alcohol_type and mood_tag in item["tags"]
    ]

    # 完全一致がなければ同じアルコール区分だけで返す
    if not results:
        results = [item for item in MENU if item["type"] == alcohol_type][:3]

    return jsonify(results)


@app.route("/api/order", methods=["POST"])
def create_order():
    """注文を受け付けて保存"""
    data = request.json
    order = {
        "id": str(len(orders) + 1),
        "items": data.get("items", []),
        "total_amount": data.get("total_amount", 0),
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    orders.append(order)
    return jsonify({"status": "success", "order_id": order["id"]})


@app.route("/api/orders/recent")
def recent_orders():
    """最近の注文一覧（直近20件）"""
    return jsonify(orders[-20:])


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    # コメントアウト