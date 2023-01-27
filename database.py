import enum
from enum import Enum

def Setup():
    return CarData()

class CarData():
    # Input ---------------------------------------------------------------------------------------------------
    class InputTypes(Enum):                              # Input Type Enumerable
        BUTTON_WHEEL_LEFT  = 0,                          # - Left Button of Steering Wheel
        BUTTON_WHEEL_RIGHT = 1,                          # - Right Button of Steering Wheel
        BUTTON_DASH_LEFT   = 2,                          # - Left Button of Dashboard
        BUTTON_DASH_RIGHT  = 3                           # - Right Button of Dashboard

    # Communications ------------------------------------------------------------------------------------------
    ecuCanActive           = False                       # Activity of the ECU CAN
    acanCanActive          = False                       # Activity of the ACAN CAN
    bmsCanActive           = False                       # Activity of the BMS CAN
    inverterCanActive      = False                       # Activity of the Inverter CAN

    ecuCanTimeout          = None                        # Time of last ECU CAN message received 
    acanCanTimeout         = None                        # Time of last ACAN CAN message received
    bmsCanTimeout          = None                        # Time of last BMS CAN message received
    inverterCanTimeout     = None                        # Time of last Inverter CAN message received

    # Pedal Info ----------------------------------------------------------------------------------------------
    apps1                  = None                        # Real APPS-1 Value from ACAN
    apps2Raw               = None                        # Real APPS-2 Value from ACAN
    brake1                 = None                        # Real Brake-1 Value from ACAN
    brake2                 = None                        # Real Brake-2 Value from ACAN

    apps1Percent           = None                        # APPS-1 Percentage from ECU
    apps2Percent           = None                        # APPS-2 Percentage from ECU
    brake1Percent          = None                        # Brake-1 Percentage from ECU
    brake2Percent          = None                        # Brake-2 Percentage from ECU

    apps1Min               = None                        # APPS-1 Calibration Minimum from Dash
    apps1Max               = None                        # APPS-1 Calibration Maximum from Dash
    apps2RawMin            = None                        # APPS-2 Calibration Minimum from Dash
    apps2RawMax            = None                        # APPS-2 Calibration Maximum from Dash

    accelerating           = None                        # Acceleration State (True => Accelerating)
    braking                = None                        # Braking State (True => Braking)

    # ECU Info ------------------------------------------------------------------------------------------------
    class DriveState(Enum):                              # Drive State Type Enumerable
        INITIALIZING       = 0,                          # - Initialization State of ECU
        LV_DRIVEOFF        = 1,                          # - Low-Voltage State
        HV_DRIVEOFF        = 2,                          # - High-Voltage State
        HV_DRIVEON         = 3                           # - Ready-to-Drive State

    driveState             = DriveState.INITIALIZING     # Current Drive State of the Vehicle
    drsState               = None                        # Current DRS State of the Vehicle
    regenState             = None                        # Current Regen Braking State of the Vehicle
    lvBatteryVoltage       = None                        # Voltage of the LV Battery

    # Acumulator Data -----------------------------------------------------------------------------------------
    stateOfCharge          = None                        # State of Charge
    packVoltage            = None                        # Total Voltage of the Accumulator
    packCurrent            = None                        # Current of the Accumulator
    cellVoltages           = [None]*90                   # Accumulator Cell Voltages
    cellBalancings         = [None]*90                   # Accumulator Cell Balancings
    cellVoltageMax         = None                        # Accumulator Highest Cell Voltage
    cellVoltageMin         = None                        # Accumulator Lowest Cell Voltage
    cellDeltaMax           = None                        # Accumulator Max Delta Voltage
    cellDeltaMean          = None                        # Accumulator Average Delta Voltage
    packTemperatures       = [None]*45                   # Accumulator Pack Temperatures
    packTemperatureMax     = None                        # Highest Pack Temperature
    packTemperatureMean    = None                        # Average Pack Temperature
    segmentSenseLines      = [None]*5                    # Accumulator Segment Sense Line Statuses

    # Inverter Data -------------------------------------------------------------------------------------------
    inverterTempGdb        = None                        # Temperature of the Inverter GDB
    inverterTempModuleA    = None                        # Temperature of the Inverter Module A
    inverterTempModuleB    = None                        # Temperature of the Inverter Module B
    inverterTempModuleC    = None                        # Temperature of the Inverter Module C
    inverterTempCb         = None                        # Temperature of the Inverter CB
    inverterTempMean       = None                        # Average Temperature of the Inverter
    inverterTempMax        = None                        # Maximum Temperature of the Inverter

    # Motor Data ----------------------------------------------------------------------------------------------
    motorRpm               = None                        # RPM of the Motor
    motorSpeedMph          = None                        # Speed of the Vehicle
    torquePercentageMax    = None                        # Maximum Torque Percentage from ECU
    torquePercentageRegen  = None                        # Maximum Regen Percentage from ECU
    motorTemperature       = None                        # Temperature of the Motor

    # Errors --------------------------------------------------------------------------------------------------
    error25_5Implausible   = None                        # 25/5 APPS Implausibility
    errorInverterFault     = None                        # Inverter Fault Detected
    errorAcanImplausible   = None                        # ACAN Value Implausibility
    error100MsImplausible  = None                        # 100ms APPS Implausibility
    errorBmsTempFault      = None                        # BMS Temperature Fault
    errorBmsVoltageFault   = None                        # BMS Voltage Fault
    errorBmsSelfTestFault  = None                        # BMS Self Test Fault
    errorBmsSenseLineFault = None                        # BMS Sense Line Fault