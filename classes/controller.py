from classes.mixer import Mixer
from copy import copy
from classes.modesEnum import RegionMode
from classes.customImage import CustomImage
import numpy as np
import cv2

class Controller():
    def __init__(self, list_of_iamges,list_of_image_viewers,list_of_component_viewers, list_of_combo_boxes , list_of_output_viewers):
        self.list_of_images = list_of_iamges
        self.list_of_image_viewers = list_of_image_viewers
        self.list_of_component_viewers = list_of_component_viewers
        self.list_of_combo_boxes = list_of_combo_boxes
        self.list_of_output_viewers = list_of_output_viewers
        for box in self.list_of_combo_boxes:
            box.currentTextChanged.connect(self.set_current_images_list)
            

            
        self.Mixer = Mixer()
        self.result_image_1 = None #custom image
        self.result_image_2 = None #custom image
        self.min_hight = 50000
        self.min_width = 50000
        self.image_weights = [25,25,25,25]
        # self.old_image_weights = [25,25,25,25]
        
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
                image_hight, image_width  = self.list_of_images[index].original_sized_image[2].shape[:2]
                if image_width!=self.min_width or image_hight!= self.min_hight:
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
                
    # def detect_and_adjust_weights(current_weights, incoming_weights, tolerance=1e-6):
        
    #     modified_indices = [
    #         i for i in range(len(current_weights))
    #         if abs(current_weights[i] - incoming_weights[i]) > tolerance
    #     ]
        
    #     adjusted_values = [incoming_weights[i] for i in modified_indices]
        
    #     fixed_weights_sum = sum(incoming_weights[i] for i in modified_indices)
    #     remaining_weight = 1.0 - fixed_weights_sum
        
    #     unadjusted_indices = [i for i in range(len(current_weights)) if i not in modified_indices]
    #     if unadjusted_indices:
    #         equal_weight = remaining_weight / len(unadjusted_indices)
    #         for idx in unadjusted_indices:
    #             incoming_weights[idx] = equal_weight
        
    #     return incoming_weights, modified_indices, adjusted_values            
    
    def mix_all(self, output_viewer_number:int ,region_mode):
        self.Mixer.images_list = self.list_of_images
        temp_weights = self.image_weights
        self.image_weights = [weight / 100 for weight in self.image_weights]
        mixer_result = self.Mixer.mix(self.image_weights,[0],region_mode)
        mixer_result_normalized = cv2.normalize(mixer_result , None ,0 ,255 ,cv2.NORM_MINMAX).astype(np.uint8)
        self.result_image_1 = CustomImage(mixer_result_normalized)
        self.list_of_output_viewers[output_viewer_number].current_image = self.result_image_1
        self.list_of_output_viewers[output_viewer_number].update_plot()
        self.image_weights = temp_weights