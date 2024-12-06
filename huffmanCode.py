import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QWidget
)

# Huffman Node class
class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


# Build Huffman Tree
def build_huffman_tree(freq_dict):
    nodes = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)

        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        nodes.append(merged)

    return nodes[0]


# Generate Huffman codes
def generate_huffman_codes(node, code="", mapping=None):
    if mapping is None:
        mapping = {}

    if node is not None:
        if node.char is not None:
            mapping[node.char] = code
        generate_huffman_codes(node.left, code + "0", mapping)
        generate_huffman_codes(node.right, code + "1", mapping)

    return mapping


# Huffman Compression
def huffman_compress(text):
    freq_dict = {char: text.count(char) for char in set(text)}
    root = build_huffman_tree(freq_dict)
    codes = generate_huffman_codes(root)

    compressed_text = ''.join(codes[char] for char in text)
    return compressed_text, codes, freq_dict


# Huffman Code Window
class HuffmanCodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Huffman Code Generator")
        self.setGeometry(100, 100, 600, 500)

        # Main layout
        layout = QVBoxLayout()

        # Input label and text box
        self.input_label = QLabel("Enter Text to Compress:")
        layout.addWidget(self.input_label)

        self.input_text = QLineEdit(self)
        layout.addWidget(self.input_text)

        # Submit button
        self.submit_button = QPushButton("Generate Huffman Code")
        self.submit_button.clicked.connect(self.generate_huffman_code)
        layout.addWidget(self.submit_button)

        # Output labels and text boxes
        self.huffman_code_label = QLabel("Huffman Code and Character Mapping:")
        layout.addWidget(self.huffman_code_label)

        self.huffman_code_output = QTextEdit(self)
        self.huffman_code_output.setReadOnly(True)
        layout.addWidget(self.huffman_code_output)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def generate_huffman_code(self):
        text = self.input_text.text()

        if text.strip() == "":
            self.huffman_code_output.setText("Error: Please enter some text.")
            return

        compressed_text, codes, freq_dict = huffman_compress(text)

        # Prepare output: Huffman code and mapping
        output = f"Compressed Huffman Code:\n{compressed_text}\n\n"
        output += "Character to Huffman Code Mapping:\n"
        for char, code in codes.items():
            output += f"'{char}': {code}\n"

        # Display the Huffman code and mapping
        self.huffman_code_output.setText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HuffmanCodeWindow()
    window.show()
    sys.exit(app.exec_())
