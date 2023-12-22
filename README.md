# ZRE-Dashboard-2023
This code is for the dashboard of a Zips Racing Electric's Formula SAE Electric race car, using the CAN communications protocol. This code is designed to run on a Raspberry Pi 3B with an HDMI Touchscreen.

## GUI Hierarchy
### Low Voltage View
The Low Voltage View is the primary view for when the car is not in drive mode. The lv-view is designed for calibration, configuration,
and debugging. When the car is first powered on it will enter the lv-view, where it will instruct the driver on how to enter drive-mode.
The lv-view is structured in 3 main sections, correlating to the appropriate drive-states.
- Initialization State
The initialization state occurs when the car first enters low voltage. This state only lasts until the ECU has properly initialized and has begun
sending CAN messages. After the first ECU CAN message has been received, the lv-view will enter the low-voltage state
- Low Voltage State
The low voltages state is present as long as the car is in low voltage. This view will allow for pedal calibration, adjustment of config
values, adjustment of settings, and viewing of debug information. The low voltage view will also inform the driver on how to turn on
high voltage.
- High Voltage State
The high voltage state occurs when the car has just entered high voltage, but is still not ready to drive. The high voltage state will not allow
calibration or configuration, but basic settings and debugging will still be available. The high voltage state will inform the driver on how to
start the car. Upon the starting of the car, the GUI will exit the low voltage view and transfer to a drive view.

### Speed View
The Speed View is the simplest drive view, intended for general driving. The layout of this view is shown below.
![alt text](images/speedView.png)
- The bars on the left and right show the position of the brake and throttle pedals, respectively.
- The bar on the top of the screen shows the current RPM as a portion of the maximum RPM, being 5500.
- The two bars on the bottom of the screen show the torque and regen percentage.
  - The torque percentage controls the maximum amount of torque able to be sent to the inverter, as a portion of 230Nm.
  - The regen percentage controls the maximum amount of torque able to be sent during regenerative braking, as a portion of 23Nm.
- The text in the center of the screen showns the speed of the car in MPH.
- The four buttons on the bottom of the screen allow the driver to switch to different drive views, labeled respectively.

### Endurance View
The Endurance View is designed for use at endurance events. The endurance view is structured similarly to the Speed View, with the main difference
being the usage of the center text as the vehicle state of charge, rather than a speed. The Stat Panel on the left of the screen is also extented,
with the state of charge being removed and additional temperatures being added.

# Code Structure
## Application - app.py
The main file for the application, execute this file to instance the app. This file is responsible for instancing and initializing the CAN and GUI modules.

## GUI - gui.py
The GUI module contains everything for managing the TKinter GUI.

### gui.Main
#### Constructor
This object, when instanced, will setup an empty TKinter window. An interface for a database, views, subwindows, and interrupts will be established.

*Due to the structure of TK, this class can only be instanced once per application.*

#### Append View
Call this method to insert a View Object into the list of GUI views. The first object appended will act as the default view, being opened when **CloseViews()** is called. The Views in this list can be accessed using **OpenView()**

#### Open View
After views have been properly initialized and appended, this method may be called to **Open()** a specific view by ID or by reference. This function will **Close()** the currently opened view, then **Open()** the desired view.

#### Close Views
After views have been properly initialized and appended, this method may be called to **Close()** the currently opened view. The view that is in position 0 of the views list will be opened.

#### Append Window
Call this method to insert a Window Object into the list of GUI subwindows.

#### Toggle Window
After windows have been properly initialized and appended, this method may be called to **Toggle()** a specific window by ID or by reference. If the specified window is currently open, it will be closed, and vice-versa.

#### Append Keybind
Call this method to insert a Keybind to the Keyboard interrupt. The **key** parameter will accept a string, being the **keysym** identity of the desired key. The command parameter accepts a lambda function that will be executed on the key interrupt.

#### Update
This method, when called, will call the **Update()** function of the currently opened view, if any.

#### Loop
This method, when called, will begin the update loop of the GUI. The function will call the **Update()** function of the GUI, then schedule itself to be called again based on the GUI framerate.

*This funtion is called by the **Begin()** function of the GUI. This function is for internal use only.*

#### Kill
Call this method to destroy the GUI and its children. The main TKinter window and its subwindows will be closed, key interrupts will no longer respond, and the update loop will be halted.

*If the GUI has already been destoryed, this function will do nothing.*

### gui.View
This object represents a root frame for the TKinter main window. In usage with the **Main** class, this object provides a stable framework for a GUI with multiple views and a main menu. Objects inheriting from this class will inherit the behavior for opening and closing, initialization, and updating. These methods may be overrided appropriately.

### gui.Window
This object represents a TopLevel object for the TKinter main window. In usage with the **Main** class, this object provides a stable framework for a GUI with Subwindows. Objects inheriting from this class will inherit the behavior opening, closing, toggling, and updating. These methods may be overrided appropriately.

### gui.Setup
This method, when called, will create and return an instance of the Main GUI class. The Main Object will be initialized and setup with appropriate views, subwindows, and interrupts. An instance of the gui_Main.View() will also be created, as a main menu for the GUI.

## Menu GUI - gui_Menu.py
This module contains the framework for the main menu of the GUI. 

### gui_Main.View
This object inherits from the gui.View object, giving it the ability to be appended and opened via the main GUI object. 

#### Constructor
When instanced, the menu will initialize itself, creating a root frame and defining its member functions. It will then instance a lib_tkinter.ScrollFrame widget, acting as the root for widget placement. This allows for many entries to fit on-screen without sacrificing widget size. By default, the menu will contain nothing until it has shortcuts appended.

#### Append Shortcut
This method will create and place a button for accessing other views. The ID passed to this function is that of the view to open when said button is pressed. In addition to this, an icon may be included which will be displayed with the button appropriately.

*Only IDs of views that current exist or will soon exist should be used. Pressing a button with an invalid ID will throw an error message*

## CAN - can.py
This module acts as the manager for anything relating to the CAN communications protocol.
### can.LibraryType
This Enum is used to identify the library that should be used for communication. The types are as follows.
- EMULATE - This indicates that no library should be used, rather, outgoing messages should simply be ignored.
- CANLIB - This refers to the Kvaser CANLIB python library. This library is handled by the lib_canlib module.
- INNOMAKER - This refers to the InnoMaker usb2can library. This library has not yet been implemented.

### can.CanInterface
This object is the parent class for any CAN interface. Any implemented libraries should inherit from this object, allowing for a standard interface for any CAN libraries.

### can.Setup
This function is used to setup the CAN interface. Depending on the library type selected, the appropriate interface will be initialized and started. This function takes a database object as a parameter, which is the target location for incoming data. This function will return the setup interface.

## Database - database.py
This module is the manager for any databases used by the application.
