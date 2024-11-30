from classes.mixer import Mixer

class Controller():
    def __init__(self, list_of_iamges,list_of_image_viewers,list_of_component_viewers):
        self.list_of_images = list_of_iamges
        self.list_of_image_viewers = list_of_image_viewers
        self.list_of_component_viewers = list_of_component_viewers
        self.Mixer = Mixer()
        self.result_image_1 = None #custom image
        self.result_image_2 = None #custom image
        
    def set_current_images_list(self):
        pass
    
    def mix_all(self, output_viewer_number:int):
        pass