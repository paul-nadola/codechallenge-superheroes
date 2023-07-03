#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes')
def heroes():
    heroes = Hero.query.all()
    hero_list = []
    for hero in heroes:
            hero_list.append({
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                "created_at": hero.created_at,
                "updated_at": hero.updated_at
            })

    response = make_response(
        jsonify(hero_list),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/heroes/<int:hero_id>')
def hero(hero_id):
     hero = Hero.query.filter_by(id=hero_id).first()
     if hero is None:
         response = make_response(
             jsonify({"error": "Hero not found"}),
             404
         )
         response.headers['Content-Type'] = 'application/json'
         return response

     response = make_response(
         jsonify({
             'id': hero.id,
             'name': hero.name,
             'super_name': hero.super_name,
             "created_at": hero.created_at,
             "updated_at": hero.updated_at
         }),
         200
     )
     response.headers['Content-Type'] = 'application/json'
     return response

@app.route('/powers')
def powers():
    powers = Hero.query.all()
    power_list = []
    for power in powers:
            power_list.append({
                'id': power.id,
                'name': power.name,
                'super_name': power.super_name,
                "created_at": power.created_at,
                "updated_at": power.updated_at
            })

    response = make_response(
        jsonify(power_list),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/powers/<int:power_id>')
def power(power_id):
     power = Hero.query.filter_by(id=power_id).first()
     if power is None:
         response = make_response(
             jsonify({"error": "Power not found"}),
             404
         )
         response.headers['Content-Type'] = 'application/json'
         return response

     response = make_response(
         jsonify({
             'id': power.id,
             'name': power.name,
             'super_name': power.super_name,
             "created_at": power.created_at,
             "updated_at": power.updated_at
         }),
         200
     )
     response.headers['Content-Type'] = 'application/json'
     return response


@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        response = make_response(
            jsonify({"error": "Power not found"}),
            404
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    if 'name' in request.json:
        power.name = request.json['name']
    if 'description' in request.json:
        power.description = request.json['description']

    db.session.commit()

    response = make_response(
        jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description,
            'created_at': power.created_at,
            'updated_at': power.updated_at
        }),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/heropower', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not strength or not power_id or not hero_id:
        response = make_response(
            jsonify({"errors": ["Validation errors"]}),
            400
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)
    if power is None or hero is None:
        response = make_response(
            jsonify({"errors": ["Invalid Power or Hero"]}),
            404
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    hero_power = HeroPower(strength=strength, power=power, hero=hero)
    db.session.add(hero_power)
    db.session.commit()

    response_data = {
        "id": hero_power.id,
        "strength": hero_power.strength,
        "hero_name": hero_power.hero.name,
        "power_name": hero_power.power.name,
        "created_at": hero_power.created_at,
        "updated_at": hero_power.updated_at
    }

    response = make_response(jsonify(response_data), 201)
    response.headers['Content-Type'] = 'application/json'
    return response






if __name__ == '__main__':
    app.run(port=5555)
