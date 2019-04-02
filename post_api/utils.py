def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}
