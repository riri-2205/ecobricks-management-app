from db_2 import crCon, crDb, crTables, crTriggers, closeCon
import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QTabWidget, QTableWidget, QTableWidgetItem, QComboBox, QTextEdit, QGroupBox, QFormLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class UsersTab(QWidget):
    def __init__(self, conn, cursor):
        super().__init__()
        self.conn, self.cursor = conn, cursor
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_group = QGroupBox("Add New User")
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.user_type = QComboBox()
        self.user_type.addItems(["Donator", "Builder"])

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Role:", self.user_type)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Add User")
        self.apply_btn.clicked.connect(self.add_user)
        self.show_btn = QPushButton("Display Users")
        self.show_btn.clicked.connect(self.show_user)

        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.show_btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        usertype = self.user_type.currentText()
        self.cursor.execute("INSERT INTO Users (name, email, phone_no, role) VALUES (%s, %s, %s, %s)", (name, email, phone, usertype))
        self.conn.commit()
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.user_type.setCurrentIndex(0)

    def show_user(self):
        self.cursor.execute("SELECT * FROM Users")
        records = self.cursor.fetchall()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["User_ID", "Name", "Email", "Phone No", "Role", "Registered At"])
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

class InventoryTab(QWidget):
    def __init__(self, conn, cursor):
        super().__init__()
        self.conn, self.cursor = conn, cursor
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_group = QGroupBox("Add Inventory Record")
        form_layout = QFormLayout()

        self.user_id_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(['Select Plastic Type', 'PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS', 'Other'])
        self.type_input.setCurrentIndex(0)
        

        form_layout.addRow("User ID:", self.user_id_input)
        form_layout.addRow("Weight:", self.weight_input)
        form_layout.addRow("Plastic type:", self.type_input)
        form_group.setLayout(form_layout)

        layout.addWidget(form_group)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add to Inventory")
        self.add_btn.clicked.connect(self.add_inventory)
        self.show_btn = QPushButton("Display Inventory")
        self.show_btn.clicked.connect(self.show_inventory)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.show_btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.total_ecobricks=QTextEdit()
        self.total_btn=QPushButton("Show Total Eocbricks")
        self.total_btn.clicked.connect(self.total_cnt)

        layout.addWidget(self.total_btn)
        layout.addWidget(self.total_ecobricks)

        self.type_btn=QPushButton("View Ecobricks by Plastic Type")
        self.type_btn.clicked.connect(self.cnt_by_type)
        layout.addWidget(self.type_btn)
        self.cnt_table=QTableWidget()
        layout.addWidget(self.cnt_table)


        self.setLayout(layout)

    def add_inventory(self):
        user_id = self.user_id_input.text()
        weight = self.weight_input.text()
        type = self.type_input.currentText()
        self.cursor.execute("INSERT INTO Inventory (user_id, weight, plastic_type) VALUES (%s, %s, %s)", (user_id, weight,type))
        self.conn.commit()
        self.user_id_input.clear()
        self.weight_input.clear()
        self.type_input.setCurrentIndex(0)

    def show_inventory(self):
        self.cursor.execute("SELECT * FROM Inventory")
        records = self.cursor.fetchall()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Inventory_ID", "User_ID", "Weight", "Plastic type"])
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def total_cnt(self):
        self.total_ecobricks.clear()
        self.cursor.execute("Select value from global_variables where name='total_ecobricks' ;")
        result=self.cursor.fetchone()[0]
        if result:
            self.total_ecobricks.append(f"Total ecobricks in the inventory is: {float(result)}")

    def cnt_by_type(self):
        self.cursor.execute("""select plastic_type, sum(weight) from inventory group by plastic_type""")
        records=self.cursor.fetchall()
        self.cnt_table.setRowCount(len(records))
        self.cnt_table.setColumnCount(2)
        self.cnt_table.setHorizontalHeaderLabels([ "Plastic type", "Weight"])
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.cnt_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))






class ProjectsTab(QWidget):
    def __init__(self, conn, cursor):
        super().__init__()
        self.conn, self.cursor = conn, cursor
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_group = QGroupBox("Add New Project")
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.user_id_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Environmental", "Medical", "Social", "Economic", "Other"])
        self.urgency_input = QComboBox()
        self.urgency_input.addItems(["Immediate", "Short-term", "Medium-term", "Long-term", "None"])

        form_layout.addRow("Project Name:", self.name_input)
        form_layout.addRow("User ID:", self.user_id_input)
        form_layout.addRow("Weight:", self.weight_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Urgency:", self.urgency_input)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Project")
        self.add_btn.clicked.connect(self.add_project)
        self.show_btn = QPushButton("Display Projects")
        self.show_btn.clicked.connect(self.show_projects)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.show_btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_project(self):
        name = self.name_input.text()
        user_id = self.user_id_input.text()
        weight = self.weight_input.text()
        category = self.category_input.currentText()
        urgency = self.urgency_input.currentText()
        self.cursor.execute("INSERT INTO Projects (project_name, user_id, weight, category, urgency) VALUES (%s, %s, %s, %s, %s)", (name, user_id, weight, category, urgency))
        self.conn.commit()
        self.name_input.clear()
        self.user_id_input.clear()
        self.weight_input.clear()
        self.category_input.setCurrentIndex(0)
        self.urgency_input.setCurrentIndex(0)

    def show_projects(self):
        self.cursor.execute("SELECT * FROM Projects")
        records = self.cursor.fetchall()
        self.table.setRowCount(len(records))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Project ID", "Project Name", "User ID", "Weight", "Status", "Category", "Urgency", "Priority Score"])
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

class RewardsTab(QWidget):
    def __init__(self, conn, cursor):
        super().__init__()
        self.conn, self.cursor = conn, cursor
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        form_group = QGroupBox("Reward Points Calculator")
        form_layout = QFormLayout()
        self.user_input = QLineEdit()
        form_layout.addRow("User ID:", self.user_input)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        self.find_btn = QPushButton("Calculate Reward Points")
        self.find_btn.clicked.connect(self.calculate_reward_points)
        layout.addWidget(self.find_btn)

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display)

        self.setLayout(layout)

    def calculate_reward_points(self):
        id = self.user_input.text()
        if id.isdigit():
            self.cursor.execute(f"CALL reward_points({int(id)}, @points);")
            self.cursor.execute("SELECT @points AS points")
            points = self.cursor.fetchone()
            self.display.setText(f"Reward Points for user {int(id)}: {float(points[0])}")
            self.user_input.clear()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.conn, self.cursor = crDb()
        crTables(self.conn, self.cursor)
        crTriggers(self.conn, self.cursor)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        title = QLabel("Ecobricks Management System")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2C3E50; margin-bottom: 15px;")

        self.tabs = QTabWidget()
        self.tabs.addTab(UsersTab(self.conn, self.cursor), "Users")
        self.tabs.addTab(InventoryTab(self.conn, self.cursor), "Inventory")
        self.tabs.addTab(ProjectsTab(self.conn, self.cursor), "Projects")
        self.tabs.addTab(RewardsTab(self.conn, self.cursor), "Rewards")

        layout.addWidget(title)
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.setWindowTitle("NITK IT252 Minor Project")
        self.resize(800, 500)

    def closeEvent(self, event):
        closeCon(self.conn, self.cursor)
        event.accept()

if __name__=="__main__":
    
    app=QApplication(sys.argv)
    ex=MyApp()
    ex.show()
    sys.exit(app.exec())
