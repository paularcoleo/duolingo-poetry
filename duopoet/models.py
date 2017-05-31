from duopoet import app, db

poems_fragments = db.Table('poems_fragments',
	db.Column('fragment_id', db.Integer(), db.ForeignKey('fragment.id')),
	db.Column('poem_id', db.Integer(), db.ForeignKey('poem.id'))
)


class Fragment(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	text = db.Column(db.String(250), nullable=False, unique=True)
	approved = db.Column(db.Boolean(), nullable=False, default=False)
	date_approved = db.Column(db.Date())
	date_uploaded = db.Column(db.Date(), nullable=False)

	def __str__(self):
		return self.text

	def __repr__(self):
		return self.text


class Poem(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	fragment_order = db.Column(db.PickleType, nullable=False)

	fragments = db.relationship('Fragment', secondary=poems_fragments,
		backref=db.backref('poems', lazy='dynamic'))

