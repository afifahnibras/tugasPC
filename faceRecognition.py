import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QComboBox, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class FaceDetectionFeatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Face Detection')
        self.setGeometry(0, 0, 800, 600)  # Adjusted window size
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        # Main layout for the face detection feature
        layout = QVBoxLayout()

        # Upload button for face detection image
        self.upload_button = QPushButton('Upload Face Image', self)
        self.upload_button.setFixedSize(150, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.upload_button.clicked.connect(self.upload_face_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        # Blur level selector with fixed size and minimal design
        self.blur_selector = QComboBox(self)
        self.blur_selector.setFixedSize(150, 30)
        self.blur_selector.setStyleSheet("background-color: #ffffff; border: 1px solid #cccccc;")
        self.blur_selector.addItems(['Select Blur Level', 'Low', 'Medium', 'High'])
        self.blur_selector.currentIndexChanged.connect(self.apply_blur)
        layout.addWidget(self.blur_selector)

        # Face detection image label
        self.face_image_label = QLabel('Face Detection Image', self)
        self.face_image_label.setAlignment(Qt.AlignCenter)
        self.face_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.face_image_label.setFixedHeight(400)
        layout.addWidget(self.face_image_label)

        # Set main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.face_image = None
        self.faces = []

    def upload_face_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.face_image = cv2.imread(file_name)
            self.detect_faces()

    def detect_faces(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(self.face_image, cv2.COLOR_BGR2GRAY)
        self.faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.face_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        self.display_face_image(self.face_image)

    def apply_blur(self):
        if self.face_image is not None and len(self.faces) > 0:
            blur_level = self.blur_selector.currentText()
            if blur_level == 'Low':
                ksize = (31, 31) 
            elif blur_level == 'Medium':
                ksize = (51, 51)
            elif blur_level == 'High':
                ksize = (71, 71)
            else:
                return  # No blur applied if selection is 'Select Blur Level'

            blurred_image = self.face_image.copy()
            for (x, y, w, h) in self.faces:
                face_region = self.face_image[y:y + h, x:x + w]
                blurred_face = cv2.GaussianBlur(face_region, ksize, 0)
                blurred_image[y:y + h, x:x + w] = blurred_face

            self.display_face_image(blurred_image)

    def display_face_image(self, image):
        q_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        self.face_image_label.setPixmap(pixmap.scaled(self.face_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.face_image_label.setAlignment(Qt.AlignCenter)
