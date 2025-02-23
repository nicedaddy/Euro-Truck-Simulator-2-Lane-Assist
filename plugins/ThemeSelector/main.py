"""
This is an example of a panel (type="static"), they will be updated if they are open.
If you need to make a plugin that is updated in the bg then check the Plugin example!
"""


from plugins.plugin import PluginInformation
from src.logger import print

PluginInfo = PluginInformation(
    name="ThemeSelector", # This needs to match the folder name under plugins (this would mean plugins\Panel\main.py)
    description="Will let you switch between themes.\nTHEMES CREATED BY rdbende!",
    version="0.1",
    author="rdbende,Tumppi066",
    url="https://github.com/Tumppi066/Euro-Truck-Simulator-2-Lane-Assist",
    type="static" # = Panel
)

import tkinter as tk
from tkinter import ttk
import src.helpers as helpers
import src.mainUI as mainUI
import src.variables as variables
import src.settings as settings
import os

SV_TTK_PATH = [variables.PATH + "plugins\\ThemeSelector\\themes\\SunValley\\sv_ttk\\sv.tcl"]
FOREST_PATH = [variables.PATH + "plugins\\ThemeSelector\\themes\\Forest\\forest-dark.tcl", variables.PATH + "plugins\\ThemeSelector\\themes\\Forest\\forest-light.tcl"]
AZURE_PATH = [variables.PATH + "plugins\\ThemeSelector\\themes\\Azure\\azure.tcl"]

themeType = settings.GetSettings("User Interface", "Theme")
if themeType == None:
    themeType = "dark"
    settings.CreateSettings("User Interface", "Theme", themeType)

# Will switch the application theme
# theme = "SunValley", "Forest", "Azure"
def ChangeTheme(theme, root, changedColor=False):
    source = ""

    if theme == "SunValley":
        source = SV_TTK_PATH[0]
    elif theme == "Forest":
        source = FOREST_PATH[0] if themeType == "dark" else FOREST_PATH[1]
    elif theme == "Azure":
        source = AZURE_PATH[0]

    try:
        root.tk.call("source", source)
    except:
        pass
    
    try:
        if theme == "Forest":
            ttk.Style().theme_use(f"forest-{themeType}")
            if changedColor:
                variables.RELOAD = True
        elif theme == "Azure":
            root.tk.call("set_theme", f"{themeType}")
        else:
            root.tk.call("sv_set_theme", f"{themeType}")
    except:
        import traceback
        traceback.print_exc()
        pass


    settings.CreateSettings("User Interface", "ColorTheme", theme)
            

def SwitchThemeType():
    global themeType
    print(themeType)
    themeType = "dark" if themeType == "light" else "light"
    ChangeTheme(settings.GetSettings("User Interface", "ColorTheme"), mainUI.root, changedColor=True)
    settings.CreateSettings("User Interface", "Theme", themeType)
    print("Switched theme type to " + themeType)

class UI():
    try: # The panel is in a try loop so that the logger can log errors if they occur
        
        def __init__(self, master) -> None:
            self.master = master # "master" is the mainUI window
            self.exampleFunction()
        
        def destroy(self):
            self.done = True
            self.root.destroy()
            del self
        
        def changeTheme(self, theme):
            if theme != settings.GetSettings("User Interface", "ColorTheme"):
                ChangeTheme(theme, self.master)
        
        def exampleFunction(self):
            
            try:
                self.root.destroy() # Load the UI each time this plugin is called
            except: pass
            
            self.root = tk.Canvas(self.master, width=600, height=520, border=0, highlightthickness=0)
            self.root.grid_propagate(0) # Don't fit the canvast to the widgets
            self.root.pack_propagate(0)
            
            # Make a dropdown for selecting the theme
            self.theme = tk.StringVar(self.root)
            theme = settings.GetSettings("User Interface", "ColorTheme")
            if theme == None:
                theme = "SunValley"
                settings.CreateSettings("User Interface", "ColorTheme", theme)
                
            self.theme.set(theme)
            self.themeSelector = ttk.OptionMenu(self.root, self.theme, theme, "SunValley", "Forest", "Azure", command=self.changeTheme(self.theme.get()))
            ttk.Label(self.root, text="Theme: ").grid(row=0, column=0)
            self.themeSelector.grid(row=0, column=1)
            
            helpers.MakeButton(self.root, "Apply", lambda: self.changeTheme(self.theme.get()), 0, 2)
            
            helpers.MakeLabel(self.root, "All themes were created by rdbende, I just changed them to work with my application.", 1, 0, columnspan=3)
            
            self.root.pack(anchor="center", expand=False)
            self.root.update()
        
        
        def update(self, data): # When the panel is open this function is called each frame 
            self.root.update()
    
    
    except Exception as ex:
        print(ex.args)