from classes.mixer import Mixer
from copy import copy
import numpy as np

class Controller():
    def __init__(self, list_of_iamges,list_of_image_viewers,list_of_component_viewers, list_of_combo_boxes):
        self.list_of_images = list_of_iamges
        self.list_of_image_viewers = list_of_image_viewers
        self.list_of_component_viewers = list_of_component_viewers
        self.list_of_combo_boxes = list_of_combo_boxes
        for box in self.list_of_combo_boxes:
            box.currentTextChanged.connect(self.set_current_images_list)
            

            
        self.Mixer = Mixer()
        self.result_image_1 = None #custom image
        self.result_image_2 = None #custom image
        self.min_hight = 50000
        self.min_width = 50000
        
    def get_min_image_size(self):
        '''
        this function gets the min width and hight of all images
        '''
        # min_width, min_hight = 500000, 500000
        for image in self.list_of_images:
            if image.loaded:
                self.min_hight = min(self.min_hight,image.original_image[2].shape[0])
                self.min_width = min(self.min_width,image.original_image[2].shape[1])
                
    
    def update_image_plots(self):
        '''
        this function updates all the image plots , make fourier transform if the image changed for any reason 
        also checks if we need to make the transform or not for the optimization 
        '''
        for i,image in enumerate(self.list_of_images):
            if image.loaded:
                index = copy(i)
                self.list_of_images[index].handle_image_size(self.min_hight, self.min_width)
                
                if not self.list_of_images[index].original_image[2].shape == self.list_of_images[index].modified_image.shape:
                    self.list_of_images[index].transform()
                elif not np.array_equal(self.list_of_images[index].modified_image[2], self.list_of_images[index].original_image[2]):
                    self.list_of_images[index].transform()

                self.list_of_image_viewers[index].set_mouse_release_handler(self.set_current_images_list)
                
                self.list_of_image_viewers[index].current_image = self.list_of_images[index]
                self.list_of_image_viewers[index].update_plot()
                # print(f"components size{self.list_of_images[i].original_image_fourier_components.ndim}")
                
    def update_component_plots(self):
        '''
        this function updates all the component plots  
        '''
        for i, image in enumerate(self.list_of_images):
            if image.loaded:
                index = copy(i)
                self.list_of_component_viewers[index].curret_image = self.list_of_images[index]
                self.list_of_component_viewers[index].update_plot(self.list_of_combo_boxes[index].currentText())
                
        
    def set_current_images_list(self):
        self.get_min_image_size()
        self.update_image_plots()
        self.update_component_plots()
                
                
    
    def mix_all(self, output_viewer_number:int):
        pass