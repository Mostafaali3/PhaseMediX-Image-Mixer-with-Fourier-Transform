from classes.viewer import Viewer
import numpy as np
from PyQt5.QtWidgets import QFileDialog

class ImageViewer(Viewer):
    def __init__(self):
        super().__init__()
        # self.show_grid(x=False, y=False)
        self.current_signal = []
    
    def update_plot(self):
        pass
    
    def color_handle(self):
        pass
    
    def size_handle(self):
        pass
    
    def adjust_brightness(self):
        pass
    
    def adjust_contrast(self):
        pass
