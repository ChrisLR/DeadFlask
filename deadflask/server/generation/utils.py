def get_or_create(session, model, template, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        session.add(template)
        session.commit()
        return template
