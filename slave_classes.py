import json

import minimalmodbus
from pymodbus import FramerType
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

from settings import PARITY


class ParentSlave:
    """Класс Слейв-родитель"""

    def __init__(self, mb_address: int):
        self.mb_address = mb_address

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.mb_address!r},')

    def __str__(self):
        return f'Slave: {self.mb_address}'

    def read(self):
        pass


class SlaveEncoder(ParentSlave):
    def __init__(self, slave_id: int):
        super().__init__(slave_id)
        self.slave_id = slave_id
        self.params = {}
        self.write_reg_params = {}
        self.data = []
        self.err = ''

        try:
            self.client = ModbusSerialClient(framer=FramerType.RTU,
                                             port='/dev/ttyUSB0',
                                             baudrate=9600,
                                             parity='N',
                                             bytesize=8,
                                             stopbits=1,
                                             timeout=0.5)

            # self.client = minimalmodbus.Instrument('/dev/ttyUSB0', self.slave_id) # for Linux
            # self.client = minimalmodbus.Instrument('COM6', self.slave_id)
        except FileNotFoundError as err:
            print(err)
            self.err = str(err)
        except Exception as err:
            print(err)
            self.err = str(err)

    def load_json_params(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Загружаем JSON-данные из файла в переменную params
                self.params = json.load(f)
                self.params = self.params.get(str(self.slave_id))

            print(self.params)
            return self.params

        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути {file_path}")
        except json.JSONDecodeError:
            print(f"Ошибка: Не удалось декодировать JSON из файла {file_path}")
        except Exception as err:
            print(f"Произошла ошибка: {err}")

    def get_actual_params(self):
        # self.client.serial.registeraddress = self.params.get('registeraddress')
        # self.client.serial.baudrate = self.params.get('baudrate')
        # self.client.serial.bytesize = self.params.get('bytesize')
        # self.client.serial.parity = PARITY.get('NONE')
        # self.client.serial.stopbits = self.params.get('stopbits')
        # self.client.serial.timeout = self.params.get('timeout')
        # self.client.mode = minimalmodbus.MODE_RTU

        self.client.comm_params.baudrate = self.params.get('baudrate')
        self.client.comm_params.bytesize = self.params.get('bytesize')
        self.client.comm_params.parity = 'N'
        self.client.comm_params.stopbits = self.params.get('stopbits')
        self.client.comm_params.timeout_connect = self.params.get('timeout')
        self.client.comm_params.comm_type = minimalmodbus.MODE_RTU

    def read(self):
        self.get_actual_params()

        # minimalmodbus
        # self.data = self.client.read_registers(
        #     registeraddress=self.params['registeraddress'],
        #     number_of_registers=self.params['number_of_registers'],
        #     functioncode=self.params['functioncode'])
        # print(self.data)

        # pymodbus
        try:
            self.client.connect()
            print("Соединение открыто")

            self.data = self.client.read_holding_registers(address=self.params['registeraddress'],
                                                           count=self.params['number_of_registers'],
                                                           device_id=self.slave_id)

            if self.data.isError():
                print(f"Ошибка чтения: {self.data.exception_code}")
            else:
                print(f"Успешно прочитано: {self.data.registers}")
                print(f"Значение первого регистра: {self.data.registers[0]}")
                float_values = self.client.convert_from_registers(self.data.registers,
                                                                  data_type=ModbusSerialClient.DATATYPE.FLOAT32,
                                                                  word_order='little',
                                                                  string_encoding=list[float])
                print(float_values)

        except ModbusException as e:
            print(f"Произошла ошибка Modbus: {e}")
        except Exception as e:
            print(f"Произошла другая ошибка: {e}")
        finally:
            self.client.close()
            print("Соединение закрыто")

    def write(self):
        self.get_actual_params()

        # minimalmodbus
        # self.client.write_register(registeraddress=self.write_reg_params.get('registeraddress'),
        #                            value=float(self.write_reg_params.get('value')),
        #                            number_of_decimals=self.write_reg_params.get('number_of_decimals'),
        #                            functioncode=self.write_reg_params.get('functioncode'),
        #                            signed=self.write_reg_params.get('signed'))

        # self.client.write_registers(registeraddress=3,
        #                             values=[1, 2, 3, 4])

        # pymodbus
        try:
            self.client.close()
            self.client.connect()

            if self.write_reg_params.get('signed'):
                float_to_regs = self.client.convert_to_registers(value=float(self.write_reg_params.get('value')),
                                                                 data_type=ModbusSerialClient.DATATYPE.FLOAT32,
                                                                 word_order='little')

                write_result = self.client.write_registers(address=self.write_reg_params.get('registeraddress'),
                                                           values=float_to_regs,
                                                           device_id=self.slave_id)
                if write_result.isError():
                    print(f"Ошибка записи: {write_result.exception_code}")
                else:
                    print("Значение записано")
            else:
                write_result = self.client.write_register(address=self.write_reg_params.get('registeraddress'),
                                                          value=int(self.write_reg_params.get('value')),
                                                          device_id=self.slave_id)
                if write_result.isError():
                    print(f"Ошибка записи: {write_result.exception_code}")
                else:
                    print("Значение записано")
        except ModbusException as e:
            print(f"Произошла ошибка Modbus: {e}")
        except Exception as e:
            print(f"Произошла другая ошибка: {e}")
        finally:
            self.client.close()
            print("Соединение закрыто")