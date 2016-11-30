from duopoet import app, db
from flask_security import RoleMixin, UserMixin

roles_members = db.Table(
    'roles_members',
    db.Column('member_id', db.Integer(), db.ForeignKey('member.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))



class Member(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    # first_name = db.Column(db.String(100), nullable=False)
    # last_name = db.Column(db.String(100), nullable=False)


    # added for Flask Security
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_members,
                            backref=db.backref('members', lazy='dynamic'))

    fragments_owned = db.relationship('Fragment', backref=db.backref('owner'))
    poems_owened = db.relationship('Poem', backref=db.backref('owner'))


#  many-to-many
#  http://flask-sqlalchemy.pocoo.org/2.1/models/

fragments = db.Table('fragments',
	db.Column('fragment_id', db.Integer(), db.ForeignKey('fragment.id')),
	db.Column('poem_id', db.Integer(), db.ForeignKey('poem.id'))
)


class Fragment(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	text = db.Column(db.String(250), nullable=False, unique=True)
	date_uploaded = db.Column(db.Date(), nullable=False)
	creator = db.Column(db.Integer(), db.ForeignKey('member.id'))


class Poem(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	fragment_order = db.Column(db.PickleType, nullable=False)

	fragments = db.relationship('Fragment', secondary=fragments,
		backref=db.backref('poems', lazy='dynamic'))

	author = db.Column(db.Integer(), db.ForeignKey('member.id'))

