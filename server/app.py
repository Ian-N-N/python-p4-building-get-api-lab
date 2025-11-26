#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries: list all bakeries
@app.route('/bakeries', methods=['GET'])
def bakeries():
    all_bakeries = db.session.execute(db.select(Bakery)).scalars().all()
    return jsonify([b.to_dict(rules=b.serialize_rules) for b in all_bakeries])

# GET /bakeries/<int:id>: get one bakery with baked goods
@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404
    return jsonify(bakery.to_dict(rules=bakery.serialize_rules))

# GET /baked_goods/by_price: list baked goods sorted by price descending
@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    goods = db.session.execute(db.select(BakedGood).order_by(BakedGood.price.desc())).scalars().all()
    return jsonify([g.to_dict(rules=g.serialize_rules) for g in goods])

# GET /baked_goods/most_expensive: single most expensive baked good
@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    good = db.session.execute(
        db.select(BakedGood).order_by(BakedGood.price.desc())
    ).scalars().first()
    if not good:
        return jsonify({"error": "No baked goods found"}), 404
    return jsonify(good.to_dict(rules=good.serialize_rules))

if __name__ == '__main__':
    app.run(port=5555, debug=True)
