import sys
import sqlite3
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QAbstractTableModel

class MitarbeiterModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["ID", "Vorname", "Nachname"][section]
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mitarbeiter-Tabelle")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        
        self.table = QTableView()
        data = self.fetch_data_from_db()
        self.model = MitarbeiterModel(data)
        self.table.setModel(self.model)
        
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def fetch_data_from_db(self):
        
        db_path = './T1_Kunden_Mitarbeiter.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM C_Mitarbeiter")
        rows = cursor.fetchall()
        conn.close()
        return rows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())