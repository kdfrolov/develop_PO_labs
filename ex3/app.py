import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QBrush, QColor

class ShoppingItem:
    def __init__(self, name, quantity, price, category):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.quantity} x {self.price:.2f}) - {self.category}"


class ShoppingListModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data  # List of ShoppingItem objects

    def rowCount(self, parent=QModelIndex()):
        return len(self.data) if parent.isValid() == False else 0

    def columnCount(self, parent=QModelIndex()):
        return 4  # Name, Quantity, Price, Category

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        item = self.data[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return QVariant(item.name)
            elif col == 1:
                return QVariant(item.quantity)
            elif col == 2:
                return QVariant(item.price)
            elif col == 3:
                return QVariant(item.category)

        elif role == Qt.BackgroundRole and item.quantity <= 1:
            return QVariant(QBrush(QColor("yellow"))) # highlight low quantity

        return QVariant()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return QVariant("Name")
            elif section == 1:
                return QVariant("Quantity")
            elif section == 2:
                return QVariant("Price")
            elif section == 3:
                return QVariant("Category")
        return QVariant()

    def index(self, row, column, parent):
        if parent.isValid() or row < 0 or row >= self.rowCount() or column < 0 or column >= self.columnCount():
            return QModelIndex()
        return self.createIndex(row, column, self.data[row])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.treeView = QTreeView()
        self.setCentralWidget(self.treeView)

        # Sample data
        self.shopping_list = [
            ShoppingItem("Milk", 2, 2.5, "Dairy"),
            ShoppingItem("Eggs", 12, 3.0, "Dairy"),
            ShoppingItem("Bread", 1, 2.0, "Bakery"),
            ShoppingItem("Apples", 5, 4.0, "Fruits"),
        ]

        model = ShoppingListModel(self.shopping_list)
        self.treeView.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
