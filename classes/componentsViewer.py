from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsRectItem
import numpy as np
import pyqtgraph as pg
from classes.CustomROI import CustomRectROI
from classes.viewer import Viewer

class ComponentViewer(Viewer):
    def __init__(self):
        """
        Initialize ComponentViewer with custom ROI and default settings.
        """
        super().__init__()
        self.region_mode = "full"

        # Custom Rectangular ROI
        self.roi = CustomRectROI([0, 0], [20, 20], pen='r', movable=True, resizable=True)
        self.roi.addScaleHandle([1, 1], [0, 0])
        self.roi.addScaleHandle([0, 0], [1, 1])
        self.roi.hide()

        # Transparent rectangle for full/outer visualization
        self.transparent_rect = None

        # Add ROI to the view
        self.getView().addItem(self.roi)

        # Track view bounds
        self.xmin = self.ymin = self.xmax = self.ymax = 0

    def update_plot(self, plot_type: str):
        """
        Update the current image plot based on the selected plot type.
        Args:
            plot_type (str): 'Magnitude', 'Phase', 'Real', or 'Imaginary'.
        """
        if self.current_image.modified_image[2].ndim == 2:
            # Remove previous transparent rect if exists
            # if self.transparent_rect:
            #     self.getView().removeItem(self.transparent_rect)

            # Plot selected component
            if plot_type == "Magnitude":
                magnitude = self.current_image.modified_image_fourier_components_mag.T
                processed_image = self._normalize_and_convert(np.log1p(magnitude))
            elif plot_type == "Phase":
                phase = self.current_image.modified_image_fourier_components_phase.T
                processed_image = self._normalize_and_convert((phase + np.pi) * (255.0 / (2 * np.pi)))
            elif plot_type == "Real":
                real = self.current_image.modified_image_fourier_components_real
                processed_image = self._normalize_and_convert(np.log1p(np.clip(real, 1e-10, None)))
            elif plot_type == "Imaginary":
                imaginary = self.current_image.modified_image_fourier_components_imag
                processed_image = self._normalize_and_convert(np.log1p(np.clip(imaginary, 1e-10, None)))
            else:
                return  # Invalid plot type

            self.setImage(processed_image)

            # Show ROI and update bounds
            self.roi.show()
            # self.getView().autoRange()
            self.getView().setMouseEnabled(x=False, y=False)

            # Update view range for ROI bounds
            self._update_view_bounds()

            # Set ROI bounds to the current image
            # self.roi.set_image(self.getImageItem())
            self.roi.maxBounds = self.getImageItem().boundingRect()

    def set_region(self, region):
        """
        Set the current ROI region mode and update the transparent rectangle.
        Args:
            region (str): 'full', 'inner', or 'outer'.
        """
        self.region_mode = region

        # Remove previous transparent rect
        if self.transparent_rect:
            self.getView().removeItem(self.transparent_rect)
            self.transparent_rect = None

        # Add transparent overlay if needed
        if region in {'inner', 'outer'}:
            self.transparent_rect = QGraphicsRectItem(self.getImageItem().boundingRect())
            color = QColor(0, 255, 0, 50) if region == 'outer' else QColor(255, 0, 0, 50)
            self.getView().removeItem(self.transparent_rect)

            self.transparent_rect.setBrush(QBrush(color))
            self.getView().addItem(self.transparent_rect)

        # Update ROI's mode
        self.roi.set_region(region)
        self.update()
    def _normalize_and_convert(self, image):
        """
        Normalize and convert the image to 8-bit format.
        """
        normalized = (image - np.min(image)) * (255.0 / (np.max(image) - np.min(image)))
        return normalized.astype(np.uint8)

    def _update_view_bounds(self):
        """
        Update the minimum and maximum bounds of the view.
        """
        view_range = self.getView().viewRange()
        self.xmin, self.xmax = view_range[0]  # X range
        self.ymin, self.ymax = view_range[1]  # Y range
