from PyQt5.QtGui import QPen, QColor, QPainterPath, QBrush
from PyQt5.QtCore import QRectF
import pyqtgraph as pg


class CustomRectROI(pg.RectROI):
    def __init__(self, pos, size, pen=None, **kwargs):
        """
        Custom Rectangular ROI with support for 'inner', 'outer', and 'full' region drawing.
        """
        # Convert pen string to QPen if needed
        if isinstance(pen, str):
            pen = QPen(QColor(pen))

        super().__init__(pos, size, pen=pen, **kwargs)

        # Default settings
        self.region_mode = 'inner'  # Modes: 'inner', 'outer', 'full'
        self.max_bounds = QRectF(-500, -500, 1000, 1000)  # Default outer bounds

        # Avoid redundant updates

    def set_image(self, image):
        """
        Sets image bounds to limit ROI movement.
        """
        if self.max_bounds == image.boundingRect():
            return  # Avoid redundant updates

        self.max_bounds = image.boundingRect()
        self.setPos(self.max_bounds.topLeft())  # Align ROI position
        self.setSize(self.max_bounds.size())    # Adjust size to image bounds

    def handle_roi_change(self):
        """
        Trigger updates for region mode.
        """
        self.update()  # Force repaint

    def paint(self, painter, option, widget=None):
        """
        Custom paint function to draw the ROI based on the region mode.
        """

        if self.region_mode == 'inner':
            painter.setBrush(QColor(0, 255, 0, 50))  # Semi-transparent green
            painter.drawRect(self.boundingRect())
        elif self.region_mode == 'outer':
            painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red
            painter.drawRect(self.boundingRect())  # Draw full bounds
            painter.setBrush(QBrush())  # Reset brush
            painter.drawRect(self.boundingRect())  # Subtract ROI
        elif self.region_mode == 'full':
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))  # Fully transparent
            painter.drawRect(self.boundingRect())


    def set_region(self, region):
        """
        Update the current region type ('inner', 'outer', 'full') and trigger update.
        """
        if region not in {'inner', 'outer', 'full'}:
            raise ValueError("Region must be 'inner', 'outer', or 'full'")
        self.region_mode = region
        self.handle_roi_change()  # Trigger update
