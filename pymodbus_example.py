from pymodbus.client.serial import ModbusSerialClient
from pymodbus.exceptions import ModbusException
from pymodbus import FramerType

client = ModbusSerialClient(framer=FramerType.RTU, port='/dev/ttyUSB0', baudrate=9600, parity='N', bytesize=8,
                            stopbits=1,
                            timeout=0.5)

try:
    client.connect()
    print("Соединение открыто")

    address = 100

    # read
    rr = client.read_holding_registers(address, count=4, device_id=2)

    if rr.isError():
        print(f"Ошибка чтения: {rr.exception_code}")
    else:
        print(f"Успешно прочитано: {rr.registers}")
        print(f"Значение первого регистра: {rr.registers[0]}")
        float_values = client.convert_from_registers(rr.registers,
                                                     data_type=ModbusSerialClient.DATATYPE.FLOAT32,
                                                     word_order='little',
                                                     string_encoding=list[float])
        print(float_values)

    # write
    write_result = client.write_register(1, value=123, device_id=2)  # Записать 123 в регистр 10
    if write_result.isError():
        print(f"Ошибка записи: {write_result.exception_code}")
    else:
        print("Значение записано")

    # write float
    float_for_write = 6.784
    float_to_regs = client.convert_to_registers(float_values,
                                                data_type=ModbusSerialClient.DATATYPE.FLOAT32,
                                                word_order='little')

    write_result = client.write_registers(3, values=float_to_regs, device_id=2)  # Записать 123 в регис

    # coils
    coils = client.read_coils(0, count=4, device_id=2)
    if coils.isError():
        print(f"Ошибка чтения: {coils.exception_code}")
    else:
        print(f"Успешно прочитано: {coils.bits}")

except ModbusException as e:
    print(f"Произошла ошибка Modbus: {e}")
except Exception as e:
    print(f"Произошла другая ошибка: {e}")
finally:
    client.close()
    print("Соединение закрыто")
