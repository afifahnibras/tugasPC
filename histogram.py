import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class HistogramFeatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Histogram')
        self.setGeometry(0, 0, 1200, 1000)  # Enlarged window size
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        # Add scroll area to handle large content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Main widget for scrollable content
        main_widget = QWidget()
        scroll.setWidget(main_widget)

        # Main layout for the app
        main_layout = QVBoxLayout(main_widget)

        # Upload button for the image to process
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(120, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.upload_button.clicked.connect(self.upload_image)
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        # Layout for the original image and histogram
        original_layout = QHBoxLayout()

        # Widget to hold the original image and histogram
        original_image_histogram_widget = QWidget()
        original_image_histogram_layout = QHBoxLayout(original_image_histogram_widget)

        # Label to display the original image
        self.image_label = QLabel('Original Image', self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.image_label.setFixedWidth(400)
        self.image_label.setFixedHeight(400)
        original_image_histogram_layout.addWidget(self.image_label)

        # Canvas to show the original histogram
        self.canvas_original = FigureCanvas(Figure())
        self.canvas_original.setFixedWidth(600)  # Increased width for histogram
        self.canvas_original.setFixedHeight(400)
        original_image_histogram_layout.addWidget(self.canvas_original)

        original_layout.addWidget(original_image_histogram_widget)
        main_layout.addLayout(original_layout)

        # Layout for the equalized image and histogram
        equalized_layout = QHBoxLayout()  # Changed to QHBoxLayout

        # Widget to hold the equalized image and histogram
        equalized_image_histogram_widget = QWidget()
        equalized_image_histogram_layout = QHBoxLayout(equalized_image_histogram_widget)  # Changed to QHBoxLayout

        # Label to display the equalized image
        self.equalized_image_label = QLabel('Equalized Image', self)
        self.equalized_image_label.setAlignment(Qt.AlignCenter)
        self.equalized_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.equalized_image_label.setFixedWidth(400)
        self.equalized_image_label.setFixedHeight(400)
        equalized_image_histogram_layout.addWidget(self.equalized_image_label)

        # Canvas to show the equalized histogram
        self.canvas_equalization = FigureCanvas(Figure())
        self.canvas_equalization.setFixedWidth(600)  # Increased width for histogram
        self.canvas_equalization.setFixedHeight(400)
        equalized_image_histogram_layout.addWidget(self.canvas_equalization)

        equalized_layout.addWidget(equalized_image_histogram_widget)
        main_layout.addLayout(equalized_layout)


        # Layout for grayscale image and histogram
        grayscale_layout = QHBoxLayout()

        # Widget to hold the grayscale image and histogram
        grayscale_image_histogram_widget = QWidget()
        grayscale_image_histogram_layout = QHBoxLayout(grayscale_image_histogram_widget)

        # Label to display the grayscale image
        self.grayscale_image_label = QLabel('Grayscale Image', self)
        self.grayscale_image_label.setAlignment(Qt.AlignCenter)
        self.grayscale_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.grayscale_image_label.setFixedWidth(400)
        self.grayscale_image_label.setFixedHeight(400)
        grayscale_image_histogram_layout.addWidget(self.grayscale_image_label)

        # Canvas to show the grayscale histogram
        self.canvas_grayscale = FigureCanvas(Figure())
        self.canvas_grayscale.setFixedWidth(600)  # Increased width for histogram
        self.canvas_grayscale.setFixedHeight(400)
        grayscale_image_histogram_layout.addWidget(self.canvas_grayscale)

        grayscale_layout.addWidget(grayscale_image_histogram_widget)
        main_layout.addLayout(grayscale_layout)

        # Set the scroll area as the central widget
        self.setCentralWidget(scroll)

    # Function to upload the image for histogram and equalization
    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.display_image(file_name, self.image_label)
            self.process_image(file_name)

    # Function to display the image in the QLabel
    def display_image(self, file_name, label):
        pixmap = QPixmap(file_name)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)

    # Function to process and equalize the image, displaying histogram
    def process_image(self, file_name):
        image = cv2.imread(file_name)

        if image is None:
            print("Gambar tidak terbaca dengan benar!")
            return

        # Convert image to RGB for matplotlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Show the original histogram
        self.show_histogram(image_rgb, 'Histogram Original', self.canvas_original)

        # Equalization process
        image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
        equalized_image = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

        # Display equalized image and histogram
        equalized_image_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_BGR2RGB)
        self.show_histogram(equalized_image_rgb, 'Histogram Equalization', self.canvas_equalization)
        self.display_image_cv(equalized_image, self.equalized_image_label)

        # Convert to grayscale and display
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.show_histogram(grayscale_image, 'Histogram Grayscale', self.canvas_grayscale)
        self.display_image_cv(cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR), self.grayscale_image_label)

    # Show histogram for the image
    def show_histogram(self, image, title, canvas):
        canvas.figure.clear()
        ax = canvas.figure.add_subplot(111)
        if len(image.shape) == 3:  # Color image
            color = ('r', 'g', 'b')
            for i, col in enumerate(color):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                ax.plot(hist, color=col)
        else:  # Grayscale image
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            ax.plot(hist, color='k')
        ax.set_xlim([0, 256])
        ax.set_title(title)
        canvas.draw()

    # Display image using OpenCV format
    def display_image_cv(self, image, label):
        q_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
