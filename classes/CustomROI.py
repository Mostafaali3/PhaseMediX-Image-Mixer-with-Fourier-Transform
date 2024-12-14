from PyQt5.QtGui import QPen, QColor
import pyqtgraph as pg
from PyQt5.QtGui import QPainter, QColor, QPolygonF,QBrush, QPainterPath
from PyQt5.QtCore import QRectF, QPointF

class CustomRectROI(pg.RectROI):
    def __init__(self, pos, size, pen=None, **kwargs):
        # If pen is a string, convert it to QPen
        if isinstance(pen, str):
            pen = QPen(QColor(pen))  # Convert the string to a QPen with the specified color
        super().__init__(pos, size, pen, **kwargs)
        self.region = 'inner'
    def paint(self, painter, *args):
        """
        Custom paint event to override the default painting behavior.
        Fills the ROI with a semi-transparent color or pattern.
        """
        
        bounds_rect = self.maxBounds
        rect = QRectF(0, 0, self.state['size'][0], self.state['size'][1]).normalized()
        painter.setPen(self.currentPen)
        painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red
        
        outer_path = QPainterPath()
        outer_path.addRect(bounds_rect)  # Full outer rectangle

        inner_path = QPainterPath()
        inner_path.addRect(rect) 
        if self.region == 'inner':
            painter.drawRect(rect)
        else :
           # Fill the outer region (area outside the inner rectangle)
        # Step 1: Fill the entire bounding rectangle
            outer_path = outer_path.subtracted(inner_path)  # Subtract the inner region
            painter.setBrush(QColor(255, 0, 0, 50))  # Semi-transparent red for the outer region
            painter.drawPath(outer_path)
    def set_region(self, region):
        self.region = region

    def get_rectangle_points(self,bounds_rect, rect):
        # Bounds rectangle corners (8 points in total)
        bounds_top_left = bounds_rect.topLeft()
        bounds_top_right = bounds_rect.topRight()
        bounds_bottom_left = bounds_rect.bottomLeft()
        bounds_bottom_right = bounds_rect.bottomRight()

        # Rect rectangle corners (inside bounds_rect)
        rect_top_left = rect.topLeft()
        rect_top_right = rect.topRight()
        rect_bottom_left = rect.bottomLeft()
        rect_bottom_right = rect.bottomRight()

        # Return the list of 8 points
        points = [
            bounds_top_left,  # Top-left corner of bounds_rect
            bounds_top_right,  # Top-right corner of bounds_rect
            bounds_bottom_left,  # Bottom-left corner of bounds_rect
            bounds_bottom_right,  # Bottom-right corner of bounds_rect
            rect_top_left,  # Top-left corner of rect
            rect_top_right,  # Top-right corner of rect
            rect_bottom_left,  # Bottom-left corner of rect
            rect_bottom_right,  # Bottom-right corner of rect
        ]

        return points