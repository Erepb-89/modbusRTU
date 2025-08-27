import minimalmodbus

PARITY = {
    "NONE": minimalmodbus.serial.PARITY_NONE,
    "ODD": minimalmodbus.serial.PARITY_ODD,
    "EVEN": minimalmodbus.serial.PARITY_EVEN,
    "MARK": minimalmodbus.serial.PARITY_MARK,
    "SPACE": minimalmodbus.serial.PARITY_SPACE,
    "NAMES": minimalmodbus.serial.PARITY_NAMES,
}

FUNCTION_LIST_READ = [
    "01 Read Coils (0x)",
    "02 Read Discrete Inputs (1x)",
    "03 Read Holding Registers (4x)",
    "04 Read Input Registers (3x)",
]

FUNCTION_LIST_WRITE = [
    "6 Write Single Register",
    "16 Write Multiple Registers",
]
