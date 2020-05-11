from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from config import CITIES, languages

db = SQLAlchemy()

locations = db.Table("locations",
                     db.Column("job_id", db.Integer, db.ForeignKey("jobs.id")),
                     db.Column("city_id", db.Integer, db.ForeignKey("cities.id"))
                     )

programm_langs_in_job = db.Table("programm_langs_in_job",
                     db.Column("job_id", db.Integer, db.ForeignKey("jobs.id")),
                     db.Column("language_id", db.Integer, db.ForeignKey("languages.id"))
                     )


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    @staticmethod
    def add_cities():
        for c in CITIES:
            city = db.session.query(City).filter(City.name == c).first()
            if city is None:
                city = City(name=c)
                db.session.add(city)
                db.session.commit()


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    @staticmethod
    def add_langs():
        for lang in languages:
            if lang != "Any":
                lang_obj = db.session.query(Language).filter(
                    Language.name == lang).first()
                if lang_obj is None:
                    lang_obj = Language(name=lang)
                    db.session.add(lang_obj)
                    db.session.commit()


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(128))
    dou_id = db.Column(db.String(128), default=None)
    description = db.Column(db.UnicodeText())
    details_link = db.Column(db.String(128))
    cities = db.relationship("City",
                             secondary=locations,
                             backref=db.backref("jobs", lazy="dynamic"),
                             lazy="dynamic")
    company = db.Column(db.String(128))
    salary = db.Column(db.String(64), default=None)
    active = db.Column(db.Boolean, default=True)
    remote = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    djinni_id = db.Column(db.String(64), default=None)
    is_automation = db.Column(db.Boolean, default=False)
    languages = db.relationship("Language",
                                secondary=programm_langs_in_job,
                                backref=db.backref("jobs", lazy="dynamic"),
                                lazy="dynamic")
