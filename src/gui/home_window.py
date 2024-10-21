from utils.variables_utils import *
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from common.common_utils import *
import matplotlib.pyplot as plt
import customtkinter as ctk


class HomeWindow(ctk.CTkFrame):
    def __init__(self,parent):
        self.parent = parent
        self.home_menu()

    def home_menu(self):
        # method to show the home window.
        
        # Clear self.workAreaFrame
        for widget in self.parent.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.parent.leftOriginalImgFrame = ctk.CTkFrame(master = self.parent.workAreaFrame)
        self.parent.rightPlotsImgFrame   = ctk.CTkFrame(master = self.parent.workAreaFrame)
        self.parent.bottomSliderFrame    = ctk.CTkFrame(master = self.parent.workAreaFrame)

        
        self.parent.leftOriginalImgFrame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        self.parent.rightPlotsImgFrame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        self.parent.bottomSliderFrame.place(rely = 0.9, y = 0, relwidth = 1, relheight = 0.1)


        self.parent.rightPlotsImgFrame.rowconfigure((0,1), weight = 1)
        self.parent.rightPlotsImgFrame.columnconfigure((0), weight = 1)
        self.parent.bottomSliderFrame.rowconfigure((0,1), weight = 1)
        self.parent.bottomSliderFrame.columnconfigure((0,1,2,3), weight = 1)
        

        
        if self.parent.start_app:
            print("first time start")
            
            if ctk.get_appearance_mode() == 'Light': 
                welcomeImg = Image.open(lightThemeImgPath)
            else:
                welcomeImg = Image.open(darkThemeImgPath)
                

            homeCanvas = ctk.CTkCanvas(self.parent.leftOriginalImgFrame, 
                            bg = rgbValues(self.parent),
                            bd = 0,
                            highlightthickness=0,
                            relief='ridge')
            
            homeCanvas.pack( expand =True, fill='both')
            homeCanvas.bind('<Configure>',lambda event: full_image(event,self.parent, welcomeImg, canvas=homeCanvas))
            self.parent.start_app = False
            self.parent.raw_img_dir == None
        
        else:
            with open(img_dir_record_path, 'r') as f:
                print("not first time start")
                self.parent.raw_img_dir = f.read().strip()
                homeCanvas = ctk.CTkCanvas(self.parent.leftOriginalImgFrame, 
                        bg = rgbValues(self.parent),
                        bd = 0,
                        highlightthickness=0,
                        relief='ridge')
        
                homeCanvas.pack(expand =True, fill='both')
                homeCanvas.bind('<Configure>',lambda event: full_image(event,self.parent , self.parent .tk_image, canvas=homeCanvas))
                homeCanvas.bind('<1>', lambda event: getresizedImageCoordinates(event,self.parent ,canvas = homeCanvas, image = self.parent.tk_image))

        print(self.parent.default_properties)
        noOfBandsEMR = self.parent.default_properties.get('noOfBandsEMR')
        
        #### wavelength plot ######
        self.parent.wavelengthPlotFig, self.parent.wavelengthPlotFigax = plt.subplots()
        self.parent.wavelengthPlotFig.set_facecolor(rgbValues(self.parent))
        self.parent.wavelengthPlotFigax.set_facecolor(rgbValues(self.parent))
        self.parent.wavelengthPlotFigax.set_title("Wavelength Plot")
        self.parent.wavelengthPlotFigax.set_xlabel("Wavelength")
        self.parent.wavelengthPlotFigax.set_ylabel("Reflectance")
        self.parent.wavelengthPlotFigCanvas = FigureCanvasTkAgg(self.parent.wavelengthPlotFig, master= self.parent.rightPlotsImgFrame)
        self.parent.wavelengthPlotFigCanvas.get_tk_widget().grid(row = 0, column = 0, sticky= 'nsew')

        #### scatter plot ######
        self.parent.scatterPlotFig, self.parent.scatterPlotFigax = plt.subplots()
        self.parent.scatterPlotFig.set_facecolor(rgbValues(self.parent))
        self.parent.scatterPlotFigax.set_facecolor(rgbValues(self.parent))
        self.parent.scatterPlotFigax.set_title("Scatter Plot")
        self.parent.scatterPlotFigax.set_xlabel("Band 1")
        self.parent.scatterPlotFigax.set_ylabel("Band 2")
        self.parent.scatterPlotFigCanvas = FigureCanvasTkAgg(self.parent.scatterPlotFig, master= self.parent.rightPlotsImgFrame)
        self.parent.scatterPlotFigCanvas.get_tk_widget().grid(row= 1, column=0,  sticky='nsew')
        
        
        # wavelength slider
        self.parent.wavelengthSliderCurrentValueLabel = ctk.CTkLabel(self.parent.bottomSliderFrame, text = "", justify ="center")
        self.parent.wavelengthSliderCurrentValueLabel.grid(row = 0, column = 0, columnspan = 2, padx = (100,5))
        self.parent.wavelengthSlider = ctk.CTkSlider(
            self.parent.bottomSliderFrame, 
            from_=0, 
            to=noOfBandsEMR-1, 
            height=20, 
            command=lambda value: wavelengthsSlider_event(self.parent.wavelengthSlider, value)
        )
        self.parent.wavelengthSlider.grid(row = 1, column = 0, columnspan=2, padx = (100,5))
        print(self.parent.raw_img_dir)
        wavelengthsSlider_event(self.parent)

        # band 1 slider
        self.parent.band1ScatterSliderCurrentValueLabel = self.parent.ctk.CTkLabel(self.parent.bottomSliderFrame, text = "", justify ="center")
        self.parent.band1ScatterSliderCurrentValueLabel.grid(row = 0, column =2, padx = (100,5))
        self.parent.band1ScatterSlider = self.parent.ctk.CTkSlider(self.parent.bottomSliderFrame, from_ = 0, to = noOfBandsEMR-1, height = 20, command = band1ScatterSlider_event)
        self.parent.band1ScatterSlider.grid(row =1, column =2, padx = (100,5))
        band1ScatterSlider_event(self.parent)

        # band 2 slider
        self.parent.band2ScatterSliderCurrentValueLabel = self.parent.ctk.CTkLabel(self.parent.bottomSliderFrame, text = "", justify ="center")
        self.parent.band2ScatterSliderCurrentValueLabel.grid(row = 0, column =3, padx = (5,100))
        self.parent.band2ScatterSlider = self.parent.ctk.CTkSlider(self.parent.bottomSliderFrame, from_ = 0, to = noOfBandsEMR-1, height = 20, command = band2ScatterSlider_event)
        self.parent.band2ScatterSlider.grid(row =1, column=3, padx=(5,100))
        band2ScatterSlider_event(self.parent)