import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QComboBox, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageCropperWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Cropper')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Upload button for image
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(150, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        # Crop dimension selector
        self.crop_selector = QComboBox(self)
        self.crop_selector.setFixedSize(150, 40)  # Set fixed size similar to button
        self.crop_selector.addItems(['Select Crop Dimensions', '100x100', '200x200', '300x300'])
        self.crop_selector.currentIndexChanged.connect(self.crop_image)  # Trigger crop on selection change
        layout.addWidget(self.crop_selector)

        # Crop button
        #self.crop_button = QPushButton('Crop Image', self)
        #self.crop_button.setFixedSize(150, 40)
        #self.crop_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px;")
        #self.crop_button.clicked.connect(self.crop_image)
        #layout.addWidget(self.crop_button, alignment=Qt.AlignLeft)

        # Image display label
        self.image_label = QLabel('Image will be displayed here', self)
        self.image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.image_label.setFixedHeight(400)
        layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)

    def crop_image(self):
        if self.image is not None:
            crop_size = self.crop_selector.currentText()
            if crop_size == 'Select Crop Dimensions':
                QMessageBox.warning(self, 'Warning', 'Please select crop dimensions!')
                return
            
            # Get crop dimensions
            dimension = int(crop_size.split('x')[0])
            height, width = self.image.shape[:2]

            # Ensure crop dimensions do not exceed image dimensions
            if dimension > width or dimension > height:
                QMessageBox.warning(self, 'Warning', 'Crop dimensions exceed image dimensions!')
                return

            # Cropping the center of the image
            start_x = (width - dimension) // 2
            start_y = (height - dimension) // 2
            self.cropped_image = self.image[start_y:start_y + dimension, start_x:start_x + dimension]

            self.display_image(self.cropped_image)
        else:
            QMessageBox.warning(self, 'Warning', 'No image uploaded!')

    def display_image(self, image):
        # Convert the image to the appropriate format for QImage
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_image = QImage(image.tobytes(), width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)