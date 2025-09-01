from threading import Event, Thread
from time import sleep

from settings import SCAN_RATE
from slave_classes import SlaveEncoder


class VisualModel:
    def __init__(self):
        self.running_read = Event()
        self.connect_port()

        # try:
        self.set_standard_settings(self.slave1, 1)
        self.set_standard_settings(self.slave2, 2)
        self.set_standard_settings(self.slave3, 3)
        self.set_standard_settings(self.slave4, 4)
        # except Exception as err:
        #     print(err)

    def connect_port(self):
        self.slave1 = SlaveEncoder(1)
        self.slave2 = SlaveEncoder(2)
        self.slave3 = SlaveEncoder(3)
        self.slave4 = SlaveEncoder(4)

    def load_json_params(self, path):
        self.slave1.load_json_params(path)
        self.slave2.load_json_params(path)

    def set_standard_settings(self, slave, slave_id):
        slave.params["slave_id"] = slave_id
        slave.params["registeraddress"] = 0
        slave.params["number_of_registers"] = 10
        slave.params["functioncode"] = 3
        slave.params["baudrate"] = 9600
        slave.params["bytesize"] = 8
        slave.params["parity"] = "NONE"
        slave.params["stopbits"] = 1
        slave.params["timeout"] = 0.5

    def start_polling(self):
        self.running_read.set()

        read_thread = Thread(target=self.reading_thread,
                             name="reading Thread")
        read_thread.start()

    def write_register(self):
        try:
            self.slave1.write()
        except Exception as err:
            print(err)

    def reading_thread(self):
        # while self.attempts > 0 and self.running:
        while self.running_read.is_set():
            try:
                self.slave1.read()
                sleep(SCAN_RATE)
            except Exception as err:
                print(err)

            try:
                self.slave2.read()
                sleep(SCAN_RATE)
            except Exception as err:
                print(err)

            try:
                self.slave3.read()
                sleep(SCAN_RATE)
            except Exception as err:
                print(err)

            try:
                self.slave4.read()
                sleep(SCAN_RATE)
            except Exception as err:
                print(err)

    def stop_polling(self):
        self.running_read.clear()
        print('Чтение завершено')


# v_model = VisualModel()
