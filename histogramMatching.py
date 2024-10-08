import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QGridLayout) # type: ignore
from PyQt5.QtGui import QPixmap, QImage # type: ignore
from PyQt5.QtCore import Qt # type: ignore
import matplotlib.pyplot as plt

class HistogramMatchingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogram Matching Application")
        self.setGeometry(100, 100, 1000, 800)

        # Membuat elemen-elemen UI
        self.target_image_label = QLabel(self)  # Label untuk menampilkan gambar target
        self.reference_image_label = QLabel(self)  # Label untuk menampilkan gambar referensi
        self.result_image_label = QLabel(self)  # Label untuk menampilkan hasil matching
        self.target_histogram_label = QLabel(self)  # Label untuk menampilkan histogram gambar target
        self.reference_histogram_label = QLabel(self)  # Label untuk menampilkan histogram gambar referensi
        self.result_histogram_label = QLabel(self)  # Label untuk menampilkan histogram gambar hasil

        # Tombol untuk mengunggah gambar dan menerapkan histogram matching
        self.load_target_image_button = QPushButton("Load Target Image", self)
        self.load_reference_image_button = QPushButton("Load Reference Image", self)
        self.apply_histogram_matching_button = QPushButton("Apply Histogram Matching", self)

        # Mengatur tata letak (layout)
        layout = QVBoxLayout()
        
        # Grid layout untuk menampilkan gambar dan histogram
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Target Image"), 0, 0)
        grid_layout.addWidget(QLabel("Reference Image"), 0, 1)
        grid_layout.addWidget(QLabel("Result Image"), 0, 2)
        
        grid_layout.addWidget(self.target_image_label, 1, 0)
        grid_layout.addWidget(self.reference_image_label, 1, 1)
        grid_layout.addWidget(self.result_image_label, 1, 2)

        grid_layout.addWidget(QLabel("Target Histogram"), 2, 0)
        grid_layout.addWidget(QLabel("Reference Histogram"), 2, 1)
        grid_layout.addWidget(QLabel("Result Histogram"), 2, 2)
        
        grid_layout.addWidget(self.target_histogram_label, 3, 0)
        grid_layout.addWidget(self.reference_histogram_label, 3, 1)
        grid_layout.addWidget(self.result_histogram_label, 3, 2)

        # Layout untuk tombol-tombol
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_target_image_button)
        button_layout.addWidget(self.load_reference_image_button)
        button_layout.addWidget(self.apply_histogram_matching_button)
        
        layout.addLayout(grid_layout)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Menghubungkan tombol dengan fungsinya
        self.load_target_image_button.clicked.connect(self.load_target_image)
        self.load_reference_image_button.clicked.connect(self.load_reference_image)
        self.apply_histogram_matching_button.clicked.connect(self.apply_histogram_matching)

        self.target_image = None  # Variabel untuk menyimpan gambar target
        self.reference_image = None  # Variabel untuk menyimpan gambar referensi

    def load_target_image(self):
        """ Fungsi untuk memuat gambar target """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Target Image", "", "Images (*.png *.xpm *.jpg *.jpeg)", options=options)
        if file_name:
            self.target_image = cv2.imread(file_name)
            self.display_image(self.target_image, self.target_image_label)
            self.display_histogram(self.target_image, self.target_histogram_label)

    def load_reference_image(self):
        """ Fungsi untuk memuat gambar referensi """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Reference Image", "", "Images (*.png *.xpm *.jpg *.jpeg)", options=options)
        if file_name:
            self.reference_image = cv2.imread(file_name)
            self.display_image(self.reference_image, self.reference_image_label)
            self.display_histogram(self.reference_image, self.reference_histogram_label)

    def apply_histogram_matching(self):
        """ Fungsi untuk menerapkan histogram matching """
        if self.target_image is not None and self.reference_image is not None:
            result = self.histogram_matching(self.target_image, self.reference_image)
            self.display_image(result, self.result_image_label)
            self.display_histogram(result, self.result_histogram_label)

    def histogram_matching(self, source, reference):
        """
        Menyesuaikan nilai piksel gambar sumber agar sesuai dengan histogram gambar referensi.
        """
        # Mengubah gambar ke ruang warna LAB
        source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
        reference_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB)

        # Memisahkan channel L, A, B
        source_l, source_a, source_b = cv2.split(source_lab)
        reference_l, reference_a, reference_b = cv2.split(reference_lab)

        # Menerapkan histogram matching pada channel L (kecerahan)
        matched_l = self.match_histograms(source_l, reference_l)

        # Menggabungkan channel L yang telah dimodifikasi dengan channel A dan B asli
        matched_lab = cv2.merge([matched_l, source_a, source_b])

        # Mengubah kembali ke ruang warna BGR
        matched_bgr = cv2.cvtColor(matched_lab, cv2.COLOR_LAB2BGR)

        return matched_bgr

    def match_histograms(self, source_channel, reference_channel):
        """
        Melakukan histogram matching untuk satu channel (grayscale).
        """
        # Menghitung histogram dari kedua gambar
        source_hist, bins = np.histogram(source_channel.flatten(), 256, [0, 256])
        reference_hist, _ = np.histogram(reference_channel.flatten(), 256, [0, 256])

        # Menghitung cumulative distribution function (CDF)
        source_cdf = source_hist.cumsum()
        reference_cdf = reference_hist.cumsum()

        # Normalisasi CDF
        source_cdf_normalized = source_cdf * (255.0 / source_cdf[-1])
        reference_cdf_normalized = reference_cdf * (255.0 / reference_cdf[-1])

        # Membuat lookup table untuk memetakan nilai piksel
        lookup_table = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            lookup_table[i] = np.searchsorted(reference_cdf_normalized, source_cdf_normalized[i])

        # Menerapkan lookup table untuk mentransformasi gambar sumber
        matched_channel = cv2.LUT(source_channel, lookup_table)

        return matched_channel

    def display_image(self, img, label):
        """ Fungsi untuk menampilkan gambar pada label """
        if img is not None:
            q_image = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_BGR888)
            label.setPixmap(QPixmap.fromImage(q_image).scaled(300, 300, Qt.KeepAspectRatio))

    def display_histogram(self, img, label):
        """ Fungsi untuk menampilkan histogram pada label """
        if img is not None:
            color = ('b', 'g', 'r')
            plt.figure(figsize=(4, 3))
            for i, col in enumerate(color):
                hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                plt.plot(hist, color=col)
                plt.xlim([0, 256])
            plt.title("Histogram")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")
            plt.savefig("histogram.png")
            plt.close()

            # Menampilkan gambar histogram pada label
            histogram_img = QImage("histogram.png")
            label.setPixmap(QPixmap.fromImage(histogram_img).scaled(300, 150, Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv) # type: ignore
    window = HistogramMatchingApp()
    window.show()
    sys.exit(app.exec_())
