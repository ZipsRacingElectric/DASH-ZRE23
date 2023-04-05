# GUI BMS View ----------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.19
# Date Updated: 23.01.30
#   This module contains all objects relating to the BMS View of the GUI. The View object may be instanced to create a view
#   for displaying Accumulator information.

# Libraries -------------------------------------------------------------------------------------------------------------------
import tkinter
import lib_tkinter
from lib_tkinter import Orientation

import logging

# Includes --------------------------------------------------------------------------------------------------------------------
import gui

# Constants -------------------------------------------------------------------------------------------------------------------
CELL_WIDTH_COUNT  = 18
CELL_HEIGHT_COUNT = 5

TEMP_WIDTH_COUNT = 9
TEMP_HEIGHT_COUNT = 5

# View Object -----------------------------------------------------------------------------------------------------------------
class View(gui.View):
    # Initialization
    def __init__(self, parent, id, style, database):
        # Root --------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, database)

        # Partitioning
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure   (0, weight=0)
        self.root.rowconfigure   (1, weight=1)
        self.root.rowconfigure   (2, weight=0)

        # Widgets
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.SetViewType("Cell"),
                          lambda: self.SetViewType("Voltage"),
                          lambda: self.SetViewType("Temperature"),
                          lambda: self.SetViewType("Delta")]
        buttonLabels   = ["Back",
                        "Overview",
                        "Voltages",
                        "Temps",
                        "Deltas"]

        self.statPanel   = lib_tkinter.GetFrame    (self.root, style=style, column=0, row=0, sticky="EW")
        self.cellPanel   = lib_tkinter.GetFrame    (self.root, style=style, column=0, row=1, sticky="EW")
        self.buttonPanel = lib_tkinter.GetButtonBar(self.root, style=style, column=0, row=2, sticky="EW", minHeight=style["buttonBarHeight"],
                                                    orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        # Cell Panel --------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.cellPanel.columnconfigure(0,                  weight=1) # Padding
        self.cellPanel.columnconfigure(CELL_WIDTH_COUNT+1, weight=1) # Padding
        # Widgets
        self.cellStats = [None]*(CELL_WIDTH_COUNT*CELL_HEIGHT_COUNT)
        for x in range(CELL_WIDTH_COUNT):
            for y in range(CELL_HEIGHT_COUNT):
                index = x + y*CELL_WIDTH_COUNT
                self.cellPanel.columnconfigure(x+1, minsize=style["bmsStatSize"]+2)
                self.cellPanel.rowconfigure   (y+1, minsize=style["bmsStatSize"]+2)
                self.cellStats[index] = GetCellStat(self.cellPanel, style=style, minWidth=style["bmsStatSize"], minHeight=style["bmsStatSize"],
                                                    column=x+1, row=y, styleOverrides=[("font", "fontBare")])

        # Stat Panel --------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.statPanel.columnconfigure(0, weight=1)
        self.statPanel.columnconfigure(1, weight=1)
        self.statPanel.columnconfigure(2, weight=1)
        self.statPanel.columnconfigure(3, weight=1)
        self.statPanel.columnconfigure(4, weight=1)
        self.statPanel.columnconfigure(5, weight=1)
        self.statPanel.rowconfigure   (0, minsize=style["bmsTextHeight"])
        self.statPanel.rowconfigure   (1, minsize=style["bmsTextHeight"])
        self.statPanel.rowconfigure   (2, minsize=style["bmsTextHeight"])
        self.statPanel.rowconfigure   (3, minsize=style["bmsTextHeight"])
        self.statPanel.rowconfigure   (4, minsize=style["bmsTextHeight"])
        # Widgets
        # Column 1
        canStatusLabel        = lib_tkinter.GetLabel    (self.statPanel, column=0, row=0, sticky="E", text="CAN Status:",    style=style)
        selfTestLabel         = lib_tkinter.GetLabel    (self.statPanel, column=0, row=1, sticky="E", text="Self-Test:",     style=style)
        voltageTestLabel      = lib_tkinter.GetLabel    (self.statPanel, column=0, row=2, sticky="E", text="Voltages:",      style=style)
        tempTestLabel         = lib_tkinter.GetLabel    (self.statPanel, column=0, row=3, sticky="E", text="Temperatures:",  style=style)
        senseTestLabel        = lib_tkinter.GetLabel    (self.statPanel, column=0, row=4, sticky="E", text="Sense Lines:",   style=style)
        self.canStatusStat    = lib_tkinter.GetCheckStat(self.statPanel, column=1, row=0, sticky="W",                        style=style)
        self.selfTestStat     = lib_tkinter.GetCheckStat(self.statPanel, column=1, row=1, sticky="W", inverted=True,         style=style)
        self.voltageTestStat  = lib_tkinter.GetCheckStat(self.statPanel, column=1, row=2, sticky="W", inverted=True,         style=style)
        self.tempTestStat     = lib_tkinter.GetCheckStat(self.statPanel, column=1, row=3, sticky="W", inverted=True,         style=style)
        self.senseTestStat    = lib_tkinter.GetCheckStat(self.statPanel, column=1, row=4, sticky="W", inverted=True,         style=style)
        # Column 2
        chargeLabel           = lib_tkinter.GetLabel    (self.statPanel, column=2, row=0, sticky="E", text="Charge:",        style=style)
        packVoltLabel         = lib_tkinter.GetLabel    (self.statPanel, column=2, row=1, sticky="E", text="Pack Voltage:",  style=style)
        maxVoltLabel          = lib_tkinter.GetLabel    (self.statPanel, column=2, row=2, sticky="E", text="High Voltage:",  style=style)
        minVoltLabel          = lib_tkinter.GetLabel    (self.statPanel, column=2, row=3, sticky="E", text="Low Voltage:",   style=style)
        currentLabel          = lib_tkinter.GetLabel    (self.statPanel, column=2, row=4, sticky="E", text="Current:",       style=style)
        self.chargeStat       = lib_tkinter.GetLabelStat(self.statPanel, column=3, row=0, sticky="W", precision=2,           style=style)
        self.packVoltStat     = lib_tkinter.GetLabelStat(self.statPanel, column=3, row=1, sticky="W", precision=2,           style=style)
        self.maxVoltStat      = lib_tkinter.GetLabelStat(self.statPanel, column=3, row=2, sticky="W", precision=2,           style=style)
        self.minVoltStat      = lib_tkinter.GetLabelStat(self.statPanel, column=3, row=3, sticky="W", precision=2,           style=style)
        self.currentStat      = lib_tkinter.GetLabelStat(self.statPanel, column=3, row=4, sticky="W", precision=2,           style=style)
        # Column 3
        maxTempLabel          = lib_tkinter.GetLabel    (self.statPanel, column=4, row=0, sticky="E", text="High Temp:",     style=style)
        meanTempLabel         = lib_tkinter.GetLabel    (self.statPanel, column=4, row=1, sticky="E", text="Average Temp:",  style=style)
        maxDeltaLabel         = lib_tkinter.GetLabel    (self.statPanel, column=4, row=2, sticky="E", text="High Delta:",    style=style)
        meanDeltaLabel        = lib_tkinter.GetLabel    (self.statPanel, column=4, row=3, sticky="E", text="Average Delta:", style=style)
        self.maxTempStat      = lib_tkinter.GetLabelStat(self.statPanel, column=5, row=0, sticky="W", precision=2,           style=style)
        self.meanTempStat     = lib_tkinter.GetLabelStat(self.statPanel, column=5, row=1, sticky="W", precision=2,           style=style)
        self.maxDeltaStat     = lib_tkinter.GetLabelStat(self.statPanel, column=5, row=2, sticky="W", precision=2,           style=style)
        self.meanDeltaStat    = lib_tkinter.GetLabelStat(self.statPanel, column=5, row=3, sticky="W", precision=2,           style=style)

    # Set View Type
    # - Sets the View Type of the Individual Cell Stats
    def SetViewType(self, viewType):
        for stat in self.cellStats:
            stat.SetViewType(viewType)

    # Update
    def Update(self):
        try:
            for index in range(CELL_WIDTH_COUNT*CELL_HEIGHT_COUNT):
                self.cellStats[index].Set(self.database.cellVoltages[index],
                                        self.database.cellBalancings[index],
                                        self.database.packTemperatures[int(index/2)],
                                        self.database.cellVoltageMin)
            self.canStatusStat.Set  (self.database.bmsCanActive)
            self.selfTestStat.Set   (self.database.errorBmsSelfTestFault)
            self.voltageTestStat.Set(self.database.errorBmsVoltageFault)
            self.tempTestStat.Set   (self.database.errorBmsTempFault)
            self.senseTestStat.Set  (self.database.errorBmsSenseLineFault)

            self.chargeStat.Set     (self.database.stateOfCharge)
            self.packVoltStat.Set   (self.database.packVoltage)
            self.maxVoltStat.Set    (self.database.cellVoltageMax)
            self.minVoltStat.Set    (self.database.cellVoltageMin)
            self.currentStat.Set    (self.database.packCurrent)

            self.maxTempStat.Set    (self.database.packTemperatureMax)
            self.meanTempStat.Set   (self.database.packTemperatureMean)
            self.maxDeltaStat.Set   (self.database.cellDeltaMax)
            self.meanDeltaStat.Set  (self.database.cellDeltaMean)
        except Exception as e:
            logging.error("BMS GUI Update Loop Error: " + str(e))
            raise

# Getters ---------------------------------------------------------------------------------------------------------------------
def GetCellStat(parent, style, minWidth=20, minHeight=20, grid=True, column=0, row=0, columnspan=1, rowspan=1, sticky="", styleOverrides=[]):
    style.InsertOverrides(styleOverrides)
    canvas = CellStat(parent, minWidth=int(minWidth), minHeight=int(minHeight), voltageError=style["voltageErrorColor"],
                      balancePalette=style["balancingPalette"], voltageDomain=style["voltageDomain"], temperaturePalette=style["tempHighlights"],
                      temperatureDomain=style["tempDomain"], fontColor=style["textColor"], borderColor=style["highlight"], font=style["font"],
                      borderWidth=style["borderWidth"])
    if(grid):
        canvas.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
    style.RemoveOverrides(styleOverrides)
    return canvas

# Widgets ---------------------------------------------------------------------------------------------------------------------
class CellStat(tkinter.Canvas):
    def __init__(self, parent, minWidth, minHeight, voltageError=['#FFAAAA'], balancePalette=['#F0F0F0'], temperaturePalette=['#FF0000'],
                 voltageDomain=[1], temperatureDomain=[1], fontColor='#000000', borderColor="#FFFFFF", font=("consolas", 10), borderWidth=2):
        self.width  = minWidth
        self.height = minHeight

        super().__init__(parent, width=self.width, height=self.height, highlightthickness=0)
        self.voltage            = None
        self.balancing          = None
        self.temperature        = None
        self.lowVoltage         = None
        self.viewType           = "Cell"
        self.voltageError       = voltageError
        self.balancePalette     = balancePalette
        self.temperaturePalette = temperaturePalette
        self.voltageDomain      = voltageDomain
        self.temperatureDomain  = temperatureDomain
        self.border     = self.create_rectangle(0, 0, self.width, self.height, width=0, outline=borderColor)
        self.foreground = self.create_rectangle(borderWidth, borderWidth, self.width-borderWidth-1, self.height-borderWidth-1, width=1, outline=borderColor)
        self.text       = self.create_text(self.width/2, self.height/2, fill=fontColor, font=font)

    def Update(self):
        if(self.viewType == "Cell"):
            self.itemconfigure(self.border,     fill=self.GetTemperatureColor())
            self.itemconfigure(self.foreground, fill=self.GetBalanceColor())
            self.itemconfigure(self.text,       text=self.GetVoltageText())
            self.itemconfigure(self.foreground, width=1)
        if(self.viewType == "Voltage"):
            self.itemconfigure(self.border,     fill=self.GetBalanceColor())
            self.itemconfigure(self.foreground, fill=self.GetBalanceColor())
            self.itemconfigure(self.text,       text=self.GetVoltageText())
            self.itemconfigure(self.foreground, width=0)
        if(self.viewType == "Temperature"):
            self.itemconfigure(self.border,     fill=self.GetTemperatureColor())
            self.itemconfigure(self.foreground, fill=self.GetTemperatureColor())
            self.itemconfigure(self.text,       text=self.GetTemperatureText())
            self.itemconfigure(self.foreground, width=0)
        if(self.viewType == "Delta"):
            self.itemconfigure(self.border,     fill=self.GetBalanceColor())
            self.itemconfigure(self.foreground, fill=self.GetBalanceColor())
            self.itemconfigure(self.text,       text=self.GetDeltaText())
            self.itemconfigure(self.foreground, width=0)

    def Set(self, voltage, balancing, temperature, lowest):
        self.voltage     = voltage
        self.balancing   = balancing
        self.temperature = temperature
        self.lowVoltage  = lowest
        self.Update()

    def SetViewType(self, viewType):
        self.viewType = viewType

    def GetVoltageText(self):
        if(self.voltage == None):
            return "--\n--"
        voltage = int(self.voltage*100) / 100
        text = str(voltage)
        while(len(text) < 4):
            text += "0"
        text = text.replace(".", ".\n")
        return text

    def GetDeltaText(self):
        if(self.voltage == None or self.lowVoltage == None):
            return "--"
        delta = self.voltage - self.lowVoltage
        delta = int(delta*100)/100
        text = str(delta)
        while(len(text) < 4):
            text += "0"
        text = text.replace(".", ".\n")
        return text

    def GetTemperatureText(self):
        if(self.temperature == None):
            return "--"
        temperature = int(self.temperature*10)/10
        text = str(temperature)
        return text

    def GetTemperatureColor(self):
        if(self.temperature == None): return self.temperaturePalette[0]
        for index in range(len(self.temperatureDomain)):
            if(self.temperature < self.temperatureDomain[index]):
                if(index <= 0):                           return self.temperaturePalette[0]
                if(index >= len(self.temperatureDomain)): return self.temperaturePalette[index]
                interpolation = InverseLinearInterpolate(self.temperature, self.temperatureDomain[index-1], self.temperatureDomain[index])
                return ColorLinearInterpolate(interpolation, self.temperaturePalette[index-1], self.temperaturePalette[index])
        return self.temperaturePalette[len(self.temperaturePalette)-1]

    def GetBalanceColor(self):
        if(self.balancing == None): return self.balancePalette[0]
        if(self.voltage == None):   return self.balancePalette[0]
        if(self.voltage < self.voltageDomain[0] or self.voltage > self.voltageDomain[1]):
            return self.voltageError
        if(    self.balancing): return self.balancePalette[1]
        if(not self.balancing): return self.balancePalette[2]

    def Grid(self, column=0, row=0, columnspan=1, rowspan=1, sticky=""):
        self.canvas.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)

# Misc Math Functions ---------------------------------------------------------------------------------------------------------
# Numeric Linerar Interpolation
def LinearInterpolate(value, min, max):
    return value * (max - min) + min

# Numeric Inverse Linear Interpolation
def InverseLinearInterpolate(value, min, max):
    return (value - min) / (max - min)

# Numeric Clamping
def Clamp(value, min, max):
    if(value > max): return max
    if(value < min): return min
    return value

# Hex Color Linear Interpolation
def ColorLinearInterpolate(value, min, max):
    # Extract Hexadecimal Color Channels to Integer Values
    redMin   = int(min[1:3], 16)
    greenMin = int(min[3:5], 16)
    blueMin  = int(min[5:7], 16)
    redMax   = int(max[1:3], 16)
    greenMax = int(max[3:5], 16)
    blueMax  = int(max[5:7], 16)
    # Interpolate Integer Values and Convert to Hex
    red   = hex(int(Clamp(LinearInterpolate(value, redMin,   redMax),   0, 255)))[2:]
    green = hex(int(Clamp(LinearInterpolate(value, greenMin, greenMax), 0, 255)))[2:]
    blue  = hex(int(Clamp(LinearInterpolate(value, blueMin,  blueMax),  0, 255)))[2:]
    # Insert '0' Padding
    while(len(red)   < 2): red   = '0' + red
    while(len(green) < 2): green = '0' + green
    while(len(blue)  < 2): blue  = '0' + blue
    # Generate Output from Channels
    colorOut = '#' + red + green + blue
    return colorOut