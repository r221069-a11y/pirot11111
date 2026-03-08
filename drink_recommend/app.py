from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# ===== 簡易インメモリDB =====
# 3軸分類：type（アルコール/ノンアル）、soda（炭酸/炭酸なし）、flavor（甘め/辛口）
MENU = [
    # アルコール カクテル
    {"id": "1", "name": "ミント・モーニ", "type": "alcohol", "soda": "炭酸", "flavor": "甘め", "price": 650, "description": "爽やかなミントと柑橘のカクテル", "tags": ["アルコール", "炭酸", "甘め"], "image": "ミント・モーニ.jpg"},
    {"id": "2", "name": "スパークリング・ジン・トニック", "type": "alcohol", "soda": "炭酸", "flavor": "辛口", "price": 700, "description": "定番の爽快感あるカクテル", "tags": ["アルコール", "炭酸", "辛口"], "image": "スパークリング・ジン・トニック.jpg"},
    {"id": "3", "name": "ジン・カリンクリンク", "type": "alcohol", "soda": "炭酸なし", "flavor": "甘め", "price": 680, "description": "芳しいジンと甘い香りのカクテル", "tags": ["アルコール", "炭酸なし", "甘め"], "image": "ジン・カリンクリンク.jpg"},
    {"id": "4", "name": "ハンビー・ワトコイル", "type": "alcohol", "soda": "炭酸なし", "flavor": "辛口", "price": 720, "description": "深みのある大人っぽいカクテル", "tags": ["アルコール", "炭酸なし", "辛口"], "image": "ハンピー・ワトコイル.jpg"},
    # ノンアルコール
    {"id": "5", "name": "ピーチ・クラウド・ソーダ", "type": "non_alcohol", "soda": "炭酸", "flavor": "甘め", "price": 500, "description": "桃の香りが優しい炭酸飲料", "tags": ["ノンアル", "炭酸", "甘め"], "image": "ピーチ・クラウド・ソーダ.jpg"},
    {"id": "6", "name": "ダーク・ジンジャー・エスプレッソ", "type": "non_alcohol", "soda": "炭酸", "flavor": "辛口", "price": 550, "description": "ジンジャーの辛さが引き立つ", "tags": ["ノンアル", "炭酸", "辛口"], "image": "ダーク・ジンジャー・エスプレッソ.jpg"},
    {"id": "7", "name": "ハニー・マスカット・ティー", "type": "non_alcohol", "soda": "炭酸なし", "flavor": "甘め", "price": 480, "description": "蜂蜜とマスカットの優しいティー", "tags": ["ノンアル", "炭酸なし", "甘め"], "image": "ハニー・マスカット・ティー.jpg"},
    {"id": "8", "name": "スモークド・トマト・メアリー", "type": "non_alcohol", "soda": "炭酸なし", "flavor": "辛口", "price": 520, "description": "スパイシーで個性的な味わい", "tags": ["ノンアル", "炭酸なし", "辛口"], "image": "スモークド・トマト・メアリー.jpg"},
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

# ④ レコメンド機能のAPI（3軸フィルタリング対応）
@app.route("/api/recommend")
def recommend():
    alcohol_type = request.args.get("type")  # "alcohol" or "non_alcohol"
    soda = request.args.get("soda")  # "炭酸" or "炭酸なし"
    flavor = request.args.get("flavor")  # "甘め" or "辛口"
    
    results = MENU
    
    if alcohol_type:
        results = [item for item in results if item["type"] == alcohol_type]
    if soda:
        results = [item for item in results if item["soda"] == soda]
    if flavor:
        results = [item for item in results if item["flavor"] == flavor]
    
    # 3つの条件に合致するもの1つだけ返す
    if results:
        results = [results[0]]
    
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
    # host="0.0.0.0" にすることで外部からアクセスできるようになります
    app.run(debug=True, port=8080)