from classes.viewer import Viewer
import numpy as np
import pyqtgraph as pg 
from PyQt5.QtWidgets import QFileDialog, QLabel, QGraphicsView
from PyQt5.QtGui import QPixmap, QImage, QMouseEvent
from PyQt5.QtCore import Qt
import cv2
import logging

# from PyQt5.QtGui import QMouseEvent

class ImageViewer(Viewer):
    def __init__(self):
        super().__init__()
        # self.show_grid(x=False, y=False)
        # self.getView().invertX(True)
        # self.getView().invertY(True)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_image = []
        self.double_click_handler = None
        self.mouse_release_handler = None
        self.prev_mouse_pos = None
        self.brigtness_offset = 0
        self.contrast_offset = 0
        self.change_in_y = 0
        self.change_in_x = 0
        self.current_Image_Item = None
        self.setMouseTracking(True)
        self.flag =0
        # self.getView().setAspectLocked(False)
    
    def mouseDoubleClickEvent(self, event):
        if self.double_click_handler is not None:
            self.double_click_handler()
        return super().mouseDoubleClickEvent(event)
    
    def set_double_click_handler(self, handler):
        self.double_click_handler = handler
    
    def update_plot(self):
        if self.current_image.modified_image[2].ndim == 2:
            self.clear()
            # self.current_Image_Item = pg.ImageItem(self.current_image.modified_image[2])
            
            self.setImage(self.current_image.modified_image[2].T)
            logging.debug("Current plot has been updated. Modified_image is now 2D")
            self.getView().setAspectLocked(True)
            self.getView().autoRange()
            self.getView().setMouseEnabled(x=False, y=False)
            
            if self.flag == 0 and self.mouse_release_handler is not None:
                self.getImageItem().scene().mousePressEvent = self.mousePressEvent
                self.getImageItem().scene().mouseMoveEvent = self.mouseMoveEvent
                self.getImageItem().scene().mouseReleaseEvent = self.mouseReleaseEvent
                self.flag =1
            
            
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.prev_mouse_pos = event.pos()
            self.is_left_button_pressed = True
            logging.debug(f"Left mouse button is pressed at {event.pos().y()}.")

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_left_button_pressed = False
            # if self.mouse_release_handler is not None:
            self.mouse_release_handler()
            logging.debug(f"Left mouse button is released at {event.pos().y()}.")

    def set_mouse_release_handler(self, handler):
        self.mouse_release_handler = handler
                    
    def mouseMoveEvent(self, event):
        if self.is_left_button_pressed:
            self.change_in_y = event.scenePos().y() - self.prev_mouse_pos.y()
            self.change_in_x = event.scenePos().x() - self.prev_mouse_pos.x()
            self.brigtness_offset = self.change_in_y *1
            self.contrast_offset = self.change_in_x * 0.001
            self.custom_adjust_brightness(self.brigtness_offset, self.contrast_offset)
            self.prev_mouse_pos = event.pos()
            self.update_plot()
            logging.info(f"Update the brightness and contrast of the image.")

            
    def custom_adjust_brightness(self, brightness, contrast):
        self.current_image.modified_image[2] = cv2.convertScaleAbs(self.current_image.original_sized_image[2], alpha=1+contrast, beta=brightness)
            
                    
    def image_to_pixmap(self):
        try:
            if not isinstance(self.current_image, list):
                if len(self.current_image.modified_image[2] == 2):
                    height, width = self.current_image.modified_image[2].shape
                    q_image = QImage(self.current_image.modified_image[2].data, width, height, QImage.Format_Grayscale8)
                    self.current_pixmap = QPixmap.fromImage(q_image)
                    logging.info("Attempting to convert grayscale image to QPixmap")
                    return self.current_pixmap
        except Exception as e:
            logging.error("Error occurred in image_to_pixmap function {e}")
    def color_handle(self):
        pass
    
    def size_handle(self):
        pass
    
    def adjust_brightness(self):
        pass
    
    def adjust_contrast(self):
        pass
