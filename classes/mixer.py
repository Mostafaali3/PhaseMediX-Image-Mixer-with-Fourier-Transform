from classes.customImage import CustomImage
from classes.modesEnum import Mode , RegionMode
import time
import numpy as np
import logging
class Mixer():
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.progress_value = 0
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
        self.logger.info(f"Changing mode from {self.__current_mode} to {new_mode}.")
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
        
    def get_region_image(self, image_number, region_mode, boundaries):
        region_image = self.images_list[image_number].modified_image_fourier_components
        print(type(region_image))
        if region_mode != RegionMode.FULL:
            print(boundaries)
            left, top, right, bottom = boundaries  # Unpack boundaries
            
        if region_mode == RegionMode.INNER:
            # Correct slicing for the inner region
            region_image = region_image[top:bottom+1, left:right+1]
        elif region_mode == RegionMode.OUTER:
            # Correct slices for outer regions
            left_region = region_image[top:bottom+1, :left]
            right_region = region_image[top:bottom+1, right+1:]
            top_region = region_image[:top, :]
            bottom_region = region_image[bottom+1:, :]

            # Combine outer regions
            top_bottom_region = np.vstack((top_region, bottom_region))
            inner_zero_padding = np.zeros((bottom - top + 1, right - left + 1))
            left_right_region = np.hstack((left_region, inner_zero_padding, right_region))
            region_image = np.vstack((top_bottom_region, left_right_region))
        print(f'region {region_image.shape}')
        return region_image
    
    def mix(self, weights , boundaries , region_mode):
        print(f'images {len(self.images_list)}')
        for image in self.images_list:
            print(image.loaded)
        resulted_mix_magnitude = 0
        resulted_mix_phase = 0
        resulted_mix_real = 0
        resulted_mix_imag = 0
        if (self.current_mode == Mode.MAGNITUDE_PHASE):
            weighted_images_magnitudes = []
            weighted_images_phases = []
            for image_number in range(len(self.images_list)):
                if(self.images_list[image_number].loaded == False ):
                    continue
                
                region_image = self.get_region_image(image_number , region_mode ,boundaries )
                print(f'image {region_image.shape}')
                image_magnitude = np.abs(region_image)
                image_phase = np.angle(region_image)
                
                if(self.images_modes[image_number] == Mode.MAGNITUDE):
                    weighted_image_magnitude = image_magnitude * weights[image_number]
                    weighted_images_magnitudes.append(weighted_image_magnitude)
                    # weighted_images_phases.append(image_phase)
                    
                if(self.images_modes[image_number] == Mode.PHASE):
                    weighted_image_phase = image_phase * weights[image_number]
                    weighted_images_phases.append(weighted_image_phase)
                    # weighted_images_magnitudes.append(image_magnitude)

            for weighted_mag in weighted_images_magnitudes:
                resulted_mix_magnitude += weighted_mag
            for weighted_phase in weighted_images_phases:
                resulted_mix_phase += weighted_phase
            resulted_mix_complex =  resulted_mix_magnitude * np.exp(1j * resulted_mix_phase) 

            
        elif (self.current_mode == Mode.REAL_IMAGINARY):
            weighted_images_real_parts = []
            weighted_images_imaginary_parts = []
            for image_number in range(len(self.images_list)):
                if(self.images_list[image_number].loaded == False ):
                    continue
                
                region_image = self.get_region_image(image_number , region_mode ,boundaries )

                image_real = np.real(region_image)
                image_imag = np.imag(region_image)
                
                if(self.images_modes[image_number] == Mode.REAL):
                    weighted_image_real = image_real * weights[image_number]
                    weighted_images_real_parts.append(weighted_image_real)
                    # weighted_images_phases.append(image_phase)
                    
                if(self.images_modes[image_number] == Mode.PHASE):
                    weighted_image_imag = image_imag * weights[image_number]
                    weighted_images_imaginary_parts.append(weighted_image_imag)
                    # weighted_images_magnitudes.append(image_magnitude)

            for weighted_real in weighted_images_real_parts:
                resulted_mix_real += weighted_real
            for weighted_imag in weighted_images_imaginary_parts:
                resulted_mix_imag += weighted_imag
            resulted_mix_complex = resulted_mix_real + 1j * resulted_mix_imag
            
        resulted_inversed_image = np.fft.ifft2(np.fft.ifftshift(resulted_mix_complex))
        resulted_image_real = resulted_inversed_image.real
        return resulted_image_real
    
