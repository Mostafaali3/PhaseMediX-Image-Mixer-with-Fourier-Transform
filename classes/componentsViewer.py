from classes.viewer import Viewer
import numpy as np 
from PyQt5.QtWidgets import QFileDialog, QLabel

class ComponentViewer(QLabel):
    def __init__(self):
        super().__init__()
        # self.show_grid(x=False, y=False)
        self.current_signal = []
        pass
    
    def update_plot(self):
        pass
    
    def size_handle(self):
        pass
    