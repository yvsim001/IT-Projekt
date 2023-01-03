from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFrame
#from basis_code import *


class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setObjectName("main")
        # groupbox
        self.box_one = QGroupBox()
        self.box_two = QGroupBox()
        # button
        self.btn_one = QPushButton(text="Open")
        self.btn_two = QPushButton(text="Close")
        self.btn_one.setMinimumHeight(25)
        self.btn_two.setMinimumHeight(25)
        # lay btn
        self.lay_one = QVBoxLayout()
        self.lay_two = QVBoxLayout()
        # frame
        self.frame_temp = QFrame()
        self.frame_temp.setObjectName("temp")
        self.frame_luft = QFrame()
        self.frame_luft.setObjectName("luft")
        self.frame_state = QFrame()
        self.frame_state.setObjectName("state")
        # label
        self.lab_temp = QLabel("Temperatur")
        self.val_temp = QLabel("39")
        self.lab_luft = QLabel("Luftfeuchtigkeit")
        self.val_luft = QLabel("40")
        self.lab_state = QLabel("State")
        self.val_state = QLabel("Etat")
        self.lab_temp.setAlignment(Qt.AlignCenter)
        self.val_temp.setAlignment(Qt.AlignCenter)
        self.lab_luft.setAlignment(Qt.AlignCenter)
        self.val_luft.setAlignment(Qt.AlignCenter)
        self.lab_state.setAlignment(Qt.AlignCenter)
        self.val_state.setAlignment(Qt.AlignCenter)
        # lay
        self.main_lay = QVBoxLayout()
        self.group_lay = QHBoxLayout()
        self.frame_lay = QHBoxLayout()
        self.frame_temp_lay = QVBoxLayout()
        self.frame_luft_lay = QVBoxLayout()
        self.frame_state_lay = QVBoxLayout()
        # timer
        self.timer = QTimer()
        self.timer.start(1000)
        # connect
        self.timer.timeout.connect(self.set_temp_hum)
        #self.btn_one.clicked.connect()
        #self.btn_two.clicked.connect(ledwater)
        self.setup_ui()
        self.ss()

    def setup_ui(self):
        print("ok")
        # box one
        self.box_one.setTitle("Door open")
        self.lay_one.addWidget(self.btn_one)
        self.box_one.setLayout(self.lay_one)
        # box two
        self.box_two.setTitle("Door close")
        self.lay_two.addWidget(self.btn_two)
        self.box_two.setLayout(self.lay_two)
        # group lay
        self.group_lay.addWidget(self.box_one)
        self.group_lay.addWidget(self.box_two)
        # frame one
        self.frame_temp_lay.addWidget(self.lab_temp)
        self.frame_temp_lay.addWidget(self.val_temp)
        # frame two
        self.frame_luft_lay.addWidget(self.lab_luft)
        self.frame_luft_lay.addWidget(self.val_luft)
        self.frame_luft_lay.setContentsMargins(0, 0, 0, 9)
        self.frame_temp_lay.setContentsMargins(0, 0, 0, 9)
        self.frame_state_lay.setContentsMargins(0, 0, 0, 9)
        # frame one
        self.frame_state_lay.addWidget(self.lab_state)
        self.frame_state_lay.addWidget(self.val_state)
        # frame lay
        self.frame_temp.setLayout(self.frame_temp_lay)
        self.frame_luft.setLayout(self.frame_luft_lay)
        self.frame_state.setLayout(self.frame_state_lay)
        self.frame_lay.addWidget(self.frame_temp)
        self.frame_lay.addWidget(self.frame_luft)
        self.frame_lay.addWidget(self.frame_state)
        # main
        # self.main_lay.addLayout(self.group_lay)
        self.main_lay.addLayout(self.frame_lay)
        self.setLayout(self.main_lay)

    def set_temp_hum(self):
        self.val_luft.clear()
        self.val_luft.setText("Humidity: %-3.1f %%" % result.humidity)
        self.val_temp.clear()
        self.val_temp.setText("Temperature: %-3.1f C" % result.temperature)
        self.val_state.clear()
        self.val_state.setText(door_state)

    def ss(self):
        self.setStyleSheet("""
QWidget#main{
background-color: #563e7c;
} 
QFrame#temp
{
background-color: #322448;
border: 4px solid #322448;
border-radius: 8px;
}    
QFrame#state
{
background-color: #322448;
border: 4px solid #322448;
border-radius: 8px;
}    
QFrame#luft
{
background-color: #322448;
border: 4px solid #322448;
border-radius: 8px;
}        
QPushButton{
font: 10pt "MS Shell Dlg 2";
background-color: #322448;
color: white;
font-weight: bold;
border:none;
padding: 5px;
border-radius: 12px;
}
QPushButton:hover{
background-color: rgb(35, 25, 50);
}
QPushButton:pressed{
background-color:background-color: rgb(35, 25, 50);
}
QGroupBox
{
font: 75 13pt "MS Shell Dlg 2";
border: none;
}

""")
        self.box_one.setStyleSheet("""
 QGroupBox {
     border: 3px solid #322448;
     border-radius: 5px;
     margin-top: 3ex; /* leave space at the top for the title */
padding: 2px;
	font: 75 13pt "MS Shell Dlg 2";
color: white;
 }

 QGroupBox::title {
     subcontrol-origin: margin;
     subcontrol-position: top center; /* position at the top center */
     padding: 0 3px;
  
 }""")
        self.box_two.setStyleSheet("""
 QGroupBox {
     border: 3px solid #322448;
     border-radius: 5px;
     margin-top: 3ex; /* leave space at the top for the title */
padding: 2px;
	font: 75 13pt "MS Shell Dlg 2";
color: white;
 }

 QGroupBox::title {
     subcontrol-origin: margin;
     subcontrol-position: top center; /* position at the top center */
     padding: 0 3px;
  
 }""")
        self.lab_temp.setStyleSheet("""background-color: #563e7c;
font: 10pt "MS Shell Dlg 2";
font-weight: bold;""")
        self.lab_luft.setStyleSheet("""background-color: #563e7c;
font: 10pt "MS Shell Dlg 2";
font-weight: bold;""")
        self.lab_state.setStyleSheet("""background-color: #563e7c;
font: 10pt "MS Shell Dlg 2";
font-weight: bold;""")
        self.val_luft.setStyleSheet("""font: 10pt "MS Shell Dlg 2";
color: white;
font-weight: bold;""")
        self.val_temp.setStyleSheet("""font: 10pt "MS Shell Dlg 2";
color: white;
font-weight: bold;""")
        self.val_state.setStyleSheet("""font: 10pt "MS Shell Dlg 2";
color: white;
font-weight: bold;""")



app = QApplication([])

main = MainWin()
main.show()

app.exec()
