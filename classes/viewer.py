from abc import ABC, abstractmethod
import pyqtgraph as pg

class Viewer(pg.ImageView):
    def __init__(self):
        super().__init__()
        # self.setBackground("#142A4A")
        # self.getAxis('bottom').show()  # Hides the x-axis
        # self.getAxis('left').show()
        # self.getAxis('left').invertY()
        # self.getView().invertY(False)
        self.getView().setBackgroundColor("#142A4A")
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

    def update_plot(self):
        pass