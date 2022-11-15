import sys

from PIL import Image
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLabel
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    density = '@%#*+=-:. '

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image to ASCII')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(QSize(300, 200))
        self.canSave = False

        layout = QVBoxLayout()

        buttonLayout = QHBoxLayout()

        loadButton = QPushButton('Load Image')
        loadButton.setFixedSize(QSize(100, 25))
        loadButton.clicked.connect(self.loadImage)

        buttonLayout.addWidget(loadButton)
        buttonLayout.addStretch(1)

        self.displayImage = QLabel()
        self.displayImage.setFont(QFont('Courier', 10))
        self.displayImage.setStyleSheet('color: white')

        layout.addLayout(buttonLayout)
        layout.addWidget(self.displayImage)
        layout.addSpacing(1)
        
        widget = Color(QColor.fromRgb(12, 12, 12))
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def loadImage(self):
        src_file = QFileDialog.getOpenFileName(self, 'Open File','', 'Images (*.jpg)')[0]
        
        if src_file:
            src = Image.open(src_file)
            src = src.resize((round((src.width/src.height)*200),round((src.height/src.height)*200)))
            pixels = list(src.getdata())

            ascii_pixels = []

            for u in range(0, src.height, 5):
                for v in range(0, src.width, 2):
                    index = u*src.width + v
                    brightness = (pixels[index][0] + pixels[index][1] + pixels[index][2])/3.0
                    letter = self.density[round(10*(brightness/255)-1)]
                    ascii_pixels.append(letter)
                ascii_pixels.append('\n')

            output = open('ascii-image.txt', 'w')
            for character in ascii_pixels:
                output.write(character)
            output.close()
            
            display = open('ascii-image.txt', 'r')
            self.displayImage.setText(display.read())
            display.close()
            self.canSave = True

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()