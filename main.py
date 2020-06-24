import PySide2
import sys
from PySide2.QtWidgets import QPushButton, QLineEdit, QApplication, QVBoxLayout, QGridLayout, QWidget, QFileDialog
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from cryptography.fernet import Fernet
import os
WIDGET_HEIGHT = 40


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Berlin Sans FB", 10))
        self.setWindowTitle("File ENC")
        self.setFixedSize(500, 220)

        self.btn_src = QPushButton("browse")
        self.btn_dst = QPushButton("browse")
        self.btn_enc = QPushButton("Encrypt")
        self.btn_dec = QPushButton("Decrypt")
        self.btn_src.setFixedSize(60, WIDGET_HEIGHT)
        self.btn_dst.setFixedSize(60, WIDGET_HEIGHT)
        self.btn_src.clicked.connect(self.open_file_dialog)
        self.btn_dst.clicked.connect(self.open_dir_dialog)
        self.btn_enc.clicked.connect(self.encrypt_file)
        self.btn_dec.clicked.connect(self.decrypt_file)

        self.LE_file_path = QLineEdit()
        self.LE_file_path.setPlaceholderText("Source File Path...")
        self.LE_file_path.setFixedHeight(WIDGET_HEIGHT)
        self.LE_file_path.setReadOnly(True)

        self.LE_dir_path = QLineEdit()
        self.LE_dir_path.setPlaceholderText("Destination Path...")
        self.LE_dir_path.setFixedHeight(WIDGET_HEIGHT)
        self.LE_dir_path.setReadOnly(True)

        self.LE_key = QLineEdit()
        self.LE_key.setPlaceholderText("Enter the Cipher Key...")
        self.LE_key.setFixedHeight(WIDGET_HEIGHT)

        layout = QGridLayout()
        layout.setRowMinimumHeight(0, 30)
        layout.addWidget(self.btn_src, 0, 1)
        layout.addWidget(self.btn_dst, 1, 1)
        layout.addWidget(self.btn_enc, 3, 0, 1, 2, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn_dec, 4, 0, 1, 2, alignment=Qt.AlignHCenter)
        layout.addWidget(self.LE_file_path, 0, 0)
        layout.addWidget(self.LE_dir_path, 1, 0)
        layout.addWidget(self.LE_key, 2, 0, 1, 2)
        layout.setHorizontalSpacing(10)
        layout.setHorizontalSpacing(0)
        print(layout.rowStretch(0))
        self.setLayout(layout)
        self.show()

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, "Select File")
        self.LE_file_path.setText(fname[0])

    def open_dir_dialog(self):
        file = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.LE_dir_path.setText(file)

    def encrypt_file(self):
        cipher = Fernet(self.LE_key.text())
        with open(self.LE_file_path.text(), 'rb') as f:
            data = f.read()
        with open(f"{self.LE_dir_path.text()}\\enc_{os.path.basename(self.LE_file_path.text())}", 'wb') as f:
            f.write(cipher.encrypt(data))

    def decrypt_file(self):
        cipher = Fernet(self.LE_key.text())
        with open(self.LE_file_path.text(), 'rb') as f:
            data = f.read()
        with open(f"{self.LE_dir_path.text()}\\dec_{os.path.basename(self.LE_file_path.text())}", 'wb') as f:
            f.write(cipher.decrypt(data))


if __name__ == "__main__":
    app = QApplication()
    window = Window()
    sys.exit(app.exec_())
