from classes.viewer import Viewer
import numpy as np
from PyQt5.QtWidgets import QFileDialog
# from PyQt5.QtGui import QMouseEvent

class ImageViewer(Viewer):
    def __init__(self):
        super().__init__()
        # self.show_grid(x=False, y=False)
        self.current_image = []
        self.double_click_handler = None
    
    def mouseDoubleClickEvent(self, event):
        if self.double_click_handler is not None:
            self.double_click_handler()
        return super().mouseDoubleClickEvent(event)
    
    def set_double_click_handler(self, handler):
        self.double_click_handler = handler
    
    def update_plot(self):
        self.clear()
        self.plot(self.current_image.modified_image[2])
        
    
    def color_handle(self):
        pass
    
    def size_handle(self):
        pass
    
    def adjust_brightness(self):
        pass
    
    def adjust_contrast(self):
        pass
