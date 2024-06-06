'''
Author: nagan319
Date: 2024/06/01
'''

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.plate_model import Plate

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

@pytest.fixture
def session():
    session = Session()
    Plate.metadata.create_all(engine)
    yield session
    session.rollback()
    Plate.__table__.drop(engine)  
    session.close()

@pytest.fixture
def sample_plate_data():
    return {
        'x': 1000,
        'y': 1000,
        'z': 1000,
        'material': 'Aluminum',
        'contours': 'some_contours_data'
    }

'''
Test CRUD logic for Plate class.
'''

def test_create_plate(session, sample_plate_data):
    plate = Plate(**sample_plate_data)
    session.add(plate)
    session.commit()
    assert plate.id is not None
    assert session.query(Plate).filter_by(id=plate.id).first() is not None

def test_read_plate(session, sample_plate_data):
    plate = Plate(**sample_plate_data)
    session.add(plate)
    session.commit()
    retrieved_plate = session.query(Plate).filter_by(id=plate.id).first()
    assert retrieved_plate is not None
    assert retrieved_plate.x == sample_plate_data['x']

def test_update_plate(session, sample_plate_data):
    plate = Plate(**sample_plate_data)
    session.add(plate)
    session.commit()
    plate.material = 'Steel'
    session.commit()
    updated_plate = session.query(Plate).filter_by(id=plate.id).first()
    assert updated_plate is not None
    assert updated_plate.material == 'Steel'

def test_delete_plate(session, sample_plate_data):
    plate = Plate(**sample_plate_data)
    session.add(plate)
    session.commit()
    session.delete(plate)
    session.commit()
    assert session.query(Plate).filter_by(id=plate.id).first() is None
