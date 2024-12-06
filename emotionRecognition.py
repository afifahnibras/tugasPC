import cv2
from deepface import DeepFace
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

class EmotionRecognitionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facial Emotion Recognition")
        self.setGeometry(100, 100, 600, 600)  # Ukuran jendela aplikasi

        # Layout utama
        self.layout = QVBoxLayout()

        # Label untuk menampilkan gambar
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Tombol untuk memilih gambar
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.upload_button)

        # Tombol untuk mendeteksi emosi
        self.detect_button = QPushButton("Detect Emotion")
        self.detect_button.clicked.connect(self.detect_emotion)
        self.layout.addWidget(self.detect_button)

        # Widget pusat
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Variabel untuk menyimpan path gambar
        self.image_path = None

    def load_image(self):
        # Dialog untuk memilih gambar
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            self.image_path = file_path
            # Tampilkan gambar di label dengan resolusi terjaga
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.width() - 50, self.height() - 150, Qt.KeepAspectRatio))

    def detect_emotion(self):
        if not self.image_path:
            self.image_label.setText("No image loaded!")
            return

        # Membaca gambar dengan OpenCV
        image = cv2.imread(self.image_path)
        original_image = image.copy()  # Salin gambar asli untuk menampilkan output

        # Terapkan peningkatan kontras gambar menggunakan CLAHE
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(gray_image)

        # Konversi kembali ke RGB untuk DeepFace
        rgb_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2RGB)

        # Deteksi wajah
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(enhanced_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = rgb_image[y:y + h, x:x + w]

            try:
                # Analisis emosi menggunakan DeepFace
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']

                # Gambar kotak hijau di sekitar wajah
                cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Tambahkan teks emosi di atas kotak
                cv2.putText(
                    original_image, 
                    dominant_emotion, 
                    (x + 5, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, 
                    (0, 255, 0), 
                    2, 
                    cv2.LINE_AA
                )
            except Exception as e:
                print(f"Error: {e}")

        # Tampilkan hasil gambar di PyQt
        result_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        height, width, channel = result_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(result_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        self.image_label.setPixmap(pixmap.scaled(self.width() - 50, self.height() - 150, Qt.KeepAspectRatio))
