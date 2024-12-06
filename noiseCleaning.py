import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QWidget, QPushButton, QFileDialog, QApplication,
    QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QDesktopWidget
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class NoiseCleaningApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Noise Cleaning Methods')
        self.setGeometry(100, 100, 800, 600)

         # Center the window on the screen
        cwa = self.frameGeometry()
        cwc = QDesktopWidget().availableGeometry().center()
        cwa.moveCenter(cwc)
        self.move(cwa.topLeft())

        # Layout utama dengan scroll area
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Layout atas untuk gambar original dan noise
        top_layout = QHBoxLayout()

        # Layout bawah untuk grid 2x2 hasil filtering
        filter_layout = QGridLayout()
        filter_layout.setSpacing(20)  # Tambahkan jarak antar elemen di grid

        # Inisialisasi dictionary untuk label gambar dan teks
        self.labels = {}
        titles = ['Original', 'Salt-Pepper Noise', 'Low-pass Filter', 'Median Filter', 'Rank-order Filter', 'Outlier Method']

        # Buat QLabel untuk setiap gambar dan teks di atasnya
        for i, title in enumerate(titles):
            # Label teks (judul)
            text_label = QLabel(title, self)
            text_label.setAlignment(Qt.AlignCenter)

            # Label gambar
            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setFixedSize(400, 400)

            # Masukkan ke dalam layout vertikal
            vbox = QVBoxLayout()
            vbox.addWidget(text_label)  # Tambahkan judul di atas gambar
            vbox.addWidget(img_label)   # Tambahkan gambar

            # Tambahkan spacer untuk jarak vertikal antar gambar
            vbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Simpan label gambar dalam dictionary untuk akses mudah
            self.labels[title] = img_label

            # Masukkan ke layout yang sesuai
            if i < 2:
                top_layout.addLayout(vbox)  # Untuk gambar original dan noise
            else:
                row, col = divmod(i - 2, 2)
                filter_layout.addLayout(vbox, row, col)  # Untuk hasil filtering

        # Tombol untuk memuat dan memproses gambar
        button_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)

        self.process_button = QPushButton('Apply Filter', self)
        self.process_button.clicked.connect(self.apply_filters)
        button_layout.addWidget(self.process_button)

        # Gabungkan semua layout dalam scroll area
        scroll_layout.addLayout(top_layout)
        scroll_layout.addLayout(filter_layout)
        scroll_layout.addLayout(button_layout)
        scroll_area.setWidget(scroll_content)

        # Set scroll area sebagai central widget
        self.setCentralWidget(scroll_area)

        self.image = None

    def load_image(self):
        """Memuat gambar dari file."""
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if image_path:
            self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            self.display_image(self.image, self.labels['Original'])

    def display_image(self, img, label):
        """Menampilkan gambar pada QLabel."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_img).scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def apply_filters(self):
        """Menerapkan noise dan berbagai metode filtering."""
        if self.image is None:
            return

        # Step 1: Tambahkan Salt-and-Pepper Noise
        noisy_image = self.add_salt_and_pepper_noise(self.image)
        self.display_image(noisy_image, self.labels['Salt-Pepper Noise'])

        # Step 2: Low-pass filtering (Gaussian Blur)
        low_pass = cv2.GaussianBlur(noisy_image, (5, 5), 0)
        self.display_image(low_pass, self.labels['Low-pass Filter'])

        # Step 3: Median filtering
        median_filtered = cv2.medianBlur(noisy_image, 5)
        self.display_image(median_filtered, self.labels['Median Filter'])

        # Step 4: Rank-order filtering (menggunakan median)
        rank_order = cv2.medianBlur(noisy_image, 5)  # Rank-order sederhana dengan median
        self.display_image(rank_order, self.labels['Rank-order Filter'])

        # Step 5: Outlier method (Threshold-based noise removal)
        outlier_filtered = self.outlier_method(noisy_image)
        self.display_image(outlier_filtered, self.labels['Outlier Method'])

    def add_salt_and_pepper_noise(self, image, salt_prob=0.02, pepper_prob=0.02):
        """Menambahkan salt-and-pepper noise pada gambar."""
        noisy_image = np.copy(image)
        total_pixels = image.size

        # Salt noise
        num_salt = np.ceil(salt_prob * total_pixels)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]]
        noisy_image[tuple(coords)] = 255

        # Pepper noise
        num_pepper = np.ceil(pepper_prob * total_pixels)
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]]
        noisy_image[tuple(coords)] = 0

        return noisy_image

    def outlier_method(self, image):
        """Menggunakan median sebagai deteksi outlier sederhana."""
        median = cv2.medianBlur(image, 5)
        diff = cv2.absdiff(image, median)
        _, threshold = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        return cv2.bitwise_and(image, median)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NoiseCleaningApp()
    window.show()
    sys.exit(app.exec_())
