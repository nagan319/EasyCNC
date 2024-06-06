"""
Author: nagan319
Date: 2024/06/01
"""

import os
from typing import Union, TypeVar, Type, List
from sqlalchemy.orm import Session

from ..logging import logger

T = TypeVar('T')

# add remove all items and previews method

class GenericController:
    """
    Generic controller containing basic CRUD logic. Used as superclass in controllers linked to SQL DB.
    ### Parameters:
    - session: working session.
    - db_table: table ORM class.
    - preview_image_directory: directory for storing preview images. 
    """
    def __init__(self, session: Session, db_table: Type[T], preview_image_directory: str):
        if not os.path.exists(preview_image_directory):
            logger.error(f"Attempted to create controller with invalid preview image directory: {preview_image_directory}")
            raise FileNotFoundError()
        self.session = session
        self.db_table = db_table
        self.preview_image_directory = preview_image_directory

    def _add_item_to_db(self, item: T) -> None:
        """
        Add new item to db.
        """
        try:
            self.session.add(item)
            self.session.commit()
            logger.debug(f"Item with id {getattr(item, 'id', 'unknown')} added successfully.")
        except Exception as e:
            logger.error(f"Encountered exception while adding item with id {getattr(item, 'id', 'unknown')}: {e}")
            self.session.rollback()    

    def _remove_item_and_preview(self, id: str) -> bool:
        """
        Remove item from db and delete preview image.
        Returns True if successful, False otherwise.
        """       
        item = self.session.query(self.db_table).filter(self.db_table.id == id).first()

        if not item:
            logger.error(f"Item with id {id} does not exist.")
            return False
        preview_path = self._get_preview_image_path(item.id)

        if not self._remove_item_from_db(id):
            return False
        
        if os.path.exists(preview_path):
            try:
                os.remove(preview_path)
            except Exception as e:
                logger.error(f"Error deleting preview image {preview_path}: {e}")
                return False  
        return True

    def _remove_item_from_db(self, id: str) -> bool:
        """
        Remove item with certain id from db. Returns True if removal is successful, False if item does not exist or an error is encountered.
        """
        try:
            item = self.session.query(self.db_table).filter(self.db_table.id == id).first()
            if not item:
                logger.error(f"Item with id {id} does not exist.")
                return False
            
            self.session.delete(item)
            self.session.commit()
            logger.debug(f"Item with id {id} removed successfully.")
            return True
        except Exception as e:
            logger.error(f"Encountered exception while removing item with id {id}: {e}")
            self.session.rollback()
            return False

    def _remove_all_items_from_db(self):
        """
        Remove all items of specified type from db.
        """
        try:
            self.session.query(self.db_table).delete()
            self.session.commit()
            logger.debug("Successfully cleared out data table.")
        except Exception as e:
            logger.error(f"Encountered error while attempting to clear out data table: {e}")
            self.session.rollback()

    def _get_all_items(self) -> List[T]:
        """
        Get all items stored in db table.
        """
        try:
            return self.session.query(self.db_table).all()
        except Exception as e:
            logger.error(f"Encountered error while attempting to retrieve all items from db.")
            return None

    def _get_item_attr(self, id: str, attr: str) -> Union[any, None]:
        """
        Get a certain attribute from an item. Returns None if the attribute doesn't exist.
        """
        item = self.session.query(self.db_table).filter(self.db_table.id == id).first()
        if not item:
            logger.error(f"Item with id {id} does not exist.")
            return None
        if not hasattr(item, attr):
            logger.error(f"Attribute {attr} does not exist on item with id {id}")
            return None
        return getattr(item, attr)
    
    def _get_item_amount(self) -> int:
        """
        Get amount of items in table. Returns -1 if an error is encountered.
        """
        try:
            item_count = self.session.query(self.db_table).count()
            return item_count
        except Exception as e:
            logger.error(f"Encountered error while retrieving amount of items: {e}")
            return -1

    def _edit_item_attr(self, id: str, attr: str, new_val: any) -> Union[T, None]:
        """
        Edit certain attribute of item. Returns modified item or None if an error occurs.
        """
        try:
            item = self.session.query(self.db_table).filter(self.db_table.id == id).first()
            if not item:
                logger.error(f"Item with id {id} does not exist.")
                return None
            if not hasattr(item, attr):
                logger.error(f"Attribute {attr} does not exist on item with id {id}")
                return None  

            if type(self._get_item_attr(id, attr)) != type(new_val):
                logger.error(f"New value for item parameter {attr} does not match intended type")
                return None

            setattr(item, attr, new_val)
            self.session.commit()
            logger.debug(f"Updated item id {id}: set {attr} to {new_val}")
            return item
        except Exception as e:
            logger.error(f"Error updating item with id {id}: {e}")
            self.session.rollback()
            return None

    def _get_preview_image_path(self, id: str) -> Union[str, None]:
        """ Get preview path from item id. Returns None for invalid input."""
        if id == "" or id is None:
            logger.error("Attempted to get preview image path of empty index.")
            raise ValueError()
        path = os.path.join(self.preview_image_directory, f"{id}.png")
        return path
    