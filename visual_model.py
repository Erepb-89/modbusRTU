from threading import Event
from time import sleep

from pymodbus import FramerType
from pymodbus.client import ModbusSerialClient

from settings import SCAN_RATE
from slave_classes import SlaveEncoder


class VisualModel:
    def __init__(self):
        self.running_read = Event()
        self.create_client()
        self.create_slaves()

        self.set_default_params_for_all_slaves()

    def set_default_params_for_all_slaves(self):
        self.set_default_params(self.slave1, 1)
        self.set_default_params(self.slave2, 2)
        self.set_default_params(self.slave3, 3)
        self.set_default_params(self.slave4, 4)

    def create_client(self, parent=None):
        self.client = ModbusSerialClient(framer=FramerType.RTU,
                                             port='/dev/ttyUSB0',
                                             baudrate=9600,
                                             parity='N',
                                             bytesize=8,
                                             stopbits=1,
                                             timeout=0.5)

            # self.client = minimalmodbus.Instrument('/dev/ttyUSB0', self.slave_id) # for Linux
            # self.client = minimalmodbus.Instrument('COM6', self.slave_id)
        print(self.client)
        self.client.connect()
        if self.client.connected:
            print("Соединение открыто")
            self.create_slaves()

            if parent is not None:
                parent.ui.LabelMessage_5.setText("Соединение открыто")

        try:
            if not self.client.connected:
                self.client.diag_get_comm_event_log()
        except Exception as err:
            print(err)
            if parent is not None:
                parent.ui.LabelMessage_5.setText(str(err))

    def create_slaves(self):
        self.slave1 = SlaveEncoder(1, self.client)
        self.slave2 = SlaveEncoder(2, self.client)
        self.slave3 = SlaveEncoder(3, self.client)
        self.slave4 = SlaveEncoder(4, self.client)

        self.set_default_params_for_all_slaves()

    def load_json_params(self, path):
        self.slave1.load_json_params(path)
        self.slave2.load_json_params(path)

    def set_default_params(self, slave: SlaveEncoder, slave_id: int):
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

    def reading_thread(self, parent):
        while self.running_read.is_set():
            if parent.ui.checkBoxPolling.isChecked():
                try:
                    self.slave1.read(parent.ui.LabelMessage)
                    parent.read_registers_list_update()
                    sleep(SCAN_RATE)
                except Exception as err:
                    print(err)

            if parent.ui.checkBoxPolling_2.isChecked():
                try:
                    self.slave2.read(parent.ui.LabelMessage_2)
                    parent.read_registers_list_update_2()
                    sleep(SCAN_RATE)
                except Exception as err:
                    print(err)

            if parent.ui.checkBoxPolling_3.isChecked():
                try:
                    self.slave3.read(parent.ui.LabelMessage_3)
                    parent.read_registers_list_update_3()
                    sleep(SCAN_RATE)
                except Exception as err:
                    print(err)

            if parent.ui.checkBoxPolling_4.isChecked():
                try:
                    self.slave4.read(parent.ui.LabelMessage_4)
                    parent.read_registers_list_update_4()
                    sleep(SCAN_RATE)
                except Exception as err:
                    print(err)

    # def read_slave_data(self, parent, slave, label_message, check_box):
    #     if check_box.isChecked():
    #         try:
    #             slave.read(label_message)
    #             parent.read_registers_list_update()
    #             sleep(SCAN_RATE)
    #         except Exception as err:
    #             print(err)

    def stop_polling(self):
        self.running_read.clear()
        print('Чтение завершено')


v_model = VisualModel()
