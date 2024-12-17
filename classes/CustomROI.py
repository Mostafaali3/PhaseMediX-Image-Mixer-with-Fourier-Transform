from PyQt5.QtGui import QPen, QColor, QPainterPath, QBrush
from PyQt5.QtCore import QRectF
import pyqtgraph as pg


class CustomRectROI(pg.RectROI):
    def __init__(self, pos, size, pen=None, **kwargs):
        """
        Custom Rectangular ROI with support for inner/outer region drawing.
        """
        
        # Convert pen string to QPen if needed
        if isinstance(pen, str):
            pen = QPen(QColor(pen))

        super().__init__(pos, size, pen=pen, **kwargs)

        self.region_mode = 'inner'  # Modes: 'inner' or 'outer'
        self.max_bounds = QRectF(-500, -500, 1000, 1000)  # Set large bounds for the outer region
        self.outer_path = QPainterPath()  # Path for the outer region
        self.inner_path = QPainterPath()  # Path for the inner region

        # Connect ROI region change signal
        self.sigRegionChanged.connect(self.handle_roi_change)
    
    def handle_roi_change(self):
        """
        Update the paths for the inner and outer regions dynamically.
        """
                # Trigger repaint of the ROI
        self.update()

    def paint(self, painter, option, widget=None):
        """
        Custom paint function to draw the ROI and outer region.
        """
        # Call the region update logic
        self.handle_roi_change()

        if self.region_mode == 'inner':
            # Inner mode: Fill the ROI with a semi-transparent color
            painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red
            painter.drawRect(self.max_bounds)
            painter.setBrush(QColor(0, 255, 0, 50))  # Semi-transparent green
            painter.drawRect(self.boundingRect())
        elif self.region_mode == 'outer': 
            # Outer mode: Draw the outer region with the ROI subtracted
            painter.setBrush(QColor(0, 255, 0, 50))  # Semi-transparent red
            painter.drawRect(self.max_bounds)
            painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent green
            painter.drawRect(self.boundingRect())


        
    def set_region(self, region):
        """
        Update the region type (inner or outer).
        """
        self.region_mode = region
        self.handle_roi_change()
        self.update()
        # Trig
        print(region)