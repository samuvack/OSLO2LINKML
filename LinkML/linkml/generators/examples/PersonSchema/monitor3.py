import os
import time
import yaml
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea, QWidget
from PyQt5.QtGui import QPixmap, QImageReader, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette, QColor
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QImageReader, QPainter, QPen, QColor, QTextCursor
from PyQt5.QtCore import Qt, QRect, QObject, pyqtSignal
from contextlib import contextmanager
import subprocess
import sys
import requests

class OverviewWidget(QWidget):
    def __init__(self, originalPixmap, parent=None):
        super().__init__(parent)
        # Stel de achtergrondkleur in
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('white'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.originalPixmap = originalPixmap
        self.viewRect = QRect()
        self.zoomFactor = 1.0  # Voeg zoomFactor toe
        self.updateSize()


        # Stel de stijl in op de layout
        self.setStyleSheet("background-color: white; border: 1px solid gray;")
        
    def updateSize(self):
        aspectRatio = self.originalPixmap.width() / self.originalPixmap.height()
        newWidth = int(200 * aspectRatio)
        self.setFixedSize(newWidth, 200)


    def setViewRect(self, rect, zoomFactor):
        self.viewRect = rect
        self.zoomFactor = zoomFactor  # Update de zoomFactor
        self.update()

    def paintEvent(self, event):
        if not self.originalPixmap.isNull():
            painter = QPainter(self)
            scaledPixmap = self.originalPixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(self.rect(), scaledPixmap)

            #if not self.viewRect.isNull():
            # Pas de berekening aan om rekening te houden met de zoomFactor
            scaledRect = QRect(
                int(self.viewRect.x() * self.width() / (self.originalPixmap.width() * self.zoomFactor)),
                int(self.viewRect.y() * self.height() / (self.originalPixmap.height() * self.zoomFactor)),
                int(self.viewRect.width() * self.width() / (self.originalPixmap.width() * self.zoomFactor)),
                int(self.viewRect.height() * self.height() / (self.originalPixmap.height() * self.zoomFactor))
            )
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawRect(scaledRect)


class CustomScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        # Overschrijf de standaard wheelEvent om te voorkomen dat de QScrollArea scrollt
        pass

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.scrollArea = CustomScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.setCentralWidget(self.scrollArea)
        self.connectScrollBars()
        self.setWindowTitle("OSLO UML viewer (LinkML)")
        self.setGeometry(100, 100, 800, 600)

        # Maak een wit vlak aan
        self.whiteOverlay = QLabel(self)
        self.whiteOverlay.setStyleSheet("background-color: white;")
        self.whiteOverlay.lower()  # Zorg ervoor dat het onder de overviewWidget ligt

        # Maak een QTextEdit widget voor de console
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.console.setFixedHeight(20)
        self.console.setFixedWidth(10000)  # Breedte gelijk aan vensterbreedte
        self.console.move(0, self.height() - 100) # Breedte gelijk aan vensterbreedte
    

        # Redirect stdout naar de console
        sys.stdout = Stream(newText=self.onUpdateText)

        # Variabelen voor muis tracking
        self.dragging = False
        self.lastMousePosition = None

        self.zoomFactor = 1.0
        self.originalPixmap = None
        self.imageLabel = None
        self.overviewWidget = None

        # Load image
        self.loadImage("test.svg")  # Replace with your image path

    
    def onUpdateText(self, text):
        self.console.moveCursor(QTextCursor.End)
        self.console.insertPlainText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overviewWidget:
            self.positionOverviewWidget()
            self.whiteOverlay.setGeometry(self.overviewWidget.geometry())

 

    
    def loadImage(self, imagePath):
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(False)  # Zet setScaledContents op False
        self.scrollArea.setWidget(self.imageLabel)

        imageReader = QImageReader(imagePath)
        image = imageReader.read()

        if image.isNull():
            print(f"Error loading image: {imageReader.errorString()}")
            return

        self.originalPixmap = QPixmap.fromImage(image)
        self.imageLabel.setPixmap(self.originalPixmap)
        self.adjustImageSize()

        self.overviewWidget = OverviewWidget(self.originalPixmap, self)
        self.positionOverviewWidget()
        self.updateOverview()
    
    def positionOverviewWidget(self):
        # Positioneer de mini overview map
        self.overviewWidget.move(self.width() - self.overviewWidget.width() - 10, self.height() - self.overviewWidget.height() - 10)

        # Update de positie en grootte van het witte vlak
        self.whiteOverlay.move(self.width() - self.overviewWidget.width() - 10, self.height() - self.overviewWidget.height() - 10)


    def adjustImageSize(self):
        if self.imageLabel and self.originalPixmap:
            scaledPixmap = self.originalPixmap.scaled(
                int(self.zoomFactor * self.originalPixmap.width()),
                int(self.zoomFactor * self.originalPixmap.height()),
                Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Behoud de verhoudingen
            self.imageLabel.setPixmap(scaledPixmap)
            self.imageLabel.resize(scaledPixmap.size())  # Update de grootte van QLabel
        self.updateOverview()

    def updateOverview(self):
            if self.overviewWidget and self.imageLabel:
                visibleRect = self.scrollArea.viewport().rect()
                visibleRect.moveTo(
                    self.scrollArea.horizontalScrollBar().value(), 
                    self.scrollArea.verticalScrollBar().value()
                )
                # Update de aanroep van setViewRect met de huidige zoomFactor
                self.overviewWidget.setViewRect(visibleRect, self.zoomFactor)

            
    def connectScrollBars(self):
        # Verbind de scrollbalk signalen met updateOverview
        self.scrollArea.horizontalScrollBar().valueChanged.connect(self.updateOverview)
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.updateOverview)



    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overviewWidget:
            self.positionOverviewWidget()
            # Zorg ervoor dat het witte vlak de positie van de overviewWidget volgt
            self.whiteOverlay.setGeometry(self.overviewWidget.geometry())

        self.console.move(0, self.height() - 20)  # Keep console at the bottom
        self.console.setFixedWidth(self.width())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.lastMousePosition = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Bereken hoeveel de muis is verplaatst
            delta = event.pos() - self.lastMousePosition
            self.lastMousePosition = event.pos()

            # Scroll de afbeelding
            self.scrollArea.horizontalScrollBar().setValue(
                self.scrollArea.horizontalScrollBar().value() - delta.x())
            self.scrollArea.verticalScrollBar().setValue(
                self.scrollArea.verticalScrollBar().value() - delta.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
    
    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Zoom in
        if event.angleDelta().y() > 0:
            self.zoomFactor *= zoomInFactor
        # Zoom out
        elif event.angleDelta().y() < 0:
            self.zoomFactor *= zoomOutFactor

        self.adjustImageSize()
        self.updateOverview()
        print("test")


@contextmanager
def stdout_redirect(to):
    sys.stdout = to
    try:
        yield to
    finally:
        sys.stdout = sys.__stdout__

class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

    def flush(self):
        pass


def run_command(input_yaml, output_yaml):
    try:
        # Construct the command with the provided file names
        command = f"gen-yuml {input_yaml} > {output_yaml}"

        # Execute the command
        subprocess.run(command, shell=True, check=True)

        print("Command executed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def convert_yuml_to_uml(file_path, output_path='test.svg'):
    # Read the yUML content from the file
    with open(file_path, 'r') as file:
        yuml_content = file.read()

    # Send the request to the yUML API
    response = requests.get(yuml_content)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the image
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"UML diagram successfully saved as {output_path}")
    else:
        print("Error occurred while creating the UML diagram")



# Define the file path you want to monitor
file_path = "personinfo.yaml"

# Get the initial modification timestamp of the file
initial_timestamp = os.path.getmtime(file_path)

def is_yaml_file_corrupted(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            yaml.safe_load(yaml_file)
        output_yuml = "yuml.yuml"
        run_command(file_path, output_yuml)
        print("run command")
        convert_yuml_to_uml('yuml.yuml')
        print(f"The YAML file at {file_path} is not corrupted.")
        print('')
        app = QApplication(sys.argv)
        viewer = ImageViewer()
        viewer.show()
        with stdout_redirect(Stream(newText=viewer.onUpdateText)):
            sys.exit(app.exec_())
        return False  # Parsing successful, file is not corrupted
    except yaml.YAMLError as e:
        print(f"The YAML file at {file_path} is corrupted.")
        print(f"YAML parsing error: {str(e)}")
        print('')
        return True  # Parsing failed, file is corrupted

try:
    print(f"Monitoring changes to {file_path}. Press Ctrl+C to stop.")
    while True:
        current_timestamp = os.path.getmtime(file_path)
        
        if current_timestamp != initial_timestamp:
            print(f"File {file_path} has been modified!")
            initial_timestamp = current_timestamp
            is_yaml_file_corrupted(file_path)
        
        time.sleep(1)  # Poll every 1 second (adjust as needed)
except KeyboardInterrupt:
    pass
