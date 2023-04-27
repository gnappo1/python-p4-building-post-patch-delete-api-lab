#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=["GET", "PATCH"])
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first_or_404()
    if request.method == "PATCH":
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        db.session.add(bakery)
        db.session.commit()
    
    bakery_serialized = bakery.to_dict()
    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    price = request.form.get("price")
    name = request.form.get("name")
    b_g = BakedGood(price=price, name=name)
    
    db.session.add(b_g)
    db.session.commit()
    
    response = make_response(b_g.to_dict(), 201)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/<int:id>', methods=["GET", "DELETE"])
def baked_good(id):
    bakedg = BakedGood.query.filter(BakedGood.id==id).first_or_404()
    if request.method == "DELETE":
        db.session.delete(bakedg)
        db.session.commit()
        response = make_response({"message": "record successfully deleted"}, 200)
        return response
    response = make_response(bakedg.to_dict(), 200)
    return response
    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
