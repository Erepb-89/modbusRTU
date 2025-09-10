import sys
from threading import Thread
from typing import List

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QListView

from ui.main_window import Ui_MainWindow
from ui.params_dialog import Ui_ParamsDialog
from ui.write_single_dialog import Ui_WriteRegDialog
from visual_model import v_model


class CustomListModel(QAbstractListModel):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return None

        if role == Qt.DisplayRole:
            return self._data[index.row()]

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return False

        if role == Qt.EditRole:
            self._data[index.row()] = value
            # Important: emit signal dataChanged on data change
            self.dataChanged.emit(index, index, role)
            return True

        return False


class MainWindow(QMainWindow):
    """
    Класс - основное окно пользователя.
    """

    def __init__(self, parent):
        super().__init__(parent=None)
        # основные переменные
        self.parent = parent

        self.InitUI()

        # self.items_model.dataChanged.connect(self.update_read_data)

    def InitUI(self):
        """Загружаем конфигурацию окна из дизайнера"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButtonConnect.clicked.connect(v_model.create_slaves)

        self.ui.pushButtonStartPolling.clicked.connect(self.start_polling)
        self.ui.pushButtonStopPolling.clicked.connect(self.stop_polling)

        self.ui.pushButtonChooseJSON.clicked.connect(self.open_json_dialog)
        self.ui.pushButtonLoadParams.clicked.connect(self.load_json_params)

        self.ui.pushButtonSlave1Settings.clicked.connect(
            self.open_params_dialog_1)
        self.ui.pushButtonSlave2Settings.clicked.connect(
            self.open_params_dialog_2)
        self.ui.pushButtonSlave3Settings.clicked.connect(
            self.open_params_dialog_3)
        self.ui.pushButtonSlave4Settings.clicked.connect(
            self.open_params_dialog_4)

        self.ui.pushButtonWriteReg.clicked.connect(self.open_write_dialog_1)
        self.ui.pushButtonWriteReg_2.clicked.connect(self.open_write_dialog_2)
        self.ui.pushButtonWriteReg_3.clicked.connect(self.open_write_dialog_3)
        self.ui.pushButtonWriteReg_4.clicked.connect(self.open_write_dialog_4)

        self.ui.pushButtonConnect.clicked.connect(self.create_client)

        self.ui.pushButtonLoadParams.setEnabled(False)
        self.ui.pushButtonStopPolling.setEnabled(False)

        self.check_start_button_availability()
        self.check_main_client_availability()

        self.ui.checkBoxPolling.setChecked(v_model.chosen_slave_1)
        self.ui.checkBoxPolling_2.setChecked(v_model.chosen_slave_2)
        self.ui.checkBoxPolling_3.setChecked(v_model.chosen_slave_3)
        self.ui.checkBoxPolling_4.setChecked(v_model.chosen_slave_4)

        self.ui.checkBoxPolling.stateChanged.connect(self.checkbox_polling)
        self.ui.checkBoxPolling_2.stateChanged.connect(self.checkbox_polling_2)
        self.ui.checkBoxPolling_3.stateChanged.connect(self.checkbox_polling_3)
        self.ui.checkBoxPolling_4.stateChanged.connect(self.checkbox_polling_4)

        self.show()

    def checkbox_polling(self):
        v_model.chosen_slave_1 = True if self.ui.checkBoxPolling.isChecked() else False

    def checkbox_polling_2(self):
        v_model.chosen_slave_2 = True if self.ui.checkBoxPolling_2.isChecked() else False

    def checkbox_polling_3(self):
        v_model.chosen_slave_3 = True if self.ui.checkBoxPolling_3.isChecked() else False

    def checkbox_polling_4(self):
        v_model.chosen_slave_4 = True if self.ui.checkBoxPolling_4.isChecked() else False

    def create_client(self):
        v_model.create_client(self)
        self.check_main_client_availability()

    def check_main_client_availability(self):
        if v_model.client is not None:
            # self.ui.pushButtonStartPolling.setEnabled(True)
            if not v_model.client.connected:
                self.ui.pushButtonStartPolling.setEnabled(False)
                self.ui.pushButtonConnect.setEnabled(True)
            else:
                self.ui.pushButtonConnect.setEnabled(False)
        else:
            self.ui.pushButtonStartPolling.setEnabled(False)
            self.ui.pushButtonConnect.setEnabled(True)

    def check_start_button_availability(self):
        if v_model.running_read.is_set():
            self.ui.pushButtonStartPolling.setEnabled(False)
            self.ui.pushButtonStopPolling.setEnabled(True)

            self.update_read_data()
        else:
            self.ui.pushButtonStartPolling.setEnabled(True)
            self.ui.pushButtonStopPolling.setEnabled(False)

    def update_read_data(self):
        try:
            self.read_registers_list_update()
        except Exception as err:
            print(err)
        try:
            self.read_registers_list_update_2()
        except Exception as err:
            print(err)
        try:
            self.read_registers_list_update_3()
        except Exception as err:
            print(err)
        try:
            self.read_registers_list_update_4()
        except Exception as err:
            print(err)

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
        v_model.load_json_params(self.json_path)

        self.ui.pushButtonStartPolling.setEnabled(True)
        self.ui.LabelMessage_5.setText("Параметры загружены")

    def open_params_dialog_1(self):
        try:
            dialog = Ui_ParamsDialog(v_model.slave1, self)
            dialog.exec()  # Открывает диалог модально
        except Exception as err:
            print(err)

    def open_params_dialog_2(self):
        try:
            dialog = Ui_ParamsDialog(v_model.slave2, self)
            dialog.exec()
        except Exception as err:
            print(err)

    def open_params_dialog_3(self):
        try:
            dialog = Ui_ParamsDialog(v_model.slave3, self)
            dialog.exec()
        except Exception as err:
            print(err)

    def open_params_dialog_4(self):
        try:
            dialog = Ui_ParamsDialog(v_model.slave4, self)
            dialog.exec()
        except Exception as err:
            print(err)

    def open_write_dialog_1(self):
        dialog = Ui_WriteRegDialog(v_model.slave1, self)
        dialog.exec()  # Открывает диалог модально

    def open_write_dialog_2(self):
        dialog = Ui_WriteRegDialog(v_model.slave2, self)
        dialog.exec()

    def open_write_dialog_3(self):
        dialog = Ui_WriteRegDialog(v_model.slave3, self)
        dialog.exec()

    def open_write_dialog_4(self):
        dialog = Ui_WriteRegDialog(v_model.slave4, self)
        dialog.exec()

    def start_polling(self):
        v_model.start_polling()

        self.ui.pushButtonStartPolling.setEnabled(False)
        self.ui.pushButtonStopPolling.setEnabled(True)

    def write_register(self):
        self.slave.write(self.ui.LabelMessage)

    def write_register_2(self):
        v_model.slave2.write(self.ui.LabelMessage_2)

    def write_register_3(self):
        v_model.slave3.write(self.ui.LabelMessage_3)

    def write_register_4(self):
        v_model.slave4.write(self.ui.LabelMessage_4)

    def stop_polling(self):
        v_model.stop_polling()

        self.ui.pushButtonStartPolling.setEnabled(True)
        self.ui.pushButtonStopPolling.setEnabled(False)

    def universal_list_update(self,
                              regs_list: List,
                              ui_items_list: QListView) -> None:
        """Метод обновляющий список QListView."""
        items_model = QStandardItemModel()
        for i in regs_list:
            item = QStandardItem(str(i))
            item.setEditable(False)
            items_model.appendRow(item)
        ui_items_list.setModel(items_model)

    def read_registers_list_update(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            v_model.slave1.data.registers,
            self.ui.ReadRegisters)

    def read_registers_list_update_2(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            v_model.slave2.data.registers,
            self.ui.ReadRegisters_2)

    def read_registers_list_update_3(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            v_model.slave3.data.registers,
            self.ui.ReadRegisters_3)

    def read_registers_list_update_4(self) -> None:
        """Обновление регистров на чтение"""
        self.universal_list_update(
            v_model.slave4.data.registers,
            self.ui.ReadRegisters_4)

    # def closeEvent(self, event) -> None:
    #     """Закрытие всех окон по выходу из главного"""
    #     v_model.running_read.clear()
    #     os.sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(None)
    sys.exit(app.exec_())
