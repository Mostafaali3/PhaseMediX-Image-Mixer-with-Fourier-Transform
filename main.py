import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QFileDialog, QLabel, QComboBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from helper_function.compile_qrc import compile_qrc
from classes.imageViewer import ImageViewer
from classes.componentsViewer import ComponentViewer
from classes.customImage import CustomImage
from classes.controller import Controller
from copy import copy
import cv2

compile_qrc()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Image Mixer')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))
        
        self.image_viewer_frame_1 = self.findChild(QFrame, 'image1')
        self.components_viewer_frame_1 = self.findChild(QFrame, 'image1Frequancy')
        self.image_viewer_1 = ImageViewer()
        self.components_viewer_1 = ComponentViewer()
        self.components_viewer_frame_1.layout().addWidget(self.components_viewer_1)
        self.image_viewer_frame_1.layout().addWidget(self.image_viewer_1)
        
        self.image_viewer_frame_2 = self.findChild(QFrame, 'image2')
        self.components_viewer_frame_2 = self.findChild(QFrame, 'image2Frequency')
        self.image_viewer_2 = ImageViewer()
        self.components_viewer_2 = ComponentViewer()
        self.components_viewer_frame_2.layout().addWidget(self.components_viewer_2)
        self.image_viewer_frame_2.layout().addWidget(self.image_viewer_2)
        
        self.image_viewer_frame_3 = self.findChild(QFrame, 'image3')
        self.components_viewer_frame_3 = self.findChild(QFrame, 'image3Frequency')
        self.image_viewer_3 = ImageViewer()
        self.components_viewer_3 = ComponentViewer()
        self.components_viewer_frame_3.layout().addWidget(self.components_viewer_3)
        self.image_viewer_frame_3.layout().addWidget(self.image_viewer_3)
        
        self.image_viewer_frame_4 = self.findChild(QFrame, 'image4')
        self.components_viewer_frame_4 = self.findChild(QFrame, 'image4Frequency')
        self.image_viewer_4 = ImageViewer()
        self.components_viewer_4 = ComponentViewer()
        self.components_viewer_frame_4.layout().addWidget(self.components_viewer_4)
        self.image_viewer_frame_4.layout().addWidget(self.image_viewer_4)
        
        self.output_viewer_frame_1 = self.findChild(QFrame, 'output1Frame')
        self.output_viewer_1 = ImageViewer()
        self.output_viewer_frame_1.layout().addWidget(self.output_viewer_1)
        
        self.output_viewer_frame_2 = self.findChild(QFrame, 'output2Frame')
        self.output_viewer_2 = ImageViewer()
        self.output_viewer_frame_2.layout().addWidget(self.output_viewer_2)
        
        self.list_of_combo_boxes = []
        for i in range(1,5):
            index = copy(i)
            combo_box = self.findChild(QComboBox, f"image{i}ComboBox")
            self.list_of_combo_boxes.append(combo_box)
        
        self.list_of_images = [CustomImage(), CustomImage(), CustomImage(), CustomImage()]
        self.list_of_image_viewers = [self.image_viewer_1, self.image_viewer_2, self.image_viewer_3, self.image_viewer_4]
        self.list_of_component_viewers = [self.components_viewer_1, self.components_viewer_2, self.components_viewer_3, self.components_viewer_4]
        
        self.controller = Controller(self.list_of_images, self.list_of_component_viewers, self.list_of_image_viewers, self.list_of_combo_boxes)
        self.controller.list_of_images = self.list_of_images
        self.controller.list_of_component_viewers = self.list_of_component_viewers
        self.controller.list_of_image_viewers = self.list_of_image_viewers
        self.controller.list_of_combo_boxes = self.list_of_combo_boxes
        
        #setting the double click handlers
        for i, viewer in enumerate(self.list_of_image_viewers):
            viewer.set_double_click_handler(lambda i=i: self.load_image(i))
        
        
        
        
    def load_image(self, viewer_number):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.jpeg *.jpg *.png *.bmp *.gif);;All Files (*)')
        
        print(viewer_number)
        if file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
            image = cv2.imread(file_path)
            # image = cv2.flip(image,0)
            new_image = CustomImage(image)
            self.list_of_images[viewer_number] = new_image
            self.list_of_image_viewers[viewer_number].current_image = new_image
            self.list_of_component_viewers[viewer_number].current_image = new_image
            self.controller.set_current_images_list()
            # pass
            # print(viewer_number)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())