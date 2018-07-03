from sqlalchemy import func

from duopoet import app, db
from duopoet.models import Fragment, Poem

from datetime import datetime

class Service():
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('{} is not of type {}'.format(model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(*ids)).all()

    def find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)

    def new(self, **kwargs):
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()


class FragmentService(Service):
    __model__ = Fragment
    def __init__(self, *args, **kwargs):
        super(FragmentService, self).__init__(*args, **kwargs)

    def get_random_fragments(self, n):
        fragments = self.__model__.query.filter_by(approved=True).order_by(func.random()).limit(n).all()
        return fragments

    def get_unapproved_fragments(self, n):
        fragments = self.__model__.query.filter_by(approved=False).order_by(func.random()).limit(n).all()
        return fragments
    
    def lookup(self, text):
        fragment = self.find(text=text).first()
        return fragment

    def approve(self, fragment):
        return self.update(fragment, approved=True, date_approved=datetime.utcnow().date())

    def is_unique(self, text, id=None):
        dupe_fragment = self.lookup(text)
        if dupe_fragment:
            return True if dupe_fragment.id == id else False
        else:
            return True

class PoemService(Service):
    __model__ = Poem
    def __init__(self, *args, **kwargs):
        super(PoemService, self).__init__(*args, **kwargs)

    def create(self, fragments, fragment_order):
        new_poem = self.__model__(
            fragment_order=fragment_order,
            date_created=datetime.utcnow()
        )
        for fragment in fragments:
            new_poem.fragments.append(fragment)
        return self.save(new_poem)

    def get_most_recent(self, n=1):
        return self.__model__.query.order_by(self.__model__.date_created.desc()).limit(n).all()