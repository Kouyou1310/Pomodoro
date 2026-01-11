from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QFont

from pathlib import Path
import sys
from win10toast import ToastNotifier

notify = ToastNotifier()

class Pomodoro(QWidget):
    def __init__(self):
        super().__init__()

        #time
        self.count = 25 * 60

        #
        self.is_break = False

        #timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)

        #sound effect
        self.sound = QSoundEffect()
        self.sound.setSource(Path("Annoying_Alarm_Clock-UncleKornicob-420925725.wav").absolute().as_uri())
        self.sound.setVolume(0.1)

        #window title & size
        self.setWindowTitle("Pomodoro")
        self.resize(400,300)

        #layout
        layout = QVBoxLayout()

        #displays if work or break
        self.session_label = QLabel(self.sessionChange(), alignment=Qt.AlignCenter)
        self.session_label.setFont(QFont("Arial", 18))
        self.session_label.setStyleSheet("color: #BBBBBB;")
        layout.addWidget(self.session_label)

        #displays time
        self.timer_label = QLabel(self.timeFormat(self.count), alignment=Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 36))
        layout.addWidget(self.timer_label)

        #add or remove 1min
        minute_layout = QHBoxLayout()

        self.plus_button = QPushButton("+ 1min")
        self.plus_button.clicked.connect(self.addMinute)

        self.minus_button = QPushButton("- 1min")
        self.minus_button.clicked.connect(self.removeMinute)

        minute_layout.addWidget(self.plus_button)
        minute_layout.addWidget(self.minus_button)

        layout.addLayout(minute_layout)

        #displayed reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.resetTimer)
        layout.addWidget(self.reset_button)

        #displayed start/stop button
        self.timer_button = QPushButton("Start")
        self.timer_button.clicked.connect(self.toggleTimer)
        layout.addWidget(self.timer_button)


        self.setLayout(layout)

        self.sessionDisplay()

        #styling
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #EAEAEA;
                font-family: Arial;
            }

            QLabel {
                color: #EAEAEA;
            }

            QPushButton {
                background-color: #1F1F1F;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #2A2A2A;
            }

            QPushButton:pressed {
                background-color: #333;
            }
            """)

    #switches label to according session
    def sessionChange(self):
        return "Break session" if self.is_break else "Work session"

    #updates the label
    def sessionDisplay(self):
        self.session_label.setText(self.sessionChange())
        self.updateColors()

    #seperates minutes & seconds
    def timeFormat(self, time:int):
        m, s = divmod(time, 60)
        return f"{m:02}:{s:02}"

    #update displayed time & label & notficiation
    def updateTime(self):
        if not self.is_break:
            if self.count > 0:
                self.count -= 1
                self.timer_label.setText(self.timeFormat(self.count))

            else:
                self.timer.stop()
                self.count = 5 * 60
                self.timer_label.setText(self.timeFormat(self.count))
                self.timer_button.setText("Start")
                self.sound.play()
                self.is_break = True
                self.sessionDisplay()
                self.sendNotficiation()

        else:
            if self.count > 0:
                self.count -= 1
                self.timer_label.setText(self.timeFormat(self.count))

            else:
                self.timer.stop()
                self.count = 25 * 60
                self.timer_label.setText(self.timeFormat(self.count))
                self.timer_button.setText("Start")
                self.sound.play()
                self.is_break = False
                self.sessionDisplay()
                self.sendNotficiation()

    #start & stop timer
    def toggleTimer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.timer_button.setText("Start")
        else:
            self.timer.start(1000)
            self.timer_button.setText("Stop")

    #updates to the next timer & label
    def resetTimer(self):
        if not self.is_break:
            self.count = 25 * 60
            self.timer_label.setText(self.timeFormat(self.count))
        else:
            self.count = 5 * 60
            self.timer_label.setText(self.timeFormat(self.count))

    #updates color according session
    def updateColors(self):
        if self.is_break:
            self.timer_label.setStyleSheet("color: #4CAF50;")
            self.session_label.setStyleSheet("color: #81C784;")
        else:
            self.timer_label.setStyleSheet("color: #FF5252;")
            self.session_label.setStyleSheet("color: #FF8A80;")

    #windows notfication
    def sendNotficiation(self):
        if self.is_break:
            notify.show_toast("Work is over!",duration=3,threaded=True)
        else:
            notify.show_toast("Break is over!",duration=3,threaded=True)

    #add min
    def addMinute(self):
        self.count += 60
        self.timer_label.setText(self.timeFormat(self.count))

    #remove min
    def removeMinute(self):
        if not self.count <= 60:
            self.count -= 60
            self.timer_label.setText(self.timeFormat(self.count))
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Pomodoro()
    widget.show()

    sys.exit(app.exec())