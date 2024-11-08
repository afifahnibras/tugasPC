from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

class ScalingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Scaling with Interpolation')
        self.setGeometry(100, 100, 800, 600)

        # Mengatur warna latar belakang
        self.setStyleSheet("background-color: #DFF2EB;")
        
        # Layout utama dengan area scroll
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Widget untuk menyimpan konten sebenarnya
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Layout untuk gambar sebelum dan sesudah scaling
        before_layout = QHBoxLayout()
        after_layout = QHBoxLayout()
        
        # Label untuk menampilkan gambar "Before" (sebelum scaling) dan "After" (setelah scaling)
        self.before_label = QLabel(self)
        self.before_label.setAlignment(Qt.AlignCenter)
        self.after_label = QLabel(self)
        self.after_label.setAlignment(Qt.AlignCenter)

        # Label teks untuk "Before" dan "After"
        self.before_text = QLabel("Before", self)
        self.before_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.after_text = QLabel("After", self)
        self.after_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Tambahkan gambar dan label teks ke layout masing-masing
        before_layout.addWidget(self.before_text)
        before_layout.addWidget(self.before_label)
        after_layout.addWidget(self.after_text)
        after_layout.addWidget(self.after_label)

        # Tambahkan layout "Before" dan "After" ke layout utama
        layout.addLayout(before_layout)
        layout.addLayout(after_layout)

        # Layout horizontal untuk tombol "Upload Image" dan ComboBox "Interpolation selection"
        top_layout = QHBoxLayout()
        
        # Tombol upload (di sebelah kiri)
        upload_btn = QPushButton("Upload Image")
        upload_btn.setFixedWidth(180)
        upload_btn.clicked.connect(self.upload_image)
        upload_btn.setStyleSheet("""
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
        top_layout.addWidget(upload_btn)

        # ComboBox untuk memilih metode interpolasi (di sebelah kanan)
        self.interpolation_combo = QComboBox(self)
        self.interpolation_combo.addItem("Nearest Neighbor")
        self.interpolation_combo.addItem("Bilinear")
        self.interpolation_combo.addItem("Cubic")
        self.interpolation_combo.setFixedWidth(180)
        self.interpolation_combo.setStyleSheet("""
            QComboBox {
                background-color: #B9E5E8;
                color: black;
                font-size: 14px;
                padding: 5px;
                border: 1px solid #B59F78;
                border-radius: 5px;
            }
        """)
        top_layout.addWidget(self.interpolation_combo)

        # Tambahkan layout ini ke layout utama
        layout.addLayout(top_layout)

        # Layout horizontal untuk tombol "Apply Scaling" dan ComboBox "Scale method selection"
        bottom_layout = QHBoxLayout()

        # Tombol apply (di bawah "Upload Image")
        apply_btn = QPushButton("Apply Scaling")
        apply_btn.setFixedWidth(180)
        apply_btn.clicked.connect(self.apply_scaling)
        apply_btn.setStyleSheet("""
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
        bottom_layout.addWidget(apply_btn)

        # ComboBox untuk memilih metode scaling (di bawah "Interpolation selection")
        self.scale_method_combo = QComboBox(self)
        self.scale_method_combo.addItem("Upscale")
        self.scale_method_combo.addItem("Downscale")
        self.scale_method_combo.setFixedWidth(180)
        self.scale_method_combo.setStyleSheet("""
            QComboBox {
                background-color: #B9E5E8;
                color: black;
                font-size: 14px;
                padding: 5px;
                border: 1px solid #B59F78;
                border-radius: 5px;
            }
        """)
        bottom_layout.addWidget(self.scale_method_combo)

        # Tambahkan layout ini ke layout utama
        layout.addLayout(bottom_layout)

        # Atur widget konten ke dalam area scroll
        scroll_area.setWidget(content_widget)
        
        # Tambahkan area scroll ke layout utama
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        self.image = None  # Inisialisasi variabel gambar

    def upload_image(self):
        # Buka dialog file untuk memilih gambar
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            # Baca gambar yang dipilih menggunakan OpenCV
            self.image = cv2.imread(file_path)
            self.show_image(self.image, self.before_label, scale=True)  # Tampilkan gambar asli dalam skala agar sesuai

    def apply_scaling(self):
        if self.image is not None:
            # Tentukan metode interpolasi dari pilihan ComboBox
            interpolation_method = self.interpolation_combo.currentText()
            if interpolation_method == "Nearest Neighbor":
                interpolation = cv2.INTER_NEAREST
            elif interpolation_method == "Bilinear":
                interpolation = cv2.INTER_LINEAR
            elif interpolation_method == "Cubic":
                interpolation = cv2.INTER_CUBIC

            # Mendapatkan metode scaling (Upscale atau Downscale)
            scale_method = self.scale_method_combo.currentText()
            scale_factor = 3 if scale_method == "Upscale" else 0.3  # Menentukan faktor scaling

            # Resize gambar sesuai faktor skala dan metode interpolasi yang dipilih
            scaled_image = cv2.resize(self.image, None, fx=scale_factor, fy=scale_factor, interpolation=interpolation)
            
            # Tampilkan gambar yang telah di-scaling
            self.show_image(scaled_image, self.after_label, scale=False)  # Tampilkan gambar yang telah di-scaling dalam ukuran sebenarnya

    def show_image(self, img, label, scale=True):
        # Konversi gambar dari BGR (format OpenCV) ke RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Konversi ke QImage
        height, width, channel = img_rgb.shape
        bytes_per_line = 3 * width
        qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        
        # Set QPixmap ke QLabel
        if scale:
            # Skala gambar agar sesuai dengan label
            label.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio))
        else:
            # Tampilkan gambar dalam ukuran sebenarnya
            label.setPixmap(pixmap)
