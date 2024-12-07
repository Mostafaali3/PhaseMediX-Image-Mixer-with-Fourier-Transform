from classes.viewer import Viewer
import numpy as np 
from PyQt5.QtWidgets import QFileDialog, QLabel
import pyqtgraph as pg

class ComponentViewer(Viewer):
    def __init__(self):
        super().__init__()
        self.roii = pg.ROI([50, 50], [50, 50], movable=True, resizable=True)  # Initial position and size
        self.roii.addScaleHandle([1, 1], [0, 0])  # Add handles for resizing
        self.roii.addScaleHandle([0, 0], [1, 1])
        self.ui.roiBtn.setChecked(True)
        # self.show_grid(x=False, y=False)
        
        
    
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
            elif plot_type == "Phase":
                phase = np.angle(self.current_image.modified_image_fourier_components).T
                phase_normalized = (phase + np.pi) * (255.0 / (2 * np.pi))  # Normalize to [0, 255]
                phase_normalized = phase_normalized.astype(np.uint8)
                self.setImage(phase_normalized)
            elif plot_type == "Real":
                real = self.current_image.modified_image_fourier_components.T.real
                real_clipped = np.clip(real, 1e-10, None)
                real_log = np.log1p(real_clipped)
                real_normalized = (real_log - np.min(real_log)) * (255.0 / (np.max(real_log) - np.min(real_log)))
                real_normalized = real_normalized.astype(np.uint8)
                self.setImage(real_normalized)
            elif plot_type == "Imaginary":
                imaginary = self.current_image.modified_image_fourier_components.T.imag
                imaginary_clipped = np.clip(imaginary, 1e-10, None)
                imaginary_log = np.log1p(imaginary_clipped)
                imaginary_normalized = (imaginary_log - np.min(imaginary_log)) * (255.0 / (np.max(imaginary_log) - np.min(imaginary_log)))
                imaginary_normalized = imaginary_normalized.astype(np.uint8)
                self.setImage(imaginary_normalized)
            self.getView().autoRange()
            self.getView().setMouseEnabled(x=False, y=False)
            
            
    
    def size_handle(self):
        pass
    