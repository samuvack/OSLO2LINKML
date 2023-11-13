import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea, QWidget
from PyQt5.QtGui import QPixmap, QImageReader, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect

class OverviewWidget(QWidget):
    def __init__(self, originalPixmap, parent=None):
        super().__init__(parent)
        self.originalPixmap = originalPixmap
        self.viewRect = QRect()
        self.updateSize()
        self.setStyleSheet("background-color: white; border: 1px solid gray;")  # Witte achtergrond en grijze rand
    


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
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.zoomFactor = 1.0
        self.originalPixmap = None
        self.imageLabel = None
        self.overviewWidget = None

        # Load image
        self.loadImage("test.svg")  # Replace with your image path


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
        self.overviewWidget.move(self.width() - 210, self.height() - 210)
        self.updateOverview()

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
            self.overviewWidget.setViewRect(visibleRect)
            
    def connectScrollBars(self):
        # Verbind de scrollbalk signalen met updateOverview
        self.scrollArea.horizontalScrollBar().valueChanged.connect(self.updateOverview)
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.updateOverview)


    def resizeEvent(self, event):
        if self.overviewWidget:
            self.overviewWidget.move(self.width() - 210, self.height() - 210)
        super().resizeEvent(event)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
