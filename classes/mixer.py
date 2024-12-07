from classes.customImage import CustomImage
from classes.modesEnum import Mode , RegionMode
import numpy as np
class Mixer():
    def __init__(self):
        self.images_list = []
        self.__result_image_1 = CustomImage()
        self.__result_image_2 = CustomImage()
        self.__current_mode = Mode.MAGNITUDE_PHASE
        self.images_modes = [Mode.MAGNITUDE , Mode.MAGNITUDE, Mode.MAGNITUDE, Mode.MAGNITUDE]
    
    @property
    def current_mode(self):
        return self.__current_mode
    
    @current_mode.setter
    def current_mode(self , new_mode):
        self.__current_mode = new_mode

    @property
    def result_image_1(self):
        return self.__result_image_1
    
    @result_image_1.setter
    def result_image_1(self , new_result_image_1):
        if (isinstance(new_result_image_1 , CustomImage)):
            self.__result_image_1 = new_result_image_1
        
    @property
    def result_image_2(self):
        return self.__result_image_2
    
    @result_image_2.setter
    def result_image_2(self , new_result_image_2):
        if (isinstance(new_result_image_2 , CustomImage)):
            self.__result_image_2 = new_result_image_2
        
        
    def mix(self, weights, view_port:int , boundaries , region_mode):
        resulted_mix = []
        if (self.current_mode == Mode.MAGNITUDE_PHASE):
            for image_number in range(len(self.images_list)):
                if(len(self.images_list[image_number].original_image[2]) == 0 ):
                    continue
                
                region_image = self.images_list[image_number].original_image[2]
                
                if (region_mode == RegionMode.INNER):
                    region_image = region_image[boundaries[2]:boundaries[3]+1 , boundaries[0]:boundaries[1]+1 ]
                    
                if (region_mode == RegionMode.OUTER):
                    left_region = region_image[boundaries[2]:boundaries[3]+1 , :boundaries[0]]
                    right_region = region_image[boundaries[2]:boundaries[3]+1 , boundaries[1]+1 :]
                    top_region = region_image[boundaries[3]+1: , :]
                    bottom_region = region_image[:boundaries[2] , :]
                    
                    top_bottom_region = np.vstack((bottom_region , top_region ))
                    left_right_region = np.hstack((left_region , np.zeros((boundaries[3] - boundaries[2] +1 , boundaries[1] - boundaries[0] +1  )),right_region))
                    region_image = np.vstack((top_bottom_region , left_right_region))
                print(region_image)
                image_magnitude = np.abs(self.images_list[image_number].original_image_fourier_components)
                image_phase = np.angle(self.images_list[image_number].original_image_fourier_components)
                
                if(self.images_modes[image_number] == Mode.MAGNITUDE):
                    weighted_image_magnitude = image_magnitude * weights[image_number]
                    
                if(self.images_modes[image_number] == Mode.PHASE):
                    weighted_image_phase = image_phase * weights[image_number]
                    
        elif (self.current_mode == Mode.REAL_IMAGINARY):
            pass