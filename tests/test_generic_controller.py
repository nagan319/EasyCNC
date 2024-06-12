"""
Author: nagan319
Date: 2024/06/01
"""

import os
import tempfile
import pytest
from pytest import raises
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from src.app.controllers.generic_controller import GenericController 

"""
Tests for GenericController class using a sample database.

Test coverage:
    - Initialization
        - Test valid image preview directory
        - Test invalid image preview directory handling
    - Add item to DB
        - Test valid item adding correctly
        - Test smooth handling of invalid input
    - Remove item and preview
        - Test removal of valid item and preview path
        - Test removal of item with no preview image
        - Test removing item with invalid index handles smoothly
    - Remove item from DB
        - Test removing valid item
        - Test invalid item handling correctly
    - Remove all items from DB
        - Test database with no items
        - Test database with items
    - Get all items in DB
        - Test database with no items
        - Test database with items
    - Get attribute of item
        - Test getting valid attribute of item
        - Test invalid item
        - Test invalid attribute
    - Get amount of items in DB
        - Test database with no items 
        - Test database with items
    - Edit attribute of item in DB
        - Test setting attribute with valid value
        - Test setting attribute to invalid type
        - Test invalid item
        - Test invalid attribute
    - Get image preview path of item
        - Test that preview path == preview directory + id.png
        - Test null input
"""

Base = declarative_base()

class SampleTable(Base):
    __tablename__ = 'sample_table'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope="module")
def Base():
    return declarative_base()

@pytest.fixture(scope="module")
def session_factory(engine, Base):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

@pytest.fixture(scope="function")
def session(session_factory, Base):
    session = session_factory()
    yield session
    session.close()

@pytest.fixture(scope="function", autouse=True)
def create_sample_table(engine):
    SampleTable.__table__.create(bind=engine)
    yield
    SampleTable.__table__.drop(bind=engine)

@pytest.fixture
def controller(session, temp_dir):
    preview_image_directory = temp_dir
    controller = GenericController(session, SampleTable, str(preview_image_directory))
    yield controller

def test_initialization_with_invalid_directory(session):
    with raises(FileNotFoundError):
        controller = GenericController(session, SampleTable, "invalid directory")

def test_add_valid_item(controller, session):
    item = SampleTable(name="TestItem", description="This is a test item.")
    controller._add_item_to_db(item)
    retrieved_item = session.query(SampleTable).filter_by(name="TestItem").first()
    assert retrieved_item is not None
    assert retrieved_item.name == "TestItem"
    assert retrieved_item.description == "This is a test item."

def test_add_invalid_item(controller, session): # ignores invalid input
    item = "invalid type"
    controller._add_item_to_db(item)

def test_remove_item_and_preview_path(controller, session):
    item = SampleTable(name="ToRemove", description="Item to be removed")
    session.add(item)
    session.commit()

    item_id = item.id
    preview_file_path = controller._get_preview_image_path(item_id)

    print("Preview File Path:", preview_file_path)

    with open(preview_file_path, 'w') as file:
        file.write("This is a test file.")    

    controller._remove_item_and_preview(item_id)
    
    retrieved_item = session.query(SampleTable).filter_by(id=item_id).first()
    assert retrieved_item is None
    assert not os.path.exists(controller._get_preview_image_path(item_id))

def test_remove_item_without_preview(controller, session):
    item = SampleTable(name="ToRemove", description="Item to be removed")
    session.add(item)
    session.commit()

    item_id = item.id
    preview_file_path = controller._get_preview_image_path(item_id)

    controller._remove_item_and_preview(item_id)
    
    retrieved_item = session.query(SampleTable).filter_by(id=item_id).first()
    assert retrieved_item is None
    assert not os.path.exists(controller._get_preview_image_path(item_id))

def test_remove_item_and_preview_invalid_index(controller, session):
    assert not controller._remove_item_and_preview("invalid id")

def test_remove_item_from_db_valid_index(controller, session):
    item = SampleTable(name="ToRemove", description="Item to be removed")
    session.add(item)
    session.commit()

    item_id = item.id
    controller._remove_item_from_db(item_id)

    retrieved_item = session.query(SampleTable).filter_by(id=item_id).first()
    assert retrieved_item is None

def test_remove_item_from_db_invalid_index(controller, session):
    assert not controller._remove_item_from_db("invalid id")

def test_remove_all_empty_db(controller, session):
    controller._remove_all_items_from_db()
    items = session.query(SampleTable).all()
    assert len(items) == 0

def test_remove_all_items_from_db(controller, session):
    item1 = SampleTable(name="ItemToRemove1", description="Item 1")
    item2 = SampleTable(name="ItemToRemove2", description="Item 2")
    session.add_all([item1, item2])
    session.commit()
    
    controller._remove_all_items_from_db()
    items = session.query(SampleTable).all()
    assert len(items) == 0

def test_remove_all_items_and_previews_empty_db(controller, session):
    assert controller._remove_all_items_and_previews()
    items = session.query(SampleTable).all()
    assert len(items) == 0

def test_remove_all_items_and_previews(controller, session, temp_dir):
    item1 = SampleTable(name="ItemToRemove1", description="Item 1")
    item2 = SampleTable(name="ItemToRemove2", description="Item 2")
    session.add_all([item1, item2])
    session.commit()

    preview_file_path1 = controller._get_preview_image_path(item1.id)
    preview_file_path2 = controller._get_preview_image_path(item2.id)

    with open(preview_file_path1, 'w') as file1:
        file1.write("This is a test file 1.")
    with open(preview_file_path2, 'w') as file2:
        file2.write("This is a test file 2.")

    assert os.path.exists(preview_file_path1)
    assert os.path.exists(preview_file_path2)

    assert controller._remove_all_items_and_previews()

    items = session.query(SampleTable).all()
    assert len(items) == 0
    assert not os.path.exists(preview_file_path1)
    assert not os.path.exists(preview_file_path2)

def test_get_all_empty_db(controller, session):
    items = controller._get_all_items()
    assert len(items) == 0
    assert items == []

def test_get_all_items(controller, session):
    item1 = SampleTable(name="Item1", description="First item")
    item2 = SampleTable(name="Item2", description="Second item")
    session.add_all([item1, item2])
    session.commit()
    
    items = controller._get_all_items()
    assert len(items) == 2
    assert items[0].name == "Item1"
    assert items[1].name == "Item2"

def test_get_item_attr_valid(controller, session):
    item = SampleTable(name="AttrItem", description="Item with attributes")
    session.add(item)
    session.commit()
    
    item_id = item.id
    name = controller._get_item_attr(item_id, "name")
    description = controller._get_item_attr(item_id, "description")
    
    assert name == "AttrItem"
    assert description == "Item with attributes"

def test_get_item_attr_invalid_item(controller, session):
    assert controller._get_item_attr("invalid id", "random attr") is None

def test_get_item_attr_invalid_attr(controller, session):
    item = SampleTable(name="AttrItem", description="Item with attributes")
    session.add(item)
    session.commit()

    item_id = item.id
    assert controller._get_item_attr(item_id, "invalid attr") is None

def test_get_item_amount_empty_db(controller, session):
    amount = controller._get_item_amount()
    assert amount == 0

def test_get_item_amount(controller, session):
    session.query(SampleTable).delete()
    session.commit()
    
    item1 = SampleTable(name="CountItem1", description="Item 1")
    item2 = SampleTable(name="CountItem2", description="Item 2")
    session.add_all([item1, item2])
    session.commit()
    
    amount = controller._get_item_amount()
    assert amount == 2

def test_edit_item_attr_valid(controller, session):
    item = SampleTable(name="EditItem", description="Item to edit")
    session.add(item)
    session.commit()
    
    item_id = item.id
    updated_item = controller._edit_item_attr(item_id, "description", "Updated description")
    
    assert updated_item is not None
    assert updated_item.description == "Updated description"

def test_edit_item_attr_invalid_type(controller, session):
    initial_description = "Item to edit"
    item = SampleTable(name="EditItem", description=initial_description)
    session.add(item)
    session.commit()
    
    item_id = item.id
    assert controller._edit_item_attr(item_id, "description", 5567) is None

    assert item.description == initial_description

def test_edit_item_attr_invalid_item(controller, session):
    assert controller._edit_item_attr("invalid id", "description", "") is None

def test_edit_item_attr_invalid_attr(controller, session):
    item = SampleTable(name="EditItem", description="description")
    assert controller._edit_item_attr(item.id, "invalid attr", "sfe") is None 

def test_get_image_preview_path(controller, session):
    assert controller._get_preview_image_path("id") == os.path.join(controller.preview_image_directory, "id.png")

def test_get_image_preview_path_null_value(controller, session):
    with raises(ValueError):
        controller._get_preview_image_path(None) 
        controller._get_preview_image_path("") 
