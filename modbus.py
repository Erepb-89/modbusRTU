import os
import sys
from threading import Thread, Event
from typing import List

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QListView
from time import sleep

from slave_classes import SlaveEncoder
from ui.main_window import Ui_MainWindow
from ui.params_dialog import Ui_ParamsDialog
from ui.params_dialog_2 import Ui_ParamsDialog_2
from ui.params_dialog_3 import Ui_ParamsDialog_3
from ui.params_dialog_4 import Ui_ParamsDialog_4
from ui.write_single_dialog import Ui_WriteRegDialog
from ui.write_single_dialog_2 import Ui_WriteRegDialog_2
from ui.write_single_dialog_3 import Ui_WriteRegDialog_3
from ui.write_single_dialog_4 import Ui_WriteRegDialog_4


class MainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    """

    def __init__(self):
        super().__init__()
        # основные переменные
        self.name = 'ClientMainWindow'
        self.running_read_1 = Event()
        self.running_read_2 = Event()
        self.running_read_3 = Event()
        self.running_read_4 = Event()
        # self.attempts = 3

        self.slave1 = SlaveEncoder(1)
        self.slave2 = SlaveEncoder(2)
        self.slave3 = SlaveEncoder(3)
        self.slave4 = SlaveEncoder(4)

        try:
            self.set_standard_settings(self.slave1)
            self.set_standard_settings(self.slave2)
            self.set_standard_settings(self.slave3)
            self.set_standard_settings(self.slave4)
        except Exception as err:
            print(err)

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonStartPolling.clicked.connect(self.start_polling_1)
        self.ui.pushButtonStopPolling.clicked.connect(self.stop_polling_1)
        self.ui.pushButtonStartPolling_2.clicked.connect(self.start_polling_2)
        self.ui.pushButtonStopPolling_2.clicked.connect(self.stop_polling_2)
        self.ui.pushButtonStartPolling_3.clicked.connect(self.start_polling_3)
        self.ui.pushButtonStopPolling_3.clicked.connect(self.stop_polling_3)
        self.ui.pushButtonStartPolling_4.clicked.connect(self.start_polling_4)
        self.ui.pushButtonStopPolling_4.clicked.connect(self.stop_polling_4)

        self.ui.pushButtonChooseJSON.clicked.connect(self.open_json_dialog)
        self.ui.pushButtonLoadParams.clicked.connect(self.load_json_params)

        self.ui.pushButtonSlave1Settings.clicked.connect(self.open_params_dialog_1)
        self.ui.pushButtonSlave2Settings.clicked.connect(self.open_params_dialog_2)
        self.ui.pushButtonSlave3Settings.clicked.connect(self.open_params_dialog_3)
        self.ui.pushButtonSlave4Settings.clicked.connect(self.open_params_dialog_4)

        self.ui.pushButtonWriteReg.clicked.connect(self.open_write_dialog_1)
        self.ui.pushButtonWriteReg_2.clicked.connect(self.open_write_dialog_2)
        self.ui.pushButtonWriteReg_3.clicked.connect(self.open_write_dialog_3)
        self.ui.pushButtonWriteReg_4.clicked.connect(self.open_write_dialog_4)

        self.ui.pushButtonLoadParams.setEnabled(False)
        self.ui.pushButtonStopPolling.setEnabled(False)
        self.ui.pushButtonStopPolling_2.setEnabled(False)
        self.ui.pushButtonStopPolling_3.setEnabled(False)
        self.ui.pushButtonStopPolling_4.setEnabled(False)
        self.show()

    def closeEvent(self, event) -> None:
        """Закрытие всех окон по выходу из главного"""
        self.running_read_1.clear()
        os.sys.exit(0)

    def open_json_dialog(self):
        """Кнопка Открыть (для поиска JSON-файла)"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.json_path, _ = QFileDialog.getOpenFileName(self,
                                                        "QFileDialog.getOpenFileName()",
                                                        "JSON",
                                                        "JOSN Files (*.json)",
                                                        options=options)

        if self.json_path:
            self.ui.LabelMessage.setText(self.json_path)
            self.ui.pushButtonLoadParams.setEnabled(True)
        else:
            self.ui.LabelMessage.setText("Выберите JSON файл")

    def load_json_params(self):
        self.slave1.load_json_params(self.json_path)
        self.slave2.load_json_params(self.json_path)
        self.ui.pushButtonStartPolling.setEnabled(True)
        self.ui.pushButtonStartPolling_2.setEnabled(True)

    def set_standard_settings(self, slave):
        self.slave1.params["slave_id"] = 1
        self.slave2.params["slave_id"] = 2
        self.slave3.params["slave_id"] = 3
        self.slave4.params["slave_id"] = 4

        slave.params["registeraddress"] = 0
        slave.params["number_of_registers"] = 10
        slave.params["functioncode"] = 3
        slave.params["baudrate"] = 9600
        slave.params["bytesize"] = 8
        slave.params["parity"] = "NONE"
        slave.params["stopbits"] = 1
        slave.params["timeout"] = 0.5

    def open_params_dialog_1(self):
        try:
            dialog = Ui_ParamsDialog(self)
            dialog.exec()  # Открывает диалог модально
        except Exception as err:
            print(err)

    def open_params_dialog_2(self):
        try:
            dialog = Ui_ParamsDialog_2(self)
            dialog.exec()
        except Exception as err:
            print(err)

    def open_params_dialog_3(self):
        try:
            dialog = Ui_ParamsDialog_3(self)
            dialog.exec()
        except Exception as err:
            print(err)

    def open_params_dialog_4(self):
        try:
            dialog = Ui_ParamsDialog_4(self)
            dialog.exec()
        except Exception as err:
            print(err)

    def open_write_dialog_1(self):
        dialog = Ui_WriteRegDialog(self)
        dialog.exec()  # Открывает диалог модально

    def open_write_dialog_2(self):
        dialog = Ui_WriteRegDialog_2(self)
        dialog.exec()

    def open_write_dialog_3(self):
        dialog = Ui_WriteRegDialog_3(self)
        dialog.exec()

    def open_write_dialog_4(self):
        dialog = Ui_WriteRegDialog_4(self)
        dialog.exec()

    def start_polling_1(self):
        self.ui.pushButtonStartPolling.setEnabled(False)
        self.ui.pushButtonStopPolling.setEnabled(True)
        self.running_read_1.set()

        read_thread = Thread(target=self.reading_thread_1,
                             name="read Thread 1")
        read_thread.start()

    def start_polling_2(self):
        self.ui.pushButtonStartPolling_2.setEnabled(False)
        self.ui.pushButtonStopPolling_2.setEnabled(True)
        self.running_read_2.set()

        read_thread = Thread(target=self.reading_thread_2,
                             name="read Thread 2")
        read_thread.start()

    def start_polling_3(self):
        self.ui.pushButtonStartPolling_3.setEnabled(False)
        self.ui.pushButtonStopPolling_3.setEnabled(True)
        self.running_read_3.set()

        read_thread = Thread(target=self.reading_thread_3,
                             name="read Thread 3")
        read_thread.start()

    def start_polling_4(self):
        self.ui.pushButtonStartPolling_4.setEnabled(False)
        self.ui.pushButtonStopPolling_4.setEnabled(True)
        self.running_read_4.set()

        read_thread = Thread(target=self.reading_thread_4,
                             name="read Thread 4")
        read_thread.start()

    def write_register(self):
        try:
            self.slave1.write()
            self.ui.LabelMessage.setText("Запись в slave 1 успешно произведена")
        except Exception as err:
            print(err)
            self.ui.LabelMessage.setText(str(err))

    def write_register_2(self):
        try:
            self.slave2.write()
            self.ui.LabelMessage.setText("Запись в slave 2 успешно произведена")
        except Exception as err:
            print(err)
            self.ui.LabelMessage.setText(str(err))

    def write_register_3(self):
        try:
            self.slave3.write()
            self.ui.LabelMessage.setText("Запись в slave 3 успешно произведена")
        except Exception as err:
            print(err)
            self.ui.LabelMessage.setText(str(err))

    def write_register_4(self):
        try:
            self.slave4.write()
            self.ui.LabelMessage.setText("Запись в slave 4 успешно произведена")
        except Exception as err:
            print(err)
            self.ui.LabelMessage.setText(str(err))

    def reading_thread_1(self):
        # while self.attempts > 0 and self.running:
        while self.running_read_1.is_set():
            try:
                self.slave1.read()
                # self.attempts -= 1
                self.read_registers_list_update()
                sleep(1)
            except Exception as err:
                self.ui.LabelMessage.setText(str(err))
                print(err)
                self.stop_polling_1()
                # self.attempts -= 1

    def reading_thread_2(self):
        while self.running_read_2.is_set():
            try:
                self.slave2.read()
                self.read_registers_list_update_2()
                sleep(1)
            except AttributeError as err:
                self.ui.LabelMessage.setText(str(err))
                self.running_read_2.clear()

            except Exception as err:
                self.ui.LabelMessage.setText(str(err))
                print(err)
                self.stop_polling_2()

    def stop_polling_1(self):
        self.ui.pushButtonStartPolling.setEnabled(True)
        self.ui.pushButtonStopPolling.setEnabled(False)
        self.running_read_1.clear()
        print('Чтение Slave 1 завершено')

    def stop_polling_2(self):
        self.ui.pushButtonStartPolling_2.setEnabled(True)
        self.ui.pushButtonStopPolling_2.setEnabled(False)
        self.running_read_2.clear()
        print('Чтение Slave 2 завершено')

    def stop_polling_3(self):
        self.ui.pushButtonStartPolling_3.setEnabled(True)
        self.ui.pushButtonStopPolling_3.setEnabled(False)
        self.running_read_3.clear()
        print('Чтение Slave 3 завершено')

    def stop_polling_4(self):
        self.ui.pushButtonStartPolling_4.setEnabled(True)
        self.ui.pushButtonStopPolling_4.setEnabled(False)
        self.running_read_4.clear()
        print('Чтение Slave 4 завершено')

    @staticmethod
    def universal_list_update(regs_list: List,
                              ui_items_list: QListView) -> None:
        """Метод обновляющий список чего-нибудь."""
        items_model = QStandardItemModel()
        for i in regs_list:
            item = QStandardItem(str(i))
            item.setEditable(False)
            items_model.appendRow(item)
        ui_items_list.setModel(items_model)

    def read_registers_list_update(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            self.slave1.data,
            self.ui.ReadRegisters)

    def read_registers_list_update_2(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            self.slave2.data,
            self.ui.ReadRegisters_2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
