import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea, QWidget
from PyQt5.QtGui import QPixmap, QImageReader, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette, QColor


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

        # Variabelen voor muis tracking
        self.dragging = False
        self.lastMousePosition = None

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
        self.positionOverviewWidget()
        self.updateOverview()
    
    def positionOverviewWidget(self):
        # Positioneer de mini overview map
        self.overviewWidget.move(self.width() - self.overviewWidget.width() - 10, self.height() - self.overviewWidget.height() - 10)

        # Update de positie en grootte van het witte vlak
        self.whiteOverlay.setGeometry(self.overviewWidget.geometry())


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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    print("test")
    sys.exit(app.exec_())
    
    