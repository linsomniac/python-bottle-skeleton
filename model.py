
def initdb():
    dbwrap.connect()
    dbwrap.Base.metadata.create_all()
    model.create_sample_data(dbwrap.session())
