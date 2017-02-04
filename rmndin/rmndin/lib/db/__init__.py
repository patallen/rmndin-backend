def commit_session(db):
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
