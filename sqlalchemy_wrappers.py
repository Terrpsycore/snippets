from collections.abc import Iterable

import dbase.models as models


def get(model, id):
    instance = query(model).get(id)
    return instance


def create(model, **kwargs):
    instance = getattr(models, model)(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def query(model, **kwargs):
    model = getattr(models, model)
    q = session.query(model)
    for name, value in kwargs.items():
        q = q.filter(getattr(model, name)==value)
    return q


def one(model, **kwargs):
    q = query(model, **kwargs)
    return q.one_or_none()


def every(model, **kwargs):
    q = query(model, **kwargs)
    return q.all()


def one_or_create(model, **kwargs):
    instance = one(model, **kwargs)
    if not instance:
        instance = create(model, **kwargs)
    return instance


def change(instance, **kwargs):
    for name, value in kwargs.items():
        setattr(instance, name, value)
    session.add(instance)
    session.commit()
    return


def relate(parent, child, field):
    relation = getattr(parent, field)
    if isinstance(relation, Iterable):
        if child not in relation:
            relation.append(child)
    else:
        setattr(parent, field, child)
    session.commit()
    return

def chain_relate(parent, children:list, field):
    for child in children:
        relate(parent, child, field)
    return
