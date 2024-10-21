#####################################################################################
## Author: Billy G. Ram
## Refactored BY: Sunil GC
## Linkedin: https://www.linkedin.com/in/billygrahamram/
## Twitter: https://twitter.com/billygrahamram
## Github: https://github.com/billygrahamram
## This code solely belongs to Billy G. Ram and is currently NOT open sourced. 
#####################################################################################

import customtkinter as ctk
from utils.config_parser import *
from gui.main_menu import *
from gui.home_window import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_properties =  parse_properties('resources/config/default_config.property')
        self.raw_img_dir = None
        self.Dataloaded = False
        self.start_app = True
        self.ctk = ctk

        # Empty the img_dir_record.txt file at startup. Opens and closes it, making the file empty.
        with open(img_dir_record_path, 'w') as f:
            pass

         ## children to main window
        self.menuBarFrame = ctk.CTkFrame(self)
        self.workAreaFrame = ctk.CTkFrame(self)

        self.menuBarFrame.place(x=0, y=0, relwidth = 1, relheight = 0.05)
        self.workAreaFrame.place(rely = 0.05, y =0, relwidth =1, relheight =0.95)

        # set default values
        self.band1Value = 150
        self.band2Value = 150

        main_menu_obj = MainMenu(self)
        
        hw_menu_obj = HomeWindow(self)

    

