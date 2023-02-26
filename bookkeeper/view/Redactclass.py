import sys 

from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui
from redactmenu import RedactMenu,CommentMenu


class label_widget(QtWidgets.QWidget):
    def __init__(self,text,widget,percentage, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.h1 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.widg = widget
        self.h1.addWidget(self.label, percentage)
        self.h1.addWidget(self.widg, 10 - percentage)
        self.setLayout(self.h1)
    
def two_widgets_near(widgetone:QtWidgets.QLayout, widgettwo:QtWidgets.QWidget, percentage:float) -> QtWidgets.QHBoxLayout:
    h1 = QtWidgets.QHBoxLayout()
    h1.addWidget(widgetone, percentage)
    h1.addWidget(widgettwo, 10 - percentage)
    return h1
    
    
class MainTable(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(4)
        self.setRowCount(1)
        self.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
        self.setWindowTitle("Последние расходы")
        self.cur_row = 0
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        
            
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        
    def fill_data(self, data:list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(
                    i, j, 
                    QtWidgets.QTableWidgetItem(x.capitalize())
                    )
        self.cur_row += len(data)
        
    def fill_row(self, data:list[str]):
        for j, element in enumerate(data):
            self.setItem(
                self.cur_row, j,
                QtWidgets.QTableWidgetItem(element)
                )
        self.cur_row += 1
        
    def insert_row(self):
        cond = True
        row_count = self.rowCount()
        column_count = self.columnCount()
        for j in range(column_count):
            if self.item(row_count, j) == True:
                cond = False
        if cond == True:
            self.insertRow(row_count)
        
        
        
class BudgetTable(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.setRowCount(3)   
        self.setHorizontalHeaderLabels("Сумма Бюджет".split())
        self.setVerticalHeaderLabels("День Неделя Месяц".split())
        self.setWindowTitle("Бюджет")
        self.cur_row = 0
        self.header = self.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fill_begin_numbers()
            
    def fill_begin_numbers(self):
        budgets = [str(1000), str(7000), str(30000)]
        for i in range(len(budgets)):
            self.setItem(
                i, 1, 
                QtWidgets.QTableWidgetItem(budgets[i])
                )
        
        for i in range(len(budgets)):
            self.setItem(
                i, 0, 
                QtWidgets.QTableWidgetItem(str(0))
                )

        
    	
    	
    
class CatChoice(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.combo = QtWidgets.QComboBox()
        self.addItems(["Продукты", "Электроника", "Косметика", "Одежда", "Учеба"])
        
    def AddItem(self, name):
        self.addItem(name)
        
    def get_cats(self):
        AllItems = [self.itemText(i) for i in range(self.count())]
        return AllItems
    
    def remove_category(self, text):
        for i in range(self.count()):
            if self.itemText(i) == text:
                self.removeItem(i)
                
        
        
    
class RedactField(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        #Поле для записи суммы покупки
        self.sum_field = QtWidgets.QLineEdit()
        self.sum_field.setValidator(QtGui.QDoubleValidator(-999999, 999999, 3))
        self.sum_widg = label_widget("Сумма", self.sum_field, 1)
        self.layout.addWidget(self.sum_widg)
        
        #Управление категориями
        self.combobox = CatChoice()
        self.choicebar = label_widget("Категория", self.combobox, 1)
        self.redbut = QtWidgets.QPushButton(text = "Редактировать")
        
        #Вариант выбора категории
        self.cats = two_widgets_near(self.choicebar, self.redbut, 7)
        self.layout.addLayout(self.cats)
        
        #Кнопка для добавления
        self.addbut = QtWidgets.QPushButton(text = "Добавить")
        self.layout.addWidget(self.addbut)
        
        
    def get_sum(self):
        return self.sum_field.text()
            
    def is_filled(self):
        return bool(self.sum_field.text()) 
        
    def get_category(self):
        return self.combobox.currentText()
        
       
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Данные
        self.data = [ ["13 марта","138.65", "Еда"], ["13 марта","202.3", "Электроника"],
        ["14 марта","345.6", "Косметика"] ]
        
        #главный виджет
        self.main_widget = QtWidgets.QWidget()
        
        #Таблица для внесения расходов
        self.table = MainTable()
        #Таблица для бюджета
        self.budget_table = BudgetTable()
        #Окно редактирования
        self.red_field = RedactField() 
        self.red_field.addbut.clicked.connect(self.open_comment)
        #self.red_field.addbut.clicked.connect(self.fill_in_table)
        self.red_field.redbut.clicked.connect(self.open_categ_menu)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.budget_table)
        self.layout.addWidget(self.red_field)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("The Bookkeeper App")
        
        
    def add_category(self, name):
        self.red_field.combobox.AddItem(name)
    
    def get_comment(self, comment):
        self.comment = comment
        
    #def fill_in_table(self):
    #    self.table.fill_data(self.data)
    
    def insert_table_row(self):
        self.table.insert_row()
        
    def add_row(self):
        row_data = []
        now = datetime.now()
        this_moment = now.strftime("%d/%m/%Y %H:%M:%S")
        row_data.append(this_moment)
        row_data.append(self.red_field.get_sum())
        row_data.append(self.red_field.get_category())
        row_data.append(self.comment)
        self.table.fill_row(row_data)
        
    
    def open_comment(self):
        comment = CommentMenu(self)
        comment.setWindowTitle("Добавление комментария")
        comment.exec()
    
    def open_categ_menu(self):
        menu = RedactMenu(self)
        menu.setWindowTitle("Редактирование списка категорий")
        menu.exec()
        
        
	
app = QtWidgets.QApplication(sys.argv)

window = MyMainWindow()
"""
main_widget = QtWidgets.QWidget()
window.setCentralWidget(main_widget)

table_widget = MainTable()
redact_widget = RedactField()

vertical_layout = QtWidgets.QVBoxLayout()
vertical_layout.addWidget(table_widget)
vertical_layout.addWidget(redact_widget)
main_widget.setLayout(vertical_layout)
window.setWindowTitle('The Bookkeeper App')
print(redact_widget.combobox.width())
print(redact_widget.combobox.height())
print(redact_widget.combobox.geometry())
print(redact_widget.redbut.width())
"""
window.show()
sys.exit(app.exec())