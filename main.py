import sys
from PyQt5.QtCore import Qt  # type: ignore
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QLabel, QComboBox, QApplication  # type: ignore
from edgeDetection import EdgeDetectionFeatureWindow
from histogram import HistogramFeatureWindow
from faceRecognition import FaceDetectionFeatureWindow
from imageCropper import ImageCropperWindow
from imageSegmentation import ColorSegmentationApp
from histogramMatching import HistogramMatchingApp
from restoration import RestorationApp
from morphology import MorphologyApp
from noiseCleaning import NoiseCleaningApp
from chainCode import ChainCodeWindow
from huffmanCode import HuffmanCodeWindow
from emotionRecognition import EmotionRecognitionWindow

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting the title and initial window geometry
        self.setWindowTitle('Main Menu')
        self.setGeometry(0, 0, 500, 400)  # Adjust window size as needed

        # Center the window on the screen
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        # Main layout for the menu
        layout = QVBoxLayout()

        # Styling the window using a stylesheet for a more modern and colorful UI
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-family: Arial, sans-serif;
                color: #333333;
            }
            QComboBox {
                font-size: 16px;
                font-family: Arial, sans-serif;
                padding: 5px;
                margin: 10px 0;
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 8px;
            }
            QComboBox:hover {
                border-color: #66b3ff;
            }
        """)

        # Title label with styling
        self.title_label = QLabel('Select a Feature', self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2a2a2a; padding: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Combo box with styling for feature selection
        self.feature_combo = QComboBox(self)
        self.feature_combo.addItem("Histogram Equalization")
        self.feature_combo.addItem("Face & Blur Detection")
        self.feature_combo.addItem("Edge Detection")
        self.feature_combo.addItem("Image Segmentation")
        self.feature_combo.addItem("Histogram Matching")
        self.feature_combo.addItem("Image Cropper")
        self.feature_combo.addItem("Image Restoration")
        self.feature_combo.addItem("Morphology") 
        self.feature_combo.addItem("Salt & Paper Cleaning")
        self.feature_combo.addItem("Chain Code")
        self.feature_combo.addItem("Huffman Code")
        self.feature_combo.addItem("Facial Emotion Recognition")
        self.feature_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                background-color: #ffffff;
                border: 1px solid #bfbfbf;
                border-radius: 5px;
                padding: 8px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #bbbbbb;
            }
        """)
        self.feature_combo.activated[str].connect(self.open_feature)
        layout.addWidget(self.feature_combo, alignment=Qt.AlignCenter)

        # Set main layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Adjust spacing and padding for a more appealing layout
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

    def open_feature(self, feature_name):
        if feature_name == "Histogram Equalization":
            self.histogram_window = HistogramFeatureWindow()
            self.histogram_window.show()
        elif feature_name == "Face & Blur Detection":
            self.face_detection_window = FaceDetectionFeatureWindow()
            self.face_detection_window.show()
        elif feature_name == "Edge Detection":
            self.edge_detection_window = EdgeDetectionFeatureWindow()
            self.edge_detection_window.show()
        elif feature_name == "Image Segmentation":
            self.segmentation_window = ColorSegmentationApp()
            self.segmentation_window.show()
        elif feature_name == "Histogram Matching":
            self.histogram_matching_window = HistogramMatchingApp()
            self.histogram_matching_window.show()
        elif feature_name == "Image Cropper":
            self.cropper_window = ImageCropperWindow()
            self.cropper_window.show()
        elif feature_name == "Image Restoration":
            self.restoration_window = RestorationApp()
            self.restoration_window.show()
        elif feature_name == "Morphology": 
            self.morphology_window = MorphologyApp()
            self.morphology_window.show()
        elif feature_name == "Salt & Paper Cleaning": 
            self.morphology_window = NoiseCleaningApp()
            self.morphology_window.show()
        elif feature_name == "Chain Code": 
            self.chain_code_window = ChainCodeWindow()
            self.chain_code_window.show()
        elif feature_name == "Huffman Code": 
            self.huffman_code_window = HuffmanCodeWindow()
            self.huffman_code_window.show()
        elif feature_name == "Facial Emotion Recognition":  
            self.emotion_recognition_window = EmotionRecognitionWindow()
            self.emotion_recognition_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainMenuWindow()
    main_window.show()
    sys.exit(app.exec_())
