from db import db, BaseModel
from models.model_mixin import MixinModel
from urllib.request import urlopen
import json


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'positions'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float(precision=5))
  longitude = db.Column(db.Float(precision=5))
  address = db.column(db.String(300))
  # one to many with bidirectional relationship
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
  car = db.relationship('CarModel', back_populates='positions')

  def __init__(self, car_id, latitude, longitude):
    self.car_id = car_id
    self.latitude = latitude
    self.longitude = longitude

  def json(self):
    return {
        'latitude': self.latitude,
        'longitude': self.longitude,
        'date': self.date.isoformat()
        # 'address': self.address
    }

  def resolve_address(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}'
    try:
      response = urlopen(url)
      data_json = json.loads(response.read())
    except Exception:
      return False
    # print('data_json', data_json['display_name'])
    return data_json