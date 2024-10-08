import cv2
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class EdgeDetectionFeatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Edge Detection')
        self.setGeometry(0, 0, 800, 600)  # Adjusted window size
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        # Main layout for the edge detection feature
        layout = QVBoxLayout()

        # Title label
        #self.title_label = QLabel('Edge Detection', self)
        #self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; padding: 10px;")
        #self.title_label.setAlignment(Qt.AlignCenter)
        #layout.addWidget(self.title_label)

        # Upload button for edge detection image
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setFixedSize(150, 40)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        # Edge detection image label
        self.edge_image_label = QLabel('Edge Detection Image', self)
        self.edge_image_label.setAlignment(Qt.AlignCenter)
        self.edge_image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #ffffff;")
        self.edge_image_label.setFixedHeight(400)
        layout.addWidget(self.edge_image_label)

        # Set main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            self.detect_edges()

    def detect_edges(self):
        if self.image is None:
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        self.display_edge_image(edges)

    def display_edge_image(self, image):
        q_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.edge_image_label.setPixmap(pixmap.scaled(self.edge_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.edge_image_label.setAlignment(Qt.AlignCenter)
