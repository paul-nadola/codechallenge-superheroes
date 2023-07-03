from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    heropower = db.relationship('HeroPower', backref='heroes')
    def __repr__(self):
        return f' Hero Name: {self.name}'
    

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heropower = db.relationship('HeroPower', backref='powers')

    @validates('description')
    def validate_description(self, key, description):
        if len(description.strip()) < 20:
            raise ValueError('Description must be at least 20 characters long.')
        return description

    def __repr__(self):
            return f' Power Name: {self.name}'
    
class HeroPower(db.Model, SerializerMixin):
     __tablename__ = 'hero_powers'

     id = db.Column(db.Integer, primary_key=True)
     strength = db.Column(db.String)
     hero_name = db.Column(db.Integer, db.ForeignKey('heroes.name'))
     power_name = db.Column(db.Integer, db.ForeignKey('powers.name'))
     created_at = db.Column(db.DateTime, server_default=db.func.now())
     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

     @validates('strength')
     def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError('Strength must be one of the following values: Strong, Weak, Average.')
        return strength

     

     def __repr__(self):
            return f' Hero Name: {self.power_name} Hero Power: {self.power_name}'


# add any models you may need. 