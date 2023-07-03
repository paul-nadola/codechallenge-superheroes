from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower
from app import app

fake = Faker()

# Initialize the database
# db.init_app(app)

def seed_heroes(num_heroes):
    db.session.query(Hero).delete()
    db.session.commit()
    for _ in range(num_heroes):
        hero = Hero(
            name=fake.name(),
            super_name=fake.name()
        )
        db.session.add(hero)
    
    db.session.commit()

def seed_powers(num_powers):
    db.session.query(Power).delete()
    db.session.commit()
    for _ in range(num_powers):
        power = Power(
            name=fake.word(),
            description=fake.text()
        )
        db.session.add(power)
    
    db.session.commit()

def seed_hero_powers(num_hero_powers):
    db.session.query(HeroPower).delete()
    db.session.commit()
    heroes = Hero.query.all()
    powers = Power.query.all()
    strengths = ['Strong', 'Weak', 'Average']
    for _ in range(num_hero_powers):
        hero = fake.random_element(heroes)
        power = fake.random_element(powers)
        strength = fake.random_element(strengths)
        
        hero_power = HeroPower(
            strength=strength,
            hero_name=hero.name,
            power_name=power.name
        )
        db.session.add(hero_power)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Seed data
        seed_heroes(10)
        seed_powers(5)
        seed_hero_powers(20)

print("Done!")
