from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    people = db.relationship('People', backref='planets', lazy=True)
    planet_favs = db.relationship('FavPlanet', backref="planets", lazy=True)

    def __repr__(self):
        return 'Planet %r' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "people": self.getPeople(),
        }
    
    def getPeople(self):
        return list(map(lambda x: x.serialize(), self.people))

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    planet = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # planet_name = db.relationship ('Planets', backref='people', lazy=True)
    people_favs = db.relationship('FavPeople', backref="people", lazy=True)

    def __repr__(self):
        return 'People %r' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "planet": self.planet
        }

class FavPeople(db.Model):
    __tablename__ = "favpeople"
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "person_name": self.people.name,
            "user": self.user_id
        }

class FavPlanet(db.Model):
    __tablename__ = "favplanets"
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id,
            "planet name": self.planets.name
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'User %r' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }