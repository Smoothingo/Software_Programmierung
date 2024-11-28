import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QAbstractTableModel

# MC import (model view controller) is used with many different frameworks aka: django
class MitarbeiterModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data  # Private instance variable to store the data and encapsulate
        # it in the model. This ensures that the data is only accessible through the model's methods.
        # _data is a list of tuples, where each tuple represents a row in the table.
        # The first element of each tuple is the ID of the row, and the second and third elements are the first and last names of the employee, respectively.
        # The data is stored in this format to make it easier to update the database when the user edits the table.
        # The ID is used to identify the row that should be updated, and the first and last names are the values that should be updated.
        #

    def rowCount(self, index):
        # Returns the number of rows in the model.
        # The 'index' parameter is required by the QAbstractTableModel interface but is not used here.
        return len(self._data)

    def columnCount(self, index):
        # Returns the number of columns in the model.
        return len(self._data[0])
        # The column count is determined by the number of elements in the first row of the data.

    def data(self, index, role):
        # Returns the data stored under the given role for the item referred to by the index.
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role):
        # Returns the data for the given role and section in the header with the specified orientation.
        # The section parameter represents the row or column number, depending on the orientation.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["ID", "Vorname", "Nachname"][section]
        return None

    def flags(self, index):
        # Returns the item flags for the given index.
        # This implementation makes the items selectable, enabled, and editable.
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            # Convert the row data to a list to allow modification
            row = list(self._data[index.row()])
            # The index parameter contains the row and column of the cell that was edited.

            # Update the specific cell with the new value
            row[index.column()] = value

            # Convert the row back to a tuple and update the model's data
            self._data[index.row()] = tuple(row)

            # Emit the dataChanged signal to notify views of the change
            # The view relies on the dataChanged signal to know when it
            # needs to refresh its display.
            self.dataChanged.emit(index, index, [Qt.DisplayRole])

            # Commit changes to the database
            self.commit_to_database(index.row(), index.column(), value)

            return True
        return False

    def commit_to_database(self, row, column, value):
        # Establish a new database connection
        conn = sqlite3.connect('mitarbeiter_db.sqlite.db')
        cursor = conn.cursor()

        # Map column index to column name
        column_name = ["ID", "Vorname", "Nachname"][column]
        # The column_name variable is used to map the column index to the corresponding column name in the database.
        # This allows the model to update the correct column in the database when the user edits the table.

        # Update the database with the new value
        # value: The new value that should be set in the specified column.
        # self._data[row][0]:The ID of the row that should be updated. This assumes that the first column
        # (self._data[row][0]) contains the unique ID for each row.

        update_query = f"UPDATE C_Mitarbeiter SET {column_name} = ? WHERE ID = ?"
        cursor.execute(update_query, (value, self._data[row][0]))
        # The update_query variable contains an SQL query that updates the specified column in the C_Mitarbeiter table.
        # The query uses placeholders (?) to prevent SQL injection attacks and ensure that the data is properly escaped.
        # The execute method is called on the cursor object to execute the query with the new value and the ID of the row that should be updated.

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mitarbeiter-Tabelle")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.table = QTableView()
        data = self.fetch_data_from_sqlite()  # Fetch data from the database
        self.model = MitarbeiterModel(data)  # Pass the data to the model
        self.table.setModel(self.model)

        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def fetch_data_from_sqlite(self):
        conn = sqlite3.connect('mitarbeiter_db.sqlite.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Vorname, Nachname FROM C_Mitarbeiter")
        data = cursor.fetchall()
        conn.close()
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
