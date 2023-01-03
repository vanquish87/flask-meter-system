from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta
import random


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)


class Meter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, unique=True)

class MeterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meter.id'))
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'timestamp': self.timestamp,
            'value': self.value
        }

# create the database tables
with app.app_context():
    db.create_all()

# add fake meter data to the database
with app.app_context():
    meter1 = Meter.query.filter_by(label='Meter 1').first()
    if not meter1:
        meter1 = Meter(label='Meter 1')
        db.session.add(meter1)
        db.session.commit()

    meter2 = Meter.query.filter_by(label='Meter 2').first()
    if not meter2:
        meter2 = Meter(label='Meter 2')
        db.session.add(meter2)
        db.session.commit()

    now = datetime.utcnow()

    meter_data1 = MeterData(meter_id=meter1.id, timestamp=now, value=10)
    meter_data2 = MeterData(meter_id=meter1.id, timestamp=now + timedelta(hours=1), value=random.randint(1, 1000))
    meter_data3 = MeterData(meter_id=meter2.id, timestamp=now + timedelta(hours=2), value=random.randint(1, 1000))
    meter_data4 = MeterData(meter_id=meter2.id, timestamp=now + timedelta(hours=3), value=random.randint(1, 1000))
    db.session.add(meter_data1)
    db.session.add(meter_data2)
    db.session.add(meter_data3)
    db.session.add(meter_data4)
    db.session.commit()


@app.route('/meters/<int:meter_id>/')
def get_meter_data(meter_id):
    meter = Meter.query.get(meter_id)
    data = MeterData.query.filter_by(meter_id=meter.id).order_by(MeterData.timestamp).all()
    return jsonify({'label': meter.label, 'data': [d.to_dict() for d in data]})


@app.route('/meters/')
def list_meters():
    meters = Meter.query.all()
    return render_template('meter_list.html', meters=meters)


if __name__ == '__main__':
    app.run()
