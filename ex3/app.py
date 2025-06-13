import os
import sys

# Установка пути к Qt плагинам
qt_plugin_path = os.path.join(
    sys.prefix, "Lib", "site-packages", "PyQt5", "Qt5", "plugins"
)
os.environ["QT_PLUGIN_PATH"] = qt_plugin_path

from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex, QVariant
from PyQt5.QtWidgets import (
    QStyledItemDelegate,
    QLineEdit,
    QApplication,
    QMainWindow,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


# Класс узла дерева, который хранит данные и ссылки на потомков и родителя
class TreeNode:
    def __init__(self, data, parent=None):
        self.parent = parent
        self.children = []
        self.data = data


# Модель, наследуемая от QAbstractItemModel для поддержки иерархических данных
class TreeModel(QAbstractItemModel):
    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.root = TreeNode(["Root"])
        self.headers = headers

    # Основные методы модели
    # Возвращает количество колонок (по числу заголовков)
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    # Возвращает количество дочерних элементов у заданного родителя
    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            parent_node = parent.internalPointer()
            return len(parent_node.children)
        return len(self.root.children)

    # Возвращает индекс дочернего элемента по строке и колонке
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_node = self.root if not parent.isValid() else parent.internalPointer()
        child = parent_node.children[row]
        return self.createIndex(row, column, child)

    # Возвращает индекс родителя для заданного индекса
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child = index.internalPointer()
        parent = child.parent

        if parent == self.root:
            return QModelIndex()

        return self.createIndex(parent.parent.children.index(parent), 0, parent)

    # Возвращает данные для отображения или редактирования
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        node = index.internalPointer()
        col = index.column()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return node.data[col] if col < len(node.data) else QVariant()

        return QVariant()

    # Устанавливает новые данные в модель по индексу
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole and index.isValid():
            node = index.internalPointer()
            node.data[index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    # Возвращает заголовки колонок
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return QVariant()

    # Устанавливает флаги (разрешаем редактирование)
    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable


# Делегат для редактирования ячеек через QLineEdit
class TreeItemDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return QLineEdit(parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())


# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Модель с заголовками
        self.model = TreeModel(["Отдел", "Номер отдела"])

        # Добавляем тестовые данные
        root = self.model.root
        child1 = TreeNode(["IT отдел", "1"], root)
        child2 = TreeNode(["Отдел продаж", "2"], root)
        child1.children.append(TreeNode(["Отдел разработки", "1.1"], child1))
        child1.children.append(TreeNode(["Отдел верификации", "1.2"], child1))
        root.children = [child1, child2]

        # Настраиваем TreeView
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setItemDelegate(TreeItemDelegate())
        self.tree.expandAll()

        # Настройка главного окна
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("Структура компании")
        self.resize(600, 400)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
