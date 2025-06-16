#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# ----------- Resource Definitions -----------

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201

class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

# ----------- Add Routes to API -----------

api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

# ----------- Run App -----------

if __name__ == '__main__':
    app.run(port=5555, debug=True)
