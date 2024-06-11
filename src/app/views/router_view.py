"""
Author: nagan319
Date: 2024/06/11
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea
from .view_template import ViewTemplate

from ..controllers.router_controller import RouterController

from ..logging import logger

class RouterView(ViewTemplate):
    """
    View for handling routers. 
    """
    def __init__(self, session, router_preview_dir: str):
        super().__init__()
        self._setup_ui()

        self.controller = RouterController(session, router_preview_dir)

        logger.debug("Successfully initialized RouterView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.content_widget)

        self.import_button = QPushButton()

        import_button_wrapper = QWidget()
        import_button_wrapper_layout = QHBoxLayout()
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper_layout.addWidget(self.import_button, 1)
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper.setLayout(import_button_wrapper_layout)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area, 7)
        main_layout.addWidget(self.import_button, 1)
        main_widget.setLayout(main_layout)

        self.__init_template_gui__("Manage Routers", main_widget)
    
    # use import file functionality in controller, define preview location
    def import_files(self):
        pass

    # reference controller method
    def on_material_edited(self, part_id: str, new_val: str):
        pass

    # assuming this takes a string
    def on_amount_edited(self, part_id: str, new_val: str):
        pass

    # use controller delete functionality
    def on_delete_requested(self, part_id: str):
        pass

    # use controller 'get total amount' method
    def _update_button_amount(self):
        pass
