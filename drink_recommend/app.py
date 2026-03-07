from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# ===== 簡易インメモリDB =====
# （※画像のファイル名も仮で設定しておきました）
MENU = [
    {"id": "1", "name": "コーラ",         "type": "soft_drink", "price": 300, "description": "定番の炭酸飲料",       "tags": ["炭酸", "甘い"], "image": "1.jpg"},
    {"id": "2", "name": "紅茶",           "type": "soft_drink", "price": 300, "description": "香り豊かな紅茶",       "tags": ["リラックス", "食事に合う"], "image": "2.jpg"},
    {"id": "3", "name": "コーヒー",       "type": "soft_drink", "price": 350, "description": "食後の一杯に",         "tags": ["リラックス", "苦い"], "image": "3.jpg"},
    {"id": "4", "name": "オレンジジュース","type": "soft_drink", "price": 300, "description": "果汁100%",            "tags": ["甘い", "子ども向け"], "image": "4.jpg"},
    {"id": "5", "name": "レモネード",     "type": "soft_drink", "price": 350, "description": "さっぱりした味わい",   "tags": ["酸味", "さっぱり"], "image": "5.jpg"},
    {"id": "6", "name": "生ビール",       "type": "alcohol",    "price": 500, "description": "キンキンに冷えてます", "tags": ["お酒", "炭酸", "定番"], "image": "6.jpg"},
    {"id": "7", "name": "赤ワイン",       "type": "alcohol",    "price": 600, "description": "お肉料理に合います",   "tags": ["お酒", "芳醇"], "image": "7.jpg"},
    {"id": "8", "name": "白ワイン",       "type": "alcohol",    "price": 600, "description": "お魚料理に合います",   "tags": ["お酒", "さっぱり"], "image": "8.jpg"},
    {"id": "9", "name": "日本酒",         "type": "alcohol",    "price": 700, "description": "地元の銘酒",           "tags": ["お酒", "和食に合う"], "image": "9.jpg"},
    {"id": "10","name": "レモンサワー",   "type": "alcohol",    "price": 450, "description": "爽やかな果実感",       "tags": ["お酒", "果実酒", "さっぱり"], "image": "10.jpg"},
]

orders = []  # 注文履歴を保持


# ① Welcomeページ（QRコードで最初に開く画面）
@app.route("/")
def welcome():
    return render_template("welcome.html")

# ② メニュー画面（「注文を始める」を押した後の画面）
@app.route("/menu")
def index():
    return render_template("index.html")

# ③ メニューのデータを画面に渡すAPI
@app.route("/api/menu")
def get_menu():
    return jsonify(MENU)

# ④ レコメンド機能のAPI
@app.route("/api/recommend")
def recommend():
    alcohol_type = request.args.get("type")
    mood_tag = request.args.get("mood")
    results = [item for item in MENU if item["type"] == alcohol_type and mood_tag in item["tags"]]
    
    if not results:
        results = [item for item in MENU if item["type"] == alcohol_type][:3]
    return jsonify(results)

# ⑤ 注文を受け付けるAPI
@app.route("/api/order", methods=["POST"])
def create_order():
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

# ⑥ みんなの注文を表示するAPI
@app.route("/api/orders/recent")
def recent_orders():
    return jsonify(orders[-20:])

if __name__ == "__main__":
    app.run(debug=True, port=5000)