import minimalmodbus
from minimalmodbus import Instrument
from time import sleep

running = True


def read():
    sensor = Instrument('COM6', 1)
    sensor.serial.baudrate = 9600
    sensor.serial.bytesize = 8
    sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
    sensor.serial.stopbits = 1
    sensor.serial.timeout = 0.5
    sensor.mode = minimalmodbus.MODE_RTU

    # while True:
    global data, value
    data = sensor.read_registers(registeraddress=0,
                                 number_of_registers=2,
                                 functioncode=3)
    print(data)
    # sleep(1)
    # break


if __name__ == '__main__':
    while running:
        read()
        sleep(1)
