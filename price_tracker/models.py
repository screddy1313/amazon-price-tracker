
from price_tracker import db

trackers = db.Table('trackers',
    db.Column('uid', db.Integer(), db.ForeignKey('user.id')),
    db.Column('pid', db.Integer(), db.ForeignKey('product.id'))

)

class User(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), default='user')
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    prods_list = db.relationship('Product',secondary='trackers',
                        backref=db.backref('users', lazy=True))


    def __repr__(self) -> str:
        return f'User : {self.email}'


class Product(db.Model) :

    id = db.Column(db.Integer, primary_key = True)
    img_id = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    mrp = db.Column(db.Integer)
    current = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f'{self.title}'





