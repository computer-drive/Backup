from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class LoadingWidget(QWidget):
    def __init__(self, title: str, content: str, parent: QWidget = None):
        super().__init__(parent)

        self.title = title
        self.content = content

        self.setWindowTitle(self.title)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self.content))
        self.setLayout(layout)


