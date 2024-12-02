from copy import deepcopy
import numpy as np
import cv2
import matplotlib.pyplot as plt

class CustomImage():
    def __init__(self , image = []):
        if (len(image) != 0 ):
            imported_image_gray_scale = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
            # Height
            image_x_components = np.arange(1 , imported_image_gray_scale.shape[0] +1 )
            # Width
            image_y_components = np.arange(1 , imported_image_gray_scale.shape[1] +1 )
            self.__original_image = np.empty((3,), dtype=object)
            self.__original_image[0] = image_x_components
            self.__original_image[1] = image_y_components
            self.__original_image[2] = np.array(imported_image_gray_scale)
            self.__modified_image = deepcopy(self.__original_image)
            self.__original_image_fourier_components = np.empty((1,) , dtype= object)
        
    @property
    def original_image(self):
        return self.__original_image
    
    @original_image.setter
    def original_image(self , new_image):
        self.__original_image = new_image
        
    @property
    def modified_image(self):
        return self.__modified_image
    
    @modified_image.setter
    def modified_image(self , new_modified_image):
        self.__modified_image = new_modified_image
        
    @property
    def original_image_fourier_components(self):
        return self.__original_image_fourier_components
    
    @original_image_fourier_components.setter
    def original_image_fourier_components(self , new_original_image_fourier_components):
        self.__original_image_fourier_components = new_original_image_fourier_components
    
    @property
    def modified_image_fourier_components(self):
        return self.__modified_image_fourier_components
    
    @modified_image_fourier_components.setter
    def modified_image_fourier_components(self , new_modified_image_fourier_components):
        self.__modified_image_fourier_components = new_modified_image_fourier_components
        
    
    def fourier_transform_image(self):
        fourier_transformed_image = np.fft.fft2(self.modified_image[2])
        shifted_fourier_transformed_image = np.fft.fftshift(fourier_transformed_image)
        self.original_image_fourier_components = shifted_fourier_transformed_image
        self.modified_image_fourier_components = deepcopy(self.original_image_fourier_components) 
    
    
    def handle_image_size(self , height , width):
        current_image_height , current_image_width  = self.original_image[2].shape[:2]  
        if(width == current_image_width and height == current_image_height):
            return
        else:
            self.modified_image[0] = np.arange(1 , height + 1)
            self.modified_image[1] = np.arange(1 , width + 1)
            self.modified_image[2] = cv2.resize(self.original_image[2] , (width , height))
            self.fourier_transform_image()