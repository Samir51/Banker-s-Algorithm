from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, \
    QPushButton, QRadioButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QGroupBox
import sys
import numpy as np

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()

        resources = QLabel('Resources number:')
        resources.setStyleSheet("font-size: 14pt")
        self.resources_textbox = (QLineEdit(self))
        self.resources_textbox.setStyleSheet("font-size: 14pt")
        self.resources_textbox.returnPressed.connect(lambda: self.handle_return(self.processes_textbox))

        processes = QLabel('Processes number:')
        processes.setStyleSheet("font-size: 14pt")
        self.processes_textbox = (QLineEdit(self))
        self.processes_textbox.setStyleSheet("font-size: 14pt")

        self.button = QPushButton("Next", self)
        self.button.setStyleSheet("font-size: 12pt")
        self.button.clicked.connect(self.next)

        self.setGeometry(600, 300, 400, 200)
        self.setWindowTitle("Banker's Algorithm")

        vbox = QVBoxLayout()
        vbox.addWidget(resources) 
        vbox.addWidget(self.resources_textbox)

        vbox.addWidget(processes)
        vbox.addWidget(self.processes_textbox)
        
        vbox.addWidget(self.button)

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(vbox)
        self.show()

    def handle_return(self, widget):
        widget.setFocus()
    
    def next(self):

        nresources = self.resources_textbox.text()
        nprocesses = self.processes_textbox.text()

        if nprocesses.isdigit() and nresources.isdigit():
            if int(nprocesses) > 0 and int(nresources) > 0 :
                arr1 = np.full((int(nprocesses), int(nresources)), -1,dtype=int)
                arr2 = np.full((int(nprocesses), int(nresources)), -1,dtype=int)
                arr3 = np.full((1, int(nresources)), -1,dtype=int)
                self.second_window = Window(int(nresources), int(nprocesses), arr1, arr2, arr3)
                self.second_window.show()
                self.close()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Input must be greater than Zero!")
                msg.setWindowTitle("Warning!")
                msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Input must be integer!")
            msg.setWindowTitle("Warning!")
            msg.exec_()


class Window(QMainWindow):
    def __init__(self, n, m, current, max, total):
        super().__init__()

        self.nresources = n
        self.nprocesses = m
        self.current_allocation = current
        self.maximum_need = max
        self.total_resources = total

        if self.maximum_need.min()>-1:
            self.arr = self.total_resources
            self.l = "Total Resources:"
            self.window_number = 3

        elif self.current_allocation.min()>-1:
            self.arr = self.maximum_need
            self.l = "Maximum Need:"
            self.window_number = 2

        else:
            self.arr = self.current_allocation
            self.l = "Current Allocation:"
            self.window_number = 1

        self.label = QLabel(self.l)
        self.label.setStyleSheet("font-size: 14pt")
   
        submit_button = QPushButton('Submit', self)
        submit_button.setStyleSheet("font-size: 12pt")
        submit_button.clicked.connect(self.submit_inputs)

        vbox = QVBoxLayout()

        vbox.addWidget(self.label)

        self.setGeometry(500, 100, 600, 600)
        self.setWindowTitle("Banker's Algorithm")

        self.table = QTableWidget()
        
        self.table.setStyleSheet("QTableView { color: black; border: solid black;font-size: 24pt;}\
                    QHeaderView::section { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, \
                                 stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565); \
                        color: white; border: solid gray; padding-left: 2px; font-size: 24pt;} ")

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setRowCount(self.nprocesses)
        self.table.setColumnCount(self.nresources)

        ph = []
        for i in range(self.nprocesses):
            ph.append("P"+str(i))
        if self.window_number == 3 :
            ph = ["Total"]
        self.table.setVerticalHeaderLabels(ph)

        rh = []
        for i in range(self.nresources):
            rh.append("R"+str(i))
        self.table.setHorizontalHeaderLabels(rh)

        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        
        vbox.addWidget(self.table)

        vbox.addWidget(submit_button)

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(vbox)
        self.show()
        
        self.table.cellChanged.connect(self.cell_edited)

    def cell_edited(self, row, column):
        
        self.table.item(row, column).setTextAlignment(Qt.AlignCenter)
        item = self.table.item(row, column).text()

        if item.isdigit(): 
            self.arr[row][column] = int(item)
           
        else:
            self.arr[row][column] = -1

        #print(f"Current state of array:\n{self.arr}")

    
    def submit_inputs(self):
        if self.arr.min()<0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Wrong input!")
            msg_box.setWindowTitle("Warning!")
            msg_box.exec_()
        else:
            if self.window_number == 1:
                self.next_window = Window(self.nresources, self.nprocesses, self.arr, self.maximum_need, self.total_resources)
            elif self.window_number == 2:
                self.next_window = Window(self.nresources, 1, self.current_allocation, self.arr, self.total_resources)
            else:
                self.next_window = Request(self.current_allocation, self.maximum_need, self.arr)
            self.next_window.show()
            self.close()


class Request(QWidget):
    def __init__(self, current_allocation, maximum_need, total_resources):
        super().__init__()

        self.current_allocation = current_allocation
        self.maximum_need = maximum_need
        self.total_resources = total_resources

        self.setGeometry(500, 200, 600, 300)
        self.setWindowTitle("Banker's Algorithm")

        group_box1 = QGroupBox("Processes")
        group_box1.setStyleSheet("font-size: 14pt")
        group_box2 = QGroupBox("Resources")
        group_box2.setStyleSheet("font-size: 14pt")

        self.radio_group1 = []
        for i in range(len(current_allocation)):
            self.radio_group1.append(QRadioButton("P"+str(i)))
            self.radio_group1[i].setStyleSheet("font-size: 14pt")
        self.radio_group1[0].setChecked(True)

        hbox1 = QHBoxLayout()
        for radio_button in self.radio_group1:
            hbox1.addWidget(radio_button)
        group_box1.setLayout(hbox1)

        self.radio_group2 = []
        for i in range(len(total_resources[0])):
            self.radio_group2.append(QRadioButton("R"+str(i)))
            self.radio_group2[i].setStyleSheet("font-size: 14pt")
        self.radio_group2[0].setChecked(True)

        hbox2 = QHBoxLayout()
        for radio_button in self.radio_group2:
            hbox2.addWidget(radio_button)
        group_box2.setLayout(hbox2)

        label = QLabel("Number of requested resource:")
        label.setStyleSheet("font-size: 14pt")

        self.textbox = (QLineEdit(self))
        self.textbox.setStyleSheet("font-size: 14pt")

        next_button = QPushButton("Next")
        next_button.setStyleSheet("font-size: 14pt")
        next_button.clicked.connect(self.next)

        vbox = QVBoxLayout()
        vbox.addWidget(group_box1)
        vbox.addWidget(group_box2)
        vbox.addWidget(label)
        vbox.addWidget(self.textbox)
        vbox.addWidget(next_button)
        self.setLayout(vbox)

    def next(self):
        if self.textbox.text().isdigit():

            num = int(self.textbox.text())
            raw = 0
            column = 0

            for i in range(len(self.radio_group1)):
                if self.radio_group1[i].isChecked():
                    raw = i
                    break

            for i in range(len(self.radio_group2)):
                if self.radio_group2[i].isChecked():
                    column = i
                    break

            #print(self.current_allocation)
            self.current_allocation[raw][column] += num
            #print(self.current_allocation)
            self.next_window = Banker(self.current_allocation, self.maximum_need, self.total_resources)
            self.next_window.show()
            self.close()
           
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Input must be integer!")
            msg.setWindowTitle("Warning!")
            msg.exec_()
                   

class Banker(QMainWindow):
    def __init__(self, current_allocation, maximum_need, total_resources):
        super().__init__()

        used_resources = np.sum(current_allocation, axis=0)
        available_resources = total_resources[0] - used_resources 
        available_update = [available_resources.copy()]

        need = maximum_need - current_allocation

        finish_process = np.zeros(len(current_allocation), dtype=bool)
        safe_sequence = []
        flag = [False, False]

        current_allocation_len = len(current_allocation)
        while True:
            if flag[0]:
                j = safe_sequence[len(safe_sequence)-1] + 1
                flag = [False, True]
            else:
                j = 0
            index = None
            for i in range(j, current_allocation_len):
                if not finish_process[i] and np.all(need[i] <= available_resources):
                    index = i
                    break
            if index is not None:
                safe_sequence.append(index)
                available_resources += current_allocation[index]
                available_update.append(available_resources.copy())
                finish_process[index] = True
                flag = [True, False]
            elif flag[1]:
                flag = [False, False]
            else:
                break

        # while True:                               ################  other way
        #     indices = np.where(~finish_process & np.all(need <= available_resources, axis=1))[0]
        #     if len(indices) == 0:
        #         break
        
        #     safe_sequence.extend(indices)
            
        #     for i in indices:
        #         available_resources += current_allocation[i]
        #         available_update.append(available_resources.copy())
            
        #     finish_process[indices] = True


        if np.all(finish_process):
            out = "Safe Sequence"
            oColor = "color: green;"
        else:
            out = "Not Safe"
            oColor = "color: red;"
        
        for i in safe_sequence:
            out = out + " -> P" + str(i)

        self.setGeometry(500, 100, 600, 600)
        self.setWindowTitle("Banker's Algorithm")

        table = QTableWidget()
        
        table.setStyleSheet("QTableView { color: black; border: solid black;font-size: 24pt;}\
                    QHeaderView::section { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, \
                                 stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565); \
                        color: white; border: solid gray; padding-left: 2px; font-size: 24pt;} ")

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setRowCount(len(available_update))
        table.setColumnCount(len(available_update[0]))

        vl = []
        for i in range(len(available_update)):
            vl.append("Iteration"+str(i))
        table.setVerticalHeaderLabels(vl)

        hl = []
        for i in range(len(available_update[0])):
            hl.append("R"+str(i))
        table.setHorizontalHeaderLabels(hl)

        for i in range(len(available_update)):
            for j in range(len(available_update[0])):
                item = QTableWidgetItem(str(available_update[i][j]))
                table.setItem(i, j, item)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)

        label = QLabel("Available Resources in each Iteration:")
        label.setStyleSheet("font-size: 14pt")

        label2 = QLabel(out)
        label2.setStyleSheet("font-size: 20pt;"+oColor)

        button = QPushButton("Done", self)
        button.setStyleSheet("font-size: 12pt")
        button.clicked.connect(self.next)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(table)
        vbox.addWidget(label2)
        vbox.addWidget(button)

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(vbox)
        self.show()

    def next(self):
        self.window1 = Window1()
        self.window1.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window1()
    sys.exit(app.exec_())