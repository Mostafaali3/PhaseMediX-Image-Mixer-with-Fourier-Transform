from classes.viewer import Viewer
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtGui import QMouseEvent

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        # self.show_grid(x=False, y=False)
        self.current_image = []
        self.double_click_handler = None
        self.current_pixmap = None
    
    def mouseDoubleClickEvent(self, event):
        if self.double_click_handler is not None:
            self.double_click_handler()
        return super().mouseDoubleClickEvent(event)
    
    def set_double_click_handler(self, handler):
        self.double_click_handler = handler
    
    def update_plot(self):
        self.image_to_pixmap()
        self.setPixmap(self.current_pixmap)
        self.setScaledContents(True)
        
    def image_to_pixmap(self):
        if not isinstance(self.current_image, list):
            if len(self.current_image.modified_image[2] == 2):
                height, width = self.current_image.modified_image[2].shape
                q_image = QImage(self.current_image.modified_image[2].data, width, height, QImage.Format_Grayscale8)
                self.current_pixmap = QPixmap.fromImage(q_image)
                return self.current_pixmap
    
    def color_handle(self):
        pass
    
    def size_handle(self):
        pass
    
    def adjust_brightness(self):
        pass
    
    def adjust_contrast(self):
        pass
