import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QHBoxLayout, QGroupBox
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

class MorphologyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Atur judul dan ukuran jendela utama
        self.setWindowTitle('Morphology Operations')
        self.setGeometry(100, 100, 900, 500)

        # Mengatur warna latar belakang
        self.setStyleSheet("background-color: #DFF2EB;")

        # Tata letak utama untuk operasi morfologi
        main_layout = QVBoxLayout()

        # Label judul
        self.title_label = QLabel('Pilih Operasi Morfologi dan Unggah Gambar', self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333; padding: 5px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Combo box untuk memilih operasi morfologi
        self.morphology_combo = QComboBox(self)
        self.morphology_combo.addItem("Dilation")
        self.morphology_combo.addItem("Erosion")
        self.morphology_combo.addItem("Opening")
        self.morphology_combo.addItem("Closing")
        self.morphology_combo.setFixedWidth(180)
        self.morphology_combo.setStyleSheet("""
            QComboBox {
                background-color: #B9E5E8;
                color: black;
                font-size: 14px;
                padding: 5px;
                border: 1px solid #B59F78;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.morphology_combo, alignment=Qt.AlignCenter)

        # Tombol untuk mengunggah gambar
        self.upload_button = QPushButton('Unggah Gambar', self)
        self.upload_button.clicked.connect(self.upload_image)
        self.upload_button.setFixedWidth(180)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #B9E5E8;
                color: black;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #B59F78;
            }
        """)
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

        # Tombol untuk menerapkan operasi yang dipilih
        self.apply_button = QPushButton('Terapkan Operasi', self)
        self.apply_button.clicked.connect(self.apply_morphology)
        self.apply_button.setEnabled(False)
        self.apply_button.setFixedWidth(180)
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #B9E5E8;
                color: black;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #B59F78;
            }
        """)
        main_layout.addWidget(self.apply_button, alignment=Qt.AlignCenter)

        # Tata letak untuk menampilkan gambar asli dan gambar yang telah diproses
        self.image_layout = QHBoxLayout()

        # Group box untuk gambar asli
        self.original_group = QGroupBox("Gambar Asli")
        original_layout = QVBoxLayout()
        self.original_image_label = QLabel(self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setFixedSize(400, 300)
        original_layout.addWidget(self.original_image_label)
        self.original_group.setLayout(original_layout)
        self.image_layout.addWidget(self.original_group)

        # Group box untuk gambar yang diproses
        self.processed_group = QGroupBox("Gambar yang Diproses")
        processed_layout = QVBoxLayout()
        self.processed_image_label = QLabel(self)
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.setFixedSize(400, 300)
        processed_layout.addWidget(self.processed_image_label)
        self.processed_group.setLayout(processed_layout)
        self.image_layout.addWidget(self.processed_group)

        # Tambahkan tata letak gambar ke tata letak utama
        main_layout.addLayout(self.image_layout)

        # Setel tata letak utama sebagai tata letak pusat jendela
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.img = None  # Placeholder untuk gambar yang diunggah

    def upload_image(self):
        # Buka dialog file untuk memilih gambar
        file_name, _ = QFileDialog.getOpenFileName(self, 'Buka File Gambar', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_name:
            # Baca dan tampilkan gambar
            self.img = cv2.imread(file_name)
            self.display_image(self.img, self.original_image_label)
            self.apply_button.setEnabled(True)  # Aktifkan tombol "Terapkan Operasi"

    def apply_morphology(self):
        if self.img is None:
            return

        # Kernel untuk operasi morfologi (ukuran 5x5)
        kernel = np.ones((5, 5), np.uint8)

        # Dapatkan operasi morfologi yang dipilih dari combo box
        selected_operation = self.morphology_combo.currentText()

        # Terapkan operasi morfologi yang dipilih
        if selected_operation == "Dilation":
            result = self.apply_dilation(self.img, kernel)
        elif selected_operation == "Erosion":
            result = self.apply_erosion(self.img, kernel)
        elif selected_operation == "Opening":
            result = self.apply_opening(self.img, kernel)
        elif selected_operation == "Closing":
            result = self.apply_closing(self.img, kernel)

        # Tampilkan gambar yang telah diproses
        self.display_image(result, self.processed_image_label)

    def apply_dilation(self, img, kernel):
        # Terapkan operasi dilasi
        dilated_img = cv2.dilate(img, kernel, iterations=1)
        return dilated_img

    def apply_erosion(self, img, kernel):
        # Terapkan operasi erosi
        eroded_img = cv2.erode(img, kernel, iterations=1)
        return eroded_img

    def apply_opening(self, img, kernel):
        # Terapkan operasi opening (erosi diikuti oleh dilasi)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening

    def apply_closing(self, img, kernel):
        # Terapkan operasi closing (dilasi diikuti oleh erosi)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return closing

    def display_image(self, img, label):
        # Konversi gambar dari BGR (format OpenCV) ke RGB (format QImage)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Konversi QImage menjadi QPixmap dan tampilkan pada label
        pixmap = QPixmap.fromImage(q_img)

        # Sesuaikan agar tidak pecah, dengan menetapkan skala pixmap pada resolusi yang tepat
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    morphology_window = MorphologyApp()
    morphology_window.show()
    sys.exit(app.exec_())
