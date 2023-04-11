# TKinter Library -------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.09.28
# Date Updated: 23.01.30
#   This module provides a standard interface for the TKinter python library. The primative objects of TKinter may be instanced
#   via Getter functions, which implement a standardized style and geometry. Custom widgets are also defined, which likewise
#   have their own Getter functions.

# Libraries -------------------------------------------------------------------------------------------------------------------
import tkinter

import json

import enum
from enum import Enum

import logging

# Objects ---------------------------------------------------------------------------------------------------------------------
class Style(dict):
    # Initialization
    def __init__(self, filePath=None):
        super().__init__()
        self.__dict__ = self
        self.overrides = dict()
        if(filePath == None):
            self.LoadDefaults()
        else:
            self.LoadJson(filePath)

    # Set Key Pair
    def Set(self, key, value):
        self[key] = value

    # Load Default Keys
    def LoadDefaults(self):
        # Font
        self.Set("font", ('Consolas', 10))
        # Colors
        self.Set("textColor",  '#000000')   # Black
        self.Set("background", '#F0F0F0')   # Light Grey
        self.Set("highlight",  '#AAAAAA')   # Grey
        self.Set("lowlight",   '#444444')   # Dark Grey
        self.Set("palette",    ['#023399']) # Blue
        # Spacing
        self.Set("padding",     4)
        self.Set("borderWidth", 1)
        # Strata
        self.Set("strataSize",  8)
        self.Set("strataGap",   2)
        self.Set("strataSlope", 0)

    # Load from JSON File
    def LoadJson(self, filePath):
        file = open(filePath)
        data = json.load(file)
        for key, item in data.items():
            if(key.__contains__("font")):
                self.Set(key, (item["font"], item["size"]))
            else:
                self.Set(key, item)

    # Insert Override
    # - Call to temporarily overide a Key Pair
    def InsertOverride(self, key1, key2):
        self.overrides[key1] = self[key1]
        self[key1] = self[key2]

    # Remove Override
    # - Call to revert a Key Pair
    def RemoveOverride(self, key1):
        self[key1] = self.overrides[key1]
        self.overrides.pop(key1)

    # Insert Overrides
    # - Call to temporarily overide a List of Key Pairs
    def InsertOverrides(self, overrides):
        for key1, key2 in overrides:
            self.InsertOverride(key1, key2)

    # Call to revert a List of Key Pairs
    def RemoveOverrides(self, overrides):
        for key1, key2 in overrides:
            self.RemoveOverride(key1)

# Enumerables -----------------------------------------------------------------------------------------------------------------
class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL   = 1

# Getters ---------------------------------------------------------------------------------------------------------------------------
# Get Frame
# - Call to Get and Grid a Frame Object
# - Use Border to Enable a Border and Padding
def GetFrame(parent, style, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", border=False, styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        frame = tkinter.Frame(parent, background=style['background'])
        padding = 0
        if(border):
            padding = style["padding"]
            frame = tkinter.Frame(parent, background=style["background"], highlightbackground=style["highlight"], padx=padding, pady=padding, highlightthickness=int(style["borderWidth"]))        
        if(grid):
            frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=padding, pady=padding)
        style.RemoveOverrides(styleOverrides)
        return frame
    except Exception as e:
        logging.error("lib_tkinter.GetFrame() call failed: " + str(e))
        raise

# Get Label Frame
# - Call to Get and Grid a Label Frame Object
# - Use Border to Enable a Border and Padding
def GetLabelFrame(parent, style, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", label="", border=False, styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        frame = tkinter.LabelFrame(parent, text=label, bg=style["background"], fg=style["textColor"], font=style["font"])
        if(border):
            frame = tkinter.LabelFrame(parent, text=label, bg=style["background"], fg=style["textColor"], font=style["font"], padx=int(style["padding"]), pady=int(style["padding"]), bd=int(style["borderWidth"]))        
        if(grid):
            frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return frame
    except Exception as e:
        logging.error("lib_tkinter.GetLabelFrame() call failed: " + str(e))
        raise

# Get Canvas
# - Call to Get and Grid a Canvas Object
# - Use Border to Enable a Border and Padding
# - Width and Height behave as minimum values
def GetCanvas(parent, style, width, height, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", border=False, styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        canvas = tkinter.Canvas(parent, width=int(width), height=int(height), background=style["background"], highlightthickness=0)
        if(border):
            canvas = tkinter.Canvas(parent, width=int(width), height=int(height), background=style["background"], highlightbackground=style["highlight"], highlightthickness=int(style["borderWidth"]))
        if(grid):
            canvas.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return canvas
    except Exception as e:
        logging.error("lib_tkinter.GetCanvas() call failed: " + str(e))
        raise

# Get Divider
# - Call to Get and Grid a Divider Styled Canvas Object
# - Use Orientation to indicate direction
def GetDivider(parent, style, orientation, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        frame = tkinter.Frame(parent)
        if(orientation == Orientation.HORIZONTAL):
            divider = tkinter.Canvas(frame, width=2, height=int(style["borderWidth"]), background=style["highlight"], highlightthickness=0)
            divider.pack(fill="both", expand=True)
        if(orientation == Orientation.VERTICAL):
            divider = tkinter.Canvas(parent, width=int(style["borderWidth"]), height=2, background=style["highlight"], highlightthickness=0)
            divider.pack(fill="both", expand=True)
        if(grid):
            frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return frame
    except Exception as e:
        logging.error("lib_tkinter.GetDivider() call failed: " + str(e))
        raise

# Get Label
# - Call to Get and Grid a Label Object
def GetLabel(parent, style, text="", grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        label = tkinter.Label(parent, font=style["font"], text=text, foreground=style["textColor"], background=style["background"])
        if(grid):
            label.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return label
    except Exception as e:
        logging.error("lib_tkinter.GetLabel() call failed: " + str(e))
        raise

# Get Button
# - Call to Get and Grid a Button Object
# - Use Command to provide Functionality
def GetButton(parent, style, command="", text="", grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        button = tkinter.Button(parent, command=command, text=text, font=style["font"], foreground=style["textColor"], background=style["background"])
        if(grid): button.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return button
    except Exception as e:
        logging.error("lib_tkinter.GetButton() call failed: " + str(e))
        raise

# Get Image Button
# - Call to Get and Grid a Button Object
# - Returns a Tuple of Button Object and PhotoImage
# - Do not discard PhotoImage, Garbage Collector will deallocate memory
# - Use Image Sampling to indicate a size
def GetImageButton(parent, style, command="", image="", imageSampling=(1,1), grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
    
        tkinterImage = tkinter.PhotoImage(file=image)
        if(imageSampling[0] < 1):
            tkinterImage = tkinterImage.subsample(int(1/imageSampling[0]), 1)
        else:
            tkinterImage = tkinterImage.zoom(int(imageSampling[0]), 1)
        if(imageSampling[1] < 1):
            tkinterImage = tkinterImage.subsample(1, int(1/imageSampling[1]))
        else:
            tkinterImage = tkinterImage.zoom(1, int(imageSampling[1]))

        button = tkinter.Button(parent, command=command, image=tkinterImage, foreground=style["textColor"], background=style["background"])
        if(grid): button.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return (button, tkinterImage)
    except Exception as e:
        logging.error("lib_tkinter.GetImageButton() call failed: " + str(e))
        raise

# Get Radio Button
# - Call to Get and Grid a Radio Button Object
# - Use Variable for Functionality
def GetRadiobutton(parent, style, value="", variable="", text="", grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky=""):
    try:
        button = tkinter.Radiobutton(parent, variable=variable, value=value, text=text, font=style["font"], foreground=style["textColor"], background=style["background"])
        if(grid): button.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        return button
    except Exception as e:
        logging.error("lib_tkinter.GetRadioButton() call failed: " + str(e))
        raise

# Get Entry
# - Call to Get and Grid an Entry Object
# - Use Variable for Functionality
def GetEntry(parent, style, minWidth, variable=None, value="", grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky=""):
    try:
        entry = tkinter.Entry(parent, textvariable=variable, width=minWidth, font=style["font"], foreground=style["textColor"], bg=style["background"])
        entry.insert(0,str(value))
        if(grid): entry.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        return entry
    except Exception as e:
        logging.error("lib_tkinter.GetEntry() call failed: " + str(e))
        raise

# Get Check Button
# - Call to Get and Grid a Check Button Object
# - Use Variable for Functionality
def GetCheckbutton(parent, style, variable, text="", grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky=""):
    try:
        button = tkinter.Checkbutton(parent, variable=variable, text=text, font=style["font"], foreground=style["textColor"], background=style["background"])
        if(grid): button.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        return button
    except Exception as e:
        logging.error("lib_tkinter.GetCheckButton() call failed: " + str(e))
        raise

# Get Progress Bar
# - Call to Get and Grid a Progress Bar Object
# - Use Orientation for Direction
# - Refer to Progress Bar Object for Info
def GetProgressBar(parent, style, orientation, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", minWidth=20, minHeight=20, gridPadding=0, scaleFactor=1, offset=0, label="", border=False, styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        bar = ProgressBar(parent, orientation, minWidth=minWidth, minHeight=minHeight, scaleFactor=scaleFactor, offset=offset, label=label, background=style["background"], outline='#000000', foreground=style["lowlight"], font=style["font"], textColor=style["textColor"], borderWidth=0)
        if(border):
            bar = ProgressBar(parent, orientation, minWidth=minWidth, minHeight=minHeight, scaleFactor=scaleFactor, offset=offset, label=label, background=style["background"], outline=style["highlight"], foreground=style["lowlight"], font=style["font"], textColor=style["textColor"], borderWidth=style["borderWidth"])
        if(grid):
            bar.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=gridPadding, pady=gridPadding)
        style.RemoveOverrides(styleOverrides)
        return bar
    except Exception as e:
        logging.error("lib_tkinter.GetProgressBar() call failed: " + str(e))
        raise

# Get Stratafied Bar
# - Call to Get and Grid a Stratafied Bar Object
# - Use Orientation for Direction
# - Refer to Stratafied Bar Object for Info
def GetStrataBar(parent, style, orientation, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", minWidth=20, minHeight=20, scaleFactor=1, offset=0, border=False, highlights=["#023399"], lowlights=["#F0F0F0"], domain=[1], mask=[], styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        bar = StratifiedBar(parent, orientation, minWidth=minWidth, minHeight=minHeight, scaleFactor=scaleFactor, offset=offset, background=style["background"], highlights=highlights, lowlights=lowlights, domain=domain, strataSize=style["strataSize"], strataGap=style["strataGap"], borderWidth=0)
        if(border):
            bar = StratifiedBar(parent, orientation, minWidth=minWidth, minHeight=minHeight, scaleFactor=scaleFactor, offset=offset, background=style["background"], highlights=highlights, lowlights=lowlights, domain=domain, strataSize=style["strataSize"], borderWidth=style["borderWidth"], borderColor=style["highlight"])
        
        bar.ShearStrata(style["strataSlope"])
        if(len(mask) >= 2):
            bar.MaskStrata(mask[0], mask[1], *mask[2:])
        
        if(grid):
            bar.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return bar
    except Exception as e:
        logging.error("lib_tkinter.GetStrataBar() call failed: " + str(e))
        raise

# Get Button Bar
# - Call to Get and Grid a Button Bar Object
# - Use Orientation for Direction
# - Use Command List size to indicate Button Count
# - Command and Label lists must match size
# - Refer to Button Bar Object for Info
def GetButtonBar(parent, style, orientation, commands, labels=[], grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", minWidth=20, minHeight=20, border=False, styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        bar = ButtonBar(parent, orientation, commands, minWidth=minWidth, minHeight=minHeight, labels=labels, background=style["background"], borderColor='#000000', font=style["font"], fontColor=style["textColor"], borderWidth=0)
        if(border):
            bar = ButtonBar(parent, orientation, commands, minWidth=minWidth, minHeight=minHeight, labels=labels, background=style["background"], borderColor=style["highlight"], font=style["font"], fontColor=style["textColor"], borderWidth=style["borderWidth"])
        if(grid):
            bar.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return bar
    except Exception as e:
        logging.error("lib_tkinter.GetButtonBar() call failed: " + str(e))
        raise

# Get Label Stat
# - Call to Get and Grid a Label Stat Object
# - Use Precision for numerics
# - Use Font Color list and Domain for advanced Coloring
# - Refer to Label Stat Object for Info
def GetLabelStat(parent, style, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", precision=0, fontColors=None, domain=[1], styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        if(fontColors == None):
            fontColors = [style["textColor"]]
        label = LabelStat(parent, precision=precision, fontColors=fontColors, background=style["background"], domain=domain, font=style["font"])
        if(grid):
            label.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return label
    except Exception as e:
        logging.error("lib_tkinter.GetLabelStat() call failed: " + str(e))
        raise

# Get Check Stat
# - Call to Get and Grid a Check Stat Object
# - Use Inverted to invert Checks and X's
# - Refer to Check Stat Object for Info
def GetCheckStat(parent, style, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", inverted=False, styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        stat = CheckStat(parent, inverted=inverted, foreground=style["textColor"], background=style["background"], font=style["font"])
        if(grid):
            stat.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return stat
    except Exception as e:
        logging.error("lib_tkinter.GetCheckStat() call failed: " + str(e))
        raise

# Get Scroll Frame
# - Call to Get and Grid a Scroll Frame Object
# - Use Orientation for Scroll Direction
# - Refer to Scroll Frame Object for Info
def GetScrollFrame(parent, style, orientation, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", styleOverrides=[]):
    try:
        style.InsertOverrides(styleOverrides)
        frame = ScrollFrame(parent, orientation=orientation, background=style["background"], highlight=style["highlight"])
        if(grid):
            frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        style.RemoveOverrides(styleOverrides)
        return frame
    except Exception as e:
        logging.error("lib_tkinter.GetScrollFrame() call failed: " + str(e))
        raise

# Widgets ---------------------------------------------------------------------------------------------------------------------------
# Progress Bar
# - Use this widget as a progress bar object
# - Use Scale Factor and Offset for Displaying non-percentages
class ProgressBar(tkinter.Canvas):
    def __init__(self, parent, orientation, minWidth=20, minHeight=20, scaleFactor=1, offset=0, label="", background='#F0F0F0', outline='#AAAAAA', foreground='#444444', font=("consolas", 10), textColor="#000000", borderWidth=1):
        # Initialize Variables
        self.width       = minWidth
        self.height      = minHeight
        self.scaleFactor = scaleFactor
        self.offset      = offset
        self.orientation = orientation
        self.value       = None
        
        # Root
        super().__init__(parent, width=self.width, height=self.height, background=background, highlightthickness=borderWidth, highlightbackground=outline)
        self.bar   = self.create_rectangle(0, 0, self.width, self.height, fill=foreground, width=0)
        self.label = self.create_text(0, 0, fill=textColor, font=font, text=self.FormatText(label))

        # Interrupts
        self.bind("<Configure>", self.Redraw)

    def Redraw(self, event):
        self.width  = event.width
        self.height = event.height
        self.RedrawBar()
        self.RedrawLabel()

    def RedrawBar(self):
        if(self.orientation == Orientation.VERTICAL):
            self.coords(self.bar, 0, self.height, self.width, self.height * (1-self.GetPercent()))
        if(self.orientation == Orientation.HORIZONTAL):
            self.coords(self.bar, 0, 0, self.width * self.GetPercent(), self.height)

    def RedrawLabel(self):
        self.coords(self.label, self.width / 2, self.height / 2)

    def FormatText(self, text):
        if(len(text) <= 1): return text
        if(self.orientation == Orientation.HORIZONTAL): return text
        if(self.orientation == Orientation.VERTICAL):
            output = ""
            for index in range(len(text) - 1):
                output += text[index] + '\n'
            output += text[len(text) - 1]
            return output
        return ""

    def GetPercent(self):
        if(self.value == None): return 0
        return (self.value - self.offset) / self.scaleFactor

    def Set(self, value):
        if(value == None): return
        self.value = value
        self.RedrawBar()

    def Get(self):
        return self.value

# Statafied Bar
# - Use this widget as a stylized progress bar
# - Use Highlight and Lowlight Lists for coloring sections
# - Use Scale Factor and Offset for Displaying non-percentages
class StratifiedBar(tkinter.Canvas):
    def __init__(self, parent, orientation, minWidth=20, minHeight=20, scaleFactor=1, offset=0, background='#F0F0F0', highlights = ['#023399'], lowlights = ['#F0F0F0'], domain = [1], strataSize = 8, strataGap = 2, borderWidth = 1, borderColor='#AAAAAA'):
        # Initialize Variables
        self.width            = minWidth
        self.height           = minHeight
        self.scaleFactor      = scaleFactor
        self.offset           = offset
        self.orientation      = orientation
        self.strataSize       = strataSize
        self.strataGap        = strataGap
        self.strata           = []
        self.mask             = None
        self.maskX0           = None
        self.maskY0           = None
        self.maskCoords       = None
        self.strataSlope      = 0
        self.strataCount      = 0
        self.background       = background
        self.domain           = domain
        self.highlights       = highlights
        self.lowlights        = lowlights
        self.value            = None

        # Root
        super().__init__(parent, width=self.width, height=self.height, bg=background, highlightthickness=borderWidth, highlightbackground=borderColor)

        # Interrupts
        self.bind("<Configure>", self.Redraw)

    def Redraw(self, event):
        self.width  = event.width
        self.height = event.height
        self.RedrawStrata()
        self.RedrawMask()

    def RedrawStrata(self):
        if(self.orientation == Orientation.VERTICAL):
            return
        if(self.orientation == Orientation.HORIZONTAL):
            self.strataCount = 0
            cumulativeWidth = 0
            
            while(True):
                if(self.strataCount != 0):
                    cumulativeWidth += self.strataGap
                cumulativeWidth += self.strataSize 
                if(cumulativeWidth < self.width):
                    self.strataCount += 1
                else:
                    cumulativeWidth -= self.strataGap
                    cumulativeWidth -= self.strataSize
                    break
            
            self.strataOffset = int((self.width - cumulativeWidth) / 2)

        for stratum in self.strata:
            self.delete(stratum)
        self.strata = []

        self.ShearStrata(self.strataSlope)
        self.GenerateStrataPalette()
        
        for stratumIndex in range(self.strataCount):
            self.RedrawStratum(stratumIndex)

    def RedrawStratum(self, index):
        if(self.orientation == Orientation.VERTICAL):
            return
        if(self.orientation == Orientation.HORIZONTAL):
            x0 = index * (self.strataSize + self.strataGap) + self.strataOffset + self.strataSlope * self.height
            y0 = 0
            x1 = x0 + self.strataSize
            y1 = y0
            x2 = x1 - self.strataSlope * self.height
            y2 = self.height
            x3 = x0 - self.strataSlope * self.height
            y3 = y2
            stratum = self.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3)
            self.strata.append(stratum)
        self.ColorStratum(index)

    def ColorStratum(self, index):
        stratumPercent = index / self.strataCount
        if(stratumPercent < self.GetPercent()):
            self.itemconfigure(self.strata[index], fill=self.strataHighlights[index])
        else:
            self.itemconfigure(self.strata[index], fill=self.strataLowlights[index])

    def GenerateStrataPalette(self):
        self.strataHighlights = []
        self.strataLowlights  = []
        for strataIndex in range(self.strataCount):
            for domainIndex in range(len(self.domain)):
                normalizedDomain = (self.domain[domainIndex] - self.offset) / self.scaleFactor
                if(strataIndex / self.strataCount < normalizedDomain):
                    self.strataHighlights.append(self.highlights[domainIndex])
                    self.strataLowlights.append(self.lowlights[domainIndex])
                    break

    def Set(self, value):
        if(value == None): return
        self.value = value

    def GetPercent(self):
        if(self.value == None): return 0
        return (self.value - self.offset) / self.scaleFactor

    def Get(self):
        return self.value

    def ShearStrata(self, slope):
        if(slope == 0): return
        self.strataSlope = slope
        if(self.orientation == Orientation.HORIZONTAL):
            strataLossCount = int(slope * self.height / (self.strataSize + self.strataGap)) + 1
            if(strataLossCount >= self.strataCount):
                self.strataCount = 0
            else:
                self.strataCount -= strataLossCount

    def MaskStrata(self, x0, y0, *xyCoords):
        self.maskX0 = x0
        self.maskY0 = y0
        self.maskCoords = xyCoords
        self.mask = self.create_polygon(0, 0)
        self.RedrawMask()

    def RedrawMask(self):
        if(self.maskX0 == None or self.maskY0 == None): return

        x0 = self.maskX0 * self.width
        y0 = self.maskY0 * self.height

        xyCoords = []
        for index in range(len(self.maskCoords)):
            if(index & 2 == 0): # X
                xyCoords.append(self.maskCoords[index] * self.width)
            else: # Y
                xyCoords.append(self.maskCoords[index] * self.height)

        self.delete(self.mask)
        self.mask = self.create_polygon(x0, y0, xyCoords, fill=self.background)

# Button Bar
# - Use this widget as a list of Button Objects 
# - Command List to indicate the number of Buttons to create
# - If using Label List, it must be of same length as Command List
class ButtonBar(tkinter.Frame):
    def __init__(self, parent, orientation, commands, minWidth=20, minHeight=20, labels=[], background="#F0F0F0", fontColor="#000000", font=("consolas", 10), borderColor="#444444", borderWidth=1):
        # Root Instantiation
        super().__init__(parent, background=background, width=minWidth, height=minHeight, highlightthickness=borderWidth, highlightcolor=borderColor)
        
        # Root Partitioning
        buttonCount = len(commands)
            
        # Button Data
        buttons = [None] * buttonCount
        if(labels == []):
            labels = [""] * buttonCount
            
        # Root Widgets
        for index in range(buttonCount):
            if(orientation == Orientation.HORIZONTAL):
                self.columnconfigure(index, weight=1)
                container = tkinter.Frame(self, height=minHeight, background=background, highlightbackground=borderColor, highlightthickness=borderWidth)
                container.pack_propagate(0)
                container.grid(column=index, row=0, sticky="NESW")
                buttons[index] = tkinter.Button(container, command=commands[index], text=labels[index], font=font, foreground=fontColor, background=background, highlightbackground=borderColor, highlightthickness=borderWidth)
                buttons[index].pack(expand=True, fill="both")
            if(orientation == Orientation.VERTICAL):
                self.rowconfigure(index, weight=1)
                container = tkinter.Frame(self, width=minWidth, background=background, highlightbackground=borderColor, highlightthickness=borderWidth)
                container.pack_propagate(0)
                container.grid(column=0, row=index, sticky="NESW")
                buttons[index] = tkinter.Button(container, command=commands[index], text=labels[index], font=font, foreground=fontColor, background=background, highlightbackground=borderColor, highlightthickness=borderWidth)
                buttons[index].pack(expand=True, fill="both")

# Label Stat
# - Use this widget as a Label for a Statistic
# - Use Precision for floating-point variables
# - Use Font Color List with Domain List to modify Coloring
class LabelStat(tkinter.Label):
    def __init__(self, parent, precision=0, fontColors=['#023399'], background='#F0F0F0', domain=[1], font=("consolas", 10)):
        super().__init__(parent, font=font, foreground=fontColors[0], background=background,  text="--")
        self.precision   = precision
        self.fontColors  = fontColors
        self.domain      = domain
        self.value       = None

    def Set(self, value):
        self.value = value
        self.Update()

    def Update(self):
        self['text'] = self.GetText()
        self['fg']   = self.GetColor(self.fontColors, self.domain)
        
    def GetText(self):
        if(self.value == None): return "--"
        if(type(self.value) == type(0) or type(self.value) == type(0.0)):
            if(self.precision == 0): return str(int(self.value))
            return (f'%.{self.precision}f' % self.value)
        if(type(self.value == type(""))):
            return self.value

    def GetColor(self, palette, domain):
        if(self.value == None): return palette[0]
        if(len(palette) == 1):  return palette[0]
        for index in range(len(domain)):
            if(self.value < domain[index]):
                return palette[index]
        return palette[len(palette) - 1]

# Check Stat
# - Use this widget as a Check/X Stat
# - Default True = Check, False - X
# - Use Invert to swap values
class CheckStat(tkinter.Label):
    def __init__(self, parent, inverted=False, background = '#F0F0F0', foreground='#000000', font=("consolas", 10)):
        super().__init__(parent, background=background, foreground=foreground, font=font, text="-")
        self.value    = None
        self.inverted = inverted

    def Set(self, value):
        self.value = value
        self.Update()

    def Update(self):
        self['text'] = self.GetText()
        
    def GetText(self):
        if(self.value == None): return "-"
        if(self.value and not self.inverted): return '\u2713'
        if(not self.value and self.inverted): return '\u2713'
        return 'X'

# Scroll Frame
# - Use this widget as a Frame with a Scroll Bar
# - Use Orientation to indicate a Scrolling Direction
class ScrollFrame(tkinter.Frame):
    def __init__(self, parent, orientation, background="#F0F0F0", highlight="#AAAAAA"):
        super().__init__(parent, background=background, highlightthickness=0)

        self.orientation = orientation

        if(orientation == Orientation.VERTICAL):
            self.scrollbar = tkinter.Scrollbar(self, orient="vertical", background=background, highlightcolor=highlight)
            self.scrollbar.pack(fill="y", side="right", expand=False)
        
            self.canvas = tkinter.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.scrollbar.set, background=background, highlightcolor=highlight)
            self.canvas.pack(side="left", fill="both", expand=True)
        
            self.scrollbar.config(command=self.canvas.yview)
        if(orientation == Orientation.HORIZONTAL):
            self.scrollbar = tkinter.Scrollbar(self, orient="horizontal", background=background, highlightcolor=highlight)
            self.scrollbar.pack(fill="x", side="bottom", expand=False)
        
            self.canvas = tkinter.Canvas(self, bd=0, highlightthickness=0, xscrollcommand=self.scrollbar.set, background=background, highlightcolor=highlight)
            self.canvas.pack(side="top", fill="both", expand=True)
        
            self.scrollbar.config(command=self.canvas.xview)

        self.offset = 0
        self.offsetPrime = 0
        self.scrollPosition = 1
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.canvasSize = 100

        self.frame  = tkinter.Frame(self.canvas, background=background, highlightcolor=highlight)
        self.frameWindow = self.canvas.create_window(0, 0, window=self.frame, anchor="nw")

        self.frame.bind('<Configure>', self.RedrawFrame)

        self.canvas.bind('<Configure>', self.RedrawCanvas)

        self.bind("<Enter>", lambda _: self.bind_all('<Button-1>', self.OnPress), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<Button-1>'), '+')
        self.bind("<Enter>", lambda _: self.bind_all('<B1-Motion>', self.OnTouchScroll), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<B1-Motion>'), '+')

    def RedrawFrame(self, event):
        width  = self.frame.winfo_reqwidth()
        height = self.frame.winfo_reqheight()
        self.canvas.config(scrollregion=(0, 0, width, height))
        if(self.orientation == Orientation.VERTICAL and width != self.canvas.winfo_width()):
            self.canvas.config(width=width)
        if(self.orientation == Orientation.HORIZONTAL and height != self.canvas.winfo_height()):
            self.canvas.config(height=height)

    def RedrawCanvas(self, event):
        if(self.orientation == Orientation.VERTICAL and self.frame.winfo_reqwidth() != self.canvas.winfo_width()):
            self.canvas.itemconfigure(self.frameWindow, width=self.canvas.winfo_width())
            self.canvasSize = self.canvas.winfo_height()
        if(self.orientation == Orientation.HORIZONTAL and self.frame.winfo_reqheight() != self.canvas.winfo_height()):
            self.canvas.itemconfigure(self.frameWindow, height=self.canvas.winfo_height())
            self.canvasSize = self.canvas.winfo_width()

    def OnPress(self, event):
        if(self.orientation == Orientation.VERTICAL):
            self.offset = event.y_root
            
            if(self.scrollPosition < 1):
                self.scrollPosition = 1

            canvasHeight = self.canvasSize
            if(self.scrollPosition > canvasHeight):
                self.scrollPosition = canvasHeight

            self.canvas.yview_moveto(self.scrollPosition / canvasHeight)

        if(self.orientation == Orientation.HORIZONTAL):
            self.offset = event.x_root
            
            canvasWidth = self.canvasSize
            if(self.scrollPosition < 1):
                self.scrollPosition = 1
            if(self.scrollPosition > canvasWidth):
                self.scrollPosition = canvasWidth

            self.canvas.xview_moveto(self.scrollPosition / canvasWidth)

    def OnTouchScroll(self, event):
        if(self.orientation == Orientation.VERTICAL):
            offsetCurrent = event.y_root
        if(self.orientation == Orientation.HORIZONTAL):
            offsetCurrent = event.y_root

        sectionStep = 4
        if(offsetCurrent > self.offsetPrime):
            event.delta = -sectionStep
        elif(offsetCurrent < self.offsetPrime):
            event.delta = sectionStep
        else:
            event.delta = 0
        self.offsetPrime= offsetCurrent
        self.scrollPosition += event.delta

        if(self.orientation == Orientation.VERTICAL):
            self.canvas.yview_moveto(self.scrollPosition / self.canvasSize)
        if(self.orientation == Orientation.HORIZONTAL):
            self.canvas.xview_moveto(self.scrollPosition / self.canvasSize)

    def Get(self):
        return self.frame
