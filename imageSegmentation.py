import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QApplication, QComboBox, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ColorSegmentationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Color-Based Object Segmentation')
        self.setGeometry(100, 100, 800, 600)

        layout = QGridLayout()

        # Original image display label
        self.original_image_label = QLabel('Original Image', self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.original_image_label, 0, 0)

        self.original_image_display = QLabel(self)
        layout.addWidget(self.original_image_display, 1, 0)

        # Segmented overlay image display label
        self.overlay_image_label = QLabel('Segmented Overlay', self)
        self.overlay_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.overlay_image_label, 0, 1)

        self.overlay_image_display = QLabel(self)
        layout.addWidget(self.overlay_image_display, 1, 1)

        # Result image display label
        self.result_image_label = QLabel('Result Image', self)
        self.result_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_image_label, 0, 2)

        self.result_image_display = QLabel(self)
        layout.addWidget(self.result_image_display, 1, 2)

        # Button to load image
        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button, 2, 0)

        # Color selection combo box
        self.color_combo = QComboBox(self)
        self.color_combo.addItem("Select a Color")
        self.color_combo.addItem("Red")
        self.color_combo.addItem("Green")
        self.color_combo.addItem("Blue")
        self.color_combo.addItem("Yellow")
        self.color_combo.addItem("Black")
        self.color_combo.currentIndexChanged.connect(self.segment_color)
        layout.addWidget(self.color_combo, 2, 1)

        # Set layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def load_image(self):
        """Load image from file."""
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if image_path:
            # Load the image using OpenCV
            self.image = cv2.imread(image_path)
            self.display_image(self.image, self.original_image_display)

    def display_image(self, img, label):
        """Helper function to display image in QLabel."""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_image).scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def segment_color(self):
        """Segment the image based on the selected color."""
        if self.image is None:
            self.original_image_display.setText("Please load an image first.")
            return

        selected_color = self.color_combo.currentText()

        # Convert the image to the HSV color space
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # Define color ranges for segmentation in HSV
        if selected_color == "Red":
            lower_bound1 = np.array([0, 120, 70])
            upper_bound1 = np.array([10, 255, 255])
            lower_bound2 = np.array([170, 120, 70])
            upper_bound2 = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv_image, lower_bound1, upper_bound1)
            mask2 = cv2.inRange(hsv_image, lower_bound2, upper_bound2)
            mask = mask1 + mask2

        elif selected_color == "Green":
            lower_bound = np.array([36, 50, 70])
            upper_bound = np.array([89, 255, 255])
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        elif selected_color == "Blue":
            lower_bound = np.array([94, 80, 2])
            upper_bound = np.array([126, 255, 255])
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        elif selected_color == "Yellow":
            lower_bound = np.array([20, 100, 100])
            upper_bound = np.array([30, 255, 255])
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        elif selected_color == "Black":
            lower_bound = np.array([0, 0, 0])
            upper_bound = np.array([180, 255, 30])
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        else:
            self.original_image_display.setText("Please select a valid color.")
            return

        # Apply the mask to the image to extract the color
        result_image = cv2.bitwise_and(self.image, self.image, mask=mask)

        # Create an overlay image
        overlay_image = self.image.copy()
        overlay_image[mask > 0] = [0, 255, 0]  # Change color of detected areas (to green)

        # Display the images
        self.display_image(self.image, self.original_image_display)       # Original image
        self.display_image(overlay_image, self.overlay_image_display)    # Segmented overlay
        self.display_image(result_image, self.result_image_display)      # Result image


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorSegmentationApp()
    window.show()
    sys.exit(app.exec_())
