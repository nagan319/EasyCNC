"""
Author: nagan319
Date: 2024/06/01
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.part_model import Part

'''
Test CRUD logic for part class.
'''

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

@pytest.fixture
def session():
    session = Session()
    Part.metadata.create_all(engine)
    yield session
    session.rollback()
    Part.__table__.drop(engine)  
    session.close()
    
@pytest.fixture
def sample_part_data():
    return {
        'filename': 'test_part.stl',
        'thickness': 5.0,
        'material': 'Steel',
        'contours': 'some_contours_data',
        'amount': 1
    }

def test_create_part(session, sample_part_data):
    part = Part(**sample_part_data)
    session.add(part)
    session.commit()
    assert part.id is not None
    assert session.query(Part).filter_by(id=part.id).first() is not None

def test_read_part(session, sample_part_data):
    part = Part(**sample_part_data)
    session.add(part)
    session.commit()
    retrieved_part = session.query(Part).filter_by(id=part.id).first()
    assert retrieved_part is not None
    assert retrieved_part.filename == sample_part_data['filename']

def test_update_part(session, sample_part_data):
    part = Part(**sample_part_data)
    session.add(part)
    session.commit()
    part.material = 'Aluminum'
    session.commit()
    updated_part = session.query(Part).filter_by(id=part.id).first()
    assert updated_part is not None
    assert updated_part.material == 'Aluminum'

def test_delete_part(session, sample_part_data):
    part = Part(**sample_part_data)
    session.add(part)
    session.commit()
    session.delete(part)
    session.commit()
    assert session.query(Part).filter_by(id=part.id).first() is None
