from flask_restful import Resource, reqparse
from models.position import PositionModel
from models.car import CarModel
from sqlalchemy.sql.functions import now


class CarPosition(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('latitude',
                      type=float,
                      required=True,
                      help="This field cannot be blank.")
  parser.add_argument('longitude',
                      type=float,
                      required=True,
                      help="This field cannot be blank.")

  def post(self, plate):
    data = CarPosition.parser.parse_args()
    car = CarModel.find_by_attribute(license_plate=plate)
    # print(car.id)

    if not car:
      return {'message': 'This car does not exist!'}, 404

    car_position = PositionModel(latitude=data['latitude'],
                                 longitude=data['longitude'],
                                 car_id=car.id)
    car_position.date = now()
    data_latlon = PositionModel.resolve_address(data['latitude'],
                                                data['longitude'])
    # (PositionModel.resolve_address(data['latitude'],
    #                                data['longitude']))['display_name']
    if data_latlon:
      car_position.address = data_latlon['display_name']
    else:
      car_position.address = 'No GPS data'

    try:
      car_position.save_to_db()
    except:
      return {"message": "An error occurred creating the fleet."}, 500

    return {'message': 'The save was successfully'}, 201

  def get(self, plate):
    car = CarModel.find_by_attribute(license_plate=plate)
    if not car:
      return {'message': 'This car does not exist'}

    return {
        'positions': [
            position.json()
            for position in PositionModel.query.filter_by(car_id=car.id)
        ]
    }
