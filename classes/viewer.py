from abc import ABC, abstractmethod
import pyqtgraph as pg

class Viewer(pg.PlotWidget, ABC):
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def update_plot(self):
        pass