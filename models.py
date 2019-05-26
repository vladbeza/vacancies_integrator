from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

locations = db.Table("locations",
                     db.Column("job_id", db.Integer, db.ForeignKey("jobs.id")),
                     db.Column("city_id", db.Integer, db.ForeignKey("cities.id"))
                     )


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64))
    dou_id = db.Column(db.String(64), default=None)
    description = db.Column(db.UnicodeText())
    details_link = db.Column(db.String(64))
    cities = db.relationship("City",
                              secondary=locations,
                              backref=db.backref("jobs", lazy="dynamic"),
                              lazy="dynamic")

    company = db.Column(db.String(64))
    salary = db.Column(db.String(64), default=None)
    active = db.Column(db.Boolean, default=True)
    remote = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
