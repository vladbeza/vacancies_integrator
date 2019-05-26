from integrator.models import db, Job


def remove_duplicates():
    jobs = db.session.query(Job).all()
    for job in jobs:
        same_dou_id = db.session.query(Job).filter_by(dou_id=job.dou_id).all()
        if len(same_dou_id) > 1:
            for j in same_dou_id[1:]:
                db.session.delete(j)
                db.session.commit()
