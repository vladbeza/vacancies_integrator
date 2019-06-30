from integrator.models import db, Job


def remove_duplicates():
    print("Remove duplications")
    jobs = db.session.query(Job).all()
    for job in jobs:
        same = []
        if job.dou_id is not None:
            same = db.session.query(Job).filter_by(dou_id=job.dou_id).all()

        if job.djinni_id is not None:
            same = db.session.query(Job).filter_by(
                djinni_id=job.djinni_id).all()

        if len(same) > 1:
            for j in same[1:]:
                print("Remove {}, {}".format(j.dou_id, j.djinni_id))
                db.session.delete(j)
                db.session.commit()
