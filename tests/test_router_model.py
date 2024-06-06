"""
Author: nagan319
Date: 2024/06/01
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.router_model import Router

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

@pytest.fixture
def session():
    session = Session()
    Router.metadata.create_all(engine)
    yield session
    session.rollback()
    Router.__table__.drop(engine)  
    session.close()

@pytest.fixture
def sample_router_data():
    return {
        'name': 'New CNC Router',
        'x': 750,
        'y': 1500,
        'z': 500,
        'plate_x': 1000,
        'plate_y': 2000,
        'plate_z': 500,
        'min_safe_dist_from_edge': 50,
        'drill_bit_diameter': 5,
        'mill_bit_diameter': 10
    }

'''
Test CRUD logic for Router class.
'''

def test_create_router(session, sample_router_data):
    router = Router(**sample_router_data)
    session.add(router)
    session.commit()
    assert router.id is not None
    assert session.query(Router).filter_by(id=router.id).first() is not None

def test_read_router(session, sample_router_data):
    router = Router(**sample_router_data)
    session.add(router)
    session.commit()
    retrieved_router = session.query(Router).filter_by(id=router.id).first()
    assert retrieved_router is not None
    assert retrieved_router.name == sample_router_data['name']

def test_update_router(session, sample_router_data):
    router = Router(**sample_router_data)
    session.add(router)
    session.commit()
    router.name = 'Updated Router'
    session.commit()
    updated_router = session.query(Router).filter_by(id=router.id).first()
    assert updated_router is not None
    assert updated_router.name == 'Updated Router'

def test_delete_router(session, sample_router_data):
    router = Router(**sample_router_data)
    session.add(router)
    session.commit()
    session.delete(router)
    session.commit()
    assert session.query(Router).filter_by(id=router.id).first() is None
