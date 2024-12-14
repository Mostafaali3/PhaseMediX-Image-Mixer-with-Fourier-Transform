from classes.viewer import Viewer
import numpy as np 
from PyQt5.QtWidgets import QFileDialog, QLabel
import pyqtgraph as pg
from classes.controller import Controller
from classes.modesEnum import RegionMode

from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF 
from PyQt5.QtCore import QPointF, QRectF
class ComponentViewer(Viewer):
    def __init__(self):
        super().__init__()

        self.overlay_items = []  # List to track overlay items
    
        self.roi = pg.RectROI([0, 0], [20, 20], pen='r', movable=True, resizable=True)
        self.roi.addScaleHandle([1, 1], [0, 0])  # Add handles for resizing
        self.roi.addScaleHandle([0, 0], [1, 1])
        self.roi.hide()
        self.roi_x_min = 0
        self.roi_y_min = 0
        self.roi_x_max = 0
        self.roi_y_max = 0 
        self.roi_boundries = []
        # Add ROI to the view and connect its signal
        self.getView().addItem(self.roi)
        # self.roi.sigRegionChanged.connect(Controller.handle_roi_change(self.roi))
        view_range = self.getView().viewRange()

# Extract the minimum x and y values
        self.xmin, self.xmax = view_range[0]  # x range (xmin, xmax)
        self.ymin, self.ymax = view_range[1]  

        # self.show_grid(x=False, y=False)  
    def get_roi_boundries(self):
        return [
            [self.roi_x_min, self.roi_y_min],
            [self.roi_x_max, self.roi_y_max]
        ]      
    def handle_roi_change(self):
        """
        Handle ROI region changes and fetch the region coordinates.
        """
        # Get the current ROI bounds as [x, y, width, height]
        roi_bounds = self.roi.getState()['pos'] + self.roi.getState()['size']
        self.roi_x_min, self.roi_y_min = self.roi.pos()
        width, height = self.roi.size()
        self.roi_x_max, self.roi_y_max = self.roi_x_min + width, self.roi_y_min + height
        print(height)

    def update_plot(self, plot_type:str):
        if self.current_image.modified_image[2].ndim == 2:
            if hasattr(self, 'imageItem'):
                self.imageItem.setImage(self.current_image.modified_image[2])
            # self.current_Image_Item = pg.ImageItem(self.current_image.modified_image[2])
            if plot_type == "Magnitude":
                
                magnitude = np.abs(self.current_image.modified_image_fourier_components).T
                magnitude_log = np.log1p(magnitude)  
                magnitude_normalized = (magnitude_log - np.min(magnitude_log)) * (255.0 / (np.max(magnitude_log) - np.min(magnitude_log)))
                magnitude_normalized = magnitude_normalized.astype(np.uint8)
                self.setImage(magnitude_normalized)
                self.roi.show()
                
            elif plot_type == "Phase":
                phase = np.angle(self.current_image.modified_image_fourier_components).T
                phase_normalized = (phase + np.pi) * (255.0 / (2 * np.pi))  # Normalize to [0, 255]
                phase_normalized = phase_normalized.astype(np.uint8)
                self.setImage(phase_normalized)
                self.roi.show()

            elif plot_type == "Real":
                real = self.current_image.modified_image_fourier_components.T.real
                real_clipped = np.clip(real, 1e-10, None)
                real_log = np.log1p(real_clipped)
                real_normalized = (real_log - np.min(real_log)) * (255.0 / (np.max(real_log) - np.min(real_log)))
                real_normalized = real_normalized.astype(np.uint8)
                self.setImage(real_normalized)
                self.roi.show()

                
            elif plot_type == "Imaginary":
                imaginary = self.current_image.modified_image_fourier_components.T.imag
                imaginary_clipped = np.clip(imaginary, 1e-10, None)
                imaginary_log = np.log1p(imaginary_clipped)
                imaginary_normalized = (imaginary_log - np.min(imaginary_log)) * (255.0 / (np.max(imaginary_log) - np.min(imaginary_log)))
                imaginary_normalized = imaginary_normalized.astype(np.uint8)
                self.setImage(imaginary_normalized)
                self.roi.show()
                

            self.getView().autoRange()
            self.getView().setMouseEnabled(x=False, y=False)
            view_range = self.getView().viewRange()

# Extract the minimum x and y values
            self.xmin, self.xmax = view_range[0]  # x range (xmin, xmax)
            self.ymin, self.ymax = view_range[0]
            
            self.roi.maxBounds = QRectF(self.xmin, self.ymin, self.xmax, self.ymax)

    def fill_roi(self, mode):
        """
        Draw a transparent rectangle or polygon over the viewer.
        mode:
            1 - Rectangle
            2 - Polygon (using ROI vertices)
        """
        # Remove previously added overlays
        # for item in self.overlay_items:
        #     self.getView().removeItem(item)
   

        # Get ROI boundaries
        x_min, y_min = self.roi_x_min, self.roi_y_min
        x_max, y_max = self.roi_x_max, self.roi_y_max

        if mode == RegionMode.INNER:  # Draw a transparent rectangle
            rect_item = QGraphicsRectItem(x_min, y_min, x_max - x_min, y_max - y_min)
            rect_item.setPen(pg.mkPen('r', width=2))  # Red border
            rect_item.setBrush(pg.mkBrush(255, 0, 0, 50))  # Semi-transparent red fill
            self.getView().addItem(rect_item)
            self.overlay_items.append(rect_item)

        elif mode == RegionMode.OUTER:  # Draw a polygon based on ROI vertices
            # Get ROI vertices
            roi_bounds = self.roi.getArraySlice(self.current_image.modified_image[2], self.imageItem)[1]
            polygon = QPolygonF()
            for point in roi_bounds:
                polygon.append(QPointF(point[0], point[1]))

            polygon_item = QGraphicsPolygonItem(polygon)
            polygon_item.setPen(pg.mkPen('g', width=2))  # Green border
            polygon_item.setBrush(pg.mkBrush(0, 255, 0, 50))  # Semi-transparent green fill
            self.getView().addItem(polygon_item)
            self.overlay_items.append(polygon_item)
   
    def size_handle(self):
        pass
    