import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ChainCodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chain Code Feature")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QHBoxLayout()

        # Left: Original image
        self.image_label = QLabel("No Image Selected", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 400)
        layout.addWidget(self.image_label)

        # Right: Chain code display
        right_layout = QVBoxLayout()

        self.chain_code_display = QTextEdit(self)
        self.chain_code_display.setReadOnly(True)
        right_layout.addWidget(self.chain_code_display)

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        right_layout.addWidget(self.load_button)

        self.generate_button = QPushButton("Generate Chain Code", self)
        self.generate_button.clicked.connect(self.generate_chain_code)
        self.generate_button.setEnabled(False)
        right_layout.addWidget(self.generate_button)

        layout.addLayout(right_layout)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))
            self.generate_button.setEnabled(True)

    def generate_chain_code(self):
        original_image, chain_code = process_image(self.image_path)

        # Display the original image
        height, width = original_image.shape
        bytes_per_line = width
        q_image = QImage(original_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio))

        # Display the chain code
        self.chain_code_display.setText("Chain Code:\n" + " ".join(map(str, chain_code)))


def process_image(image_path):
    # Load the image
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(original_image, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return original_image, []

    # Use the largest contour
    contour = max(contours, key=cv2.contourArea)

    # Convert contour points into chain code
    chain_code = []

    # Define directions
    directions = [0, 1, 2, 3, 4, 5, 6, 7]
    change_i = [-1, -1, 0, 1, 1, 1, 0, -1]
    change_j = [0, 1, 1, 1, 0, -1, -1, -1]

    for i in range(len(contour)):
        p1 = contour[i][0]  # Titik saat ini
        p2 = contour[(i + 1) % len(contour)][0]  # Titik berikutnya

        # Determine direction
        delta_i = p2[1] - p1[1]
        delta_j = p2[0] - p1[0]

        for d in directions:
            if delta_i == change_i[d] and delta_j == change_j[d]:
                chain_code.append(d)
                break

    return original_image, chain_code


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChainCodeWindow()
    window.show()
    sys.exit(app.exec_())
