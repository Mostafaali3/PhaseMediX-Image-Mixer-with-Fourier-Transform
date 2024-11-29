from abc import ABC, abstractmethod
import pyqtgraph as pg

class Viewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground("#142A4A")
        self.getAxis('bottom').hide()  # Hides the x-axis
        self.getAxis('left').hide()

    def update_plot(self):
        pass