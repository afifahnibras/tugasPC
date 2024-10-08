import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QWidget, QPushButton, QFileDialog, QApplication, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class RestorationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Perbesar ukuran jendela
        self.setWindowTitle('Image Restoration')
        self.setGeometry(100, 100, 1200, 800)  # Lebih besar: 1200x800
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        layout = QGridLayout()

        # Label untuk menampilkan gambar asli
        self.original_image_label = QLabel('Original Image', self)
        self.original_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.original_image_label, 0, 0)

        # Perbesar label gambar untuk menampilkan gambar asli
        self.original_image_display = QLabel(self)
        self.original_image_display.setFixedSize(400, 400)  # Ukuran label diperbesar
        layout.addWidget(self.original_image_display, 1, 0)

        # Label untuk menampilkan gambar yang telah di-denoise
        self.denoised_image_label = QLabel('Denoised Image', self)
        self.denoised_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.denoised_image_label, 0, 1)

        # Perbesar label gambar untuk menampilkan gambar yang telah di-denoise
        self.denoised_image_display = QLabel(self)
        self.denoised_image_display.setFixedSize(400, 400)  # Ukuran label diperbesar
        layout.addWidget(self.denoised_image_display, 1, 1)

        # Label untuk menampilkan gambar yang telah direstorasi
        self.restored_image_label = QLabel('Restored Image', self)
        self.restored_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.restored_image_label, 0, 2)

        # Perbesar label gambar untuk menampilkan gambar yang telah direstorasi
        self.restored_image_display = QLabel(self)
        self.restored_image_display.setFixedSize(400, 400)  # Ukuran label diperbesar
        layout.addWidget(self.restored_image_display, 1, 2)

        # Tombol untuk memuat gambar
        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button, 2, 0)

        # Tombol untuk merestorasi gambar
        self.restore_button = QPushButton('Restore Image', self)
        self.restore_button.clicked.connect(self.restore_image)
        layout.addWidget(self.restore_button, 2, 1)

        # Atur layout ke central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def load_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if image_path:
            # Memuat gambar menggunakan OpenCV
            self.image = cv2.imread(image_path)
            self.display_image(self.image, self.original_image_display)

    def display_image(self, img, label):
        # Mengonversi BGR ke RGB
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_image).scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def restore_image(self):
        # Restorasi gambar dengan denoising dan ekualisasi histogram
        if self.image is not None:
            # Denoising menggunakan Bilateral Filter dengan pengurangan blur
            # Sesuaikan parameter d, sigmaColor, sigmaSpace
            denoised_image = cv2.bilateralFilter(self.image, d=10, sigmaColor=20, sigmaSpace=30)

            # Mengonversi BGR ke ruang warna YCrCb
            ycrcb_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2YCrCb)

            # Menerapkan ekualisasi histogram pada channel Y (luminance)
            y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)
            equalized_y_channel = cv2.equalizeHist(y_channel)
            equalized_image = cv2.merge([equalized_y_channel, cr_channel, cb_channel])

            # Langkah 4: Mengonversi kembali ke ruang warna BGR
            restored_image_bgr = cv2.cvtColor(equalized_image, cv2.COLOR_YCrCb2BGR)

            # Menampilkan gambar-gambar
            self.display_image(self.image, self.original_image_display)          # Gambar asli
            self.display_image(denoised_image, self.denoised_image_display)     # Gambar yang di-denoise
            self.display_image(restored_image_bgr, self.restored_image_display) # Gambar yang direstorasi

            # Opsional: Menyimpan gambar yang telah diproses
            # cv2.imwrite("restored_image.png", restored_image_bgr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestorationApp()
    window.show()
    sys.exit(app.exec_())
