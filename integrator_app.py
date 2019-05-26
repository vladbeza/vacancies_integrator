# -*- coding:utf-8 -*-

from integrator import create_app
from integrator.models import db, City, Job
from integrator.retrieve_info import gather_new_jobs_dou
from flask_migrate import Migrate
from integrator.scripts import remove_duplicates

CITIES = ["Харьков", "Киев", "Одесса", "Львов"]

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    for c in CITIES:
        city = db.session.query(City).filter(City.name == c).first()
        if city is None:
            city = City(name=c)
            db.session.add(city)
            db.session.commit()

    jobs = db.session.query(Job).all()
    if not jobs:
        gather_new_jobs_dou()

    remove_duplicates()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, City=City)
