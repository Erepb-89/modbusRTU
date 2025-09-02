import os
import sys
from threading import Thread
from typing import List

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QListView

from ui.main_window import Ui_MainWindow
from ui.params_dialog import Ui_ParamsDialog
from ui.params_dialog_2 import Ui_ParamsDialog_2
from ui.params_dialog_3 import Ui_ParamsDialog_3
from ui.params_dialog_4 import Ui_ParamsDialog_4
from ui.write_single_dialog import Ui_WriteRegDialog
from ui.write_single_dialog_2 import Ui_WriteRegDialog_2
from ui.write_single_dialog_3 import Ui_WriteRegDialog_3
from ui.write_single_dialog_4 import Ui_WriteRegDialog_4
from visual_model import VisualModel


class MainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    """

    def __init__(self):
        super().__init__()
        # основные переменные
        self.name = 'ClientMainWindow'
        self.v_model = VisualModel()
        # self.v_model.connect_port()
        self.ui_dict = {}

        self.InitUI()

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonConnect.clicked.connect(self.v_model.create_slaves)

        self.ui.pushButtonStartPolling.clicked.connect(self.start_polling)
        self.ui.pushButtonStopPolling.clicked.connect(self.stop_polling)

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

        self.ui_dict = {
            "slave1": self.ui.pushButtonWriteReg,
            "slave2": self.ui.pushButtonWriteReg_2,
            "slave3": self.ui.pushButtonWriteReg_3,
            "slave4": self.ui.pushButtonWriteReg_4,
        }

        self.check_slave_availability(self.v_model.slave1, "slave1")
        self.check_slave_availability(self.v_model.slave2, "slave2")
        self.check_slave_availability(self.v_model.slave3, "slave3")
        self.check_slave_availability(self.v_model.slave4, "slave4")

        self.show()

    def check_slave_availability(self, slave, slave_name):
        if slave.err:
            self.ui.pushButtonStartPolling.setEnabled(False)
            self.ui_dict.get(slave_name).setEnabled(False)
            self.ui.LabelMessage.setText(slave.err)
        else:
            self.ui.pushButtonStartPolling.setEnabled(True)
            self.ui_dict.get(slave_name).setEnabled(True)

    def closeEvent(self, event) -> None:
        """Закрытие всех окон по выходу из главного"""
        self.v_model.running_read.clear()
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
            self.ui.LabelMessage_5.setText(self.json_path)
            self.ui.pushButtonLoadParams.setEnabled(True)
        else:
            self.ui.LabelMessage_5.setText("Выберите JSON файл")

    def load_json_params(self):
        self.v_model.load_json_params(self.json_path)

        self.ui.pushButtonStartPolling.setEnabled(True)
        self.ui.LabelMessage_5.setText("Параметры загружены")

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

    def start_polling(self):
        self.v_model.start_polling()

        self.ui.pushButtonStartPolling.setEnabled(False)
        self.ui.pushButtonStopPolling.setEnabled(True)

        # ui_items_list.model().layoutChanged.emit()
        # self.ui.ReadRegisters_2.model().dataChanged.connect(self.on_data_changed)
        self.on_data_changed()

    def on_data_changed(self):
        self.read_registers_list_update()
        self.read_registers_list_update_2()
        self.read_registers_list_update_3()
        self.read_registers_list_update_4()

    def write_register(self):
        try:
            self.v_model.slave1.write()

            self.ui.LabelMessage.setText("Запись в slave 1 успешно произведена")
        except Exception as err:
            self.ui.LabelMessage.setText(str(err))

    def write_register_2(self):
        try:
            self.v_model.slave2.write()

            self.ui.LabelMessage_2.setText("Запись в slave 2 успешно произведена")
        except Exception as err:
            self.ui.LabelMessage_2.setText(str(err))

    def write_register_3(self):
        try:
            self.v_model.slave3.write()

            self.ui.LabelMessage_3.setText("Запись в slave 3 успешно произведена")
        except Exception as err:
            self.ui.LabelMessage_3.setText(str(err))

    def write_register_4(self):
        try:
            self.v_model.slave4.write()

            self.ui.LabelMessage_4.setText("Запись в slave 4 успешно произведена")
        except Exception as err:
            self.ui.LabelMessage_4.setText(str(err))

    def stop_polling(self):
        self.v_model.stop_polling()

        self.ui.pushButtonStartPolling.setEnabled(True)
        self.ui.pushButtonStopPolling.setEnabled(False)

    def universal_list_update(self,
                              regs_list: List,
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
            self.v_model.slave1.data,
            self.ui.ReadRegisters)

    def read_registers_list_update_2(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            self.v_model.slave2.data,
            self.ui.ReadRegisters_2)

    def read_registers_list_update_3(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            self.v_model.slave3.data,
            self.ui.ReadRegisters_3)

    def read_registers_list_update_4(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            self.v_model.slave4.data,
            self.ui.ReadRegisters_4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
