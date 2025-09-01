import json

import minimalmodbus

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
    def __init__(self, mb_address: int):
        super().__init__(mb_address)
        self.mb_address = mb_address
        self.params = {}
        self.write_reg_params = {}
        self.data = []
        self.err = ''

        try:
            # self.sensor = minimalmodbus.Instrument('/dev/ttyUSB0', self.mb_address) # for Linux
            self.sensor = minimalmodbus.Instrument('COM6', self.mb_address)
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
                self.params = self.params.get(str(self.mb_address))

            print(self.params)
            return self.params

        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути {file_path}")
        except json.JSONDecodeError:
            print(f"Ошибка: Не удалось декодировать JSON из файла {file_path}")
        except Exception as err:
            print(f"Произошла ошибка: {err}")

    def get_actual_params(self):
        self.sensor.serial.baudrate = self.params.get('baudrate')
        self.sensor.serial.bytesize = self.params.get('bytesize')
        self.sensor.serial.parity = PARITY.get('NONE')
        self.sensor.serial.stopbits = self.params.get('stopbits')
        self.sensor.serial.timeout = self.params.get('timeout')
        self.sensor.mode = minimalmodbus.MODE_RTU

    def read(self):
        self.get_actual_params()

        self.data = self.sensor.read_registers(
            registeraddress=self.params.get('registeraddress'),
            number_of_registers=self.params.get('number_of_registers'),
            functioncode=self.params.get('functioncode'))
        print(self.data)

    def write(self):
        self.get_actual_params()

        self.sensor.write_register(registeraddress=self.write_reg_params.get('registeraddress'),
                                   value=self.write_reg_params.get('value'),
                                   number_of_decimals=self.write_reg_params.get('number_of_decimals'),
                                   functioncode=self.write_reg_params.get('functioncode'),
                                   signed=self.write_reg_params.get('signed'))

        # self.sensor.write_registers(registeraddress=3,
        #                             values=[1, 2, 3, 4])
