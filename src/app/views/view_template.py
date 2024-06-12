from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

class ViewTemplate(QWidget): 
    """
    Generic template for views containing margins and title.
    """
    MARGIN_WIDTH = 1
    WIDGET_WIDTH = 68

    def __init__(self):
        super().__init__()

    def __init_template_gui__(self, title_text: str, core_widget: QWidget): 

        self.main_layout = QHBoxLayout()

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()

        self.title = QLabel(title_text)
        self.title.setObjectName("titleText")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content_layout.addWidget(self.title, 1)
        self.content_layout.addWidget(core_widget, 9)
        self.content_layout.addStretch(1)
        self.content_widget.setLayout(self.content_layout)

        self.main_layout.addStretch(self.MARGIN_WIDTH)
        self.main_layout.addWidget(self.content_widget, self.WIDGET_WIDTH)
        self.main_layout.addStretch(self.MARGIN_WIDTH)

        self.setLayout(self.main_layout)
