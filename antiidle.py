import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont

import keyboard

class AntiIdleThread(QThread):
    status_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._interval = 300
        self._press_duration_space = 0.5
        self._press_duration_w = 0.3
        self._key_space = 'space'
        self._key_w = 'w'

    def run(self):
        while True:
            if self._running:
                keyboard.press(self._key_space)
                time.sleep(self._press_duration_space)
                keyboard.release(self._key_space)

                keyboard.press(self._key_w)
                time.sleep(self._press_duration_w)
                keyboard.release(self._key_w)

                remaining_sleep = self._interval - self._press_duration_space - self._press_duration_w
                if remaining_sleep > 0:
                    time.sleep(remaining_sleep)
            else:
                time.sleep(0.1)

    def toggle_run(self):
        self._running = not self._running
        self.status_signal.emit(self._running)

    @property
    def is_running(self):
        return self._running

class AntiIdleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_anti_idle_thread()
        self.apply_cheat_aesthetic()
        self.setup_hotkey()

    def init_ui(self):
        self.setWindowTitle("Anti Idle")
        self.setGeometry(100, 100, 350, 180)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        self.toggle_btn = QPushButton("ACTIVATE ANTI-IDLE")
        self.toggle_btn.setFixedSize(250, 60)
        self.toggle_btn.clicked.connect(self.toggle_anti_idle)
        layout.addWidget(self.toggle_btn, alignment=Qt.AlignCenter)

        self.info_label = QLabel("PRESS F7 TO TOGGLE (GLOBAL HOTKEY)")
        layout.addWidget(self.info_label, alignment=Qt.AlignCenter)

        self.message_box = QLabel(self)
        self.message_box.setAlignment(Qt.AlignCenter)
        self.message_box.setWordWrap(True)
        self.message_box.setStyleSheet("""
            color: #FFFF00;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 8px;
            border-radius: 5px;
            font-family: 'Consolas', 'Monospace', monospace;
            font-size: 13px;
            border: 1px solid #FFFF00;
        """)
        self.message_box.hide()
        layout.addWidget(self.message_box, alignment=Qt.AlignCenter)

    def init_anti_idle_thread(self):
        self.anti_idle_thread = AntiIdleThread()
        self.anti_idle_thread.status_signal.connect(self.update_ui_state)
        self.anti_idle_thread.start()

    def toggle_anti_idle(self):
        self.anti_idle_thread.toggle_run()

    def update_ui_state(self, is_running):
        if is_running:
            self.toggle_btn.setText("DEACTIVATE ANTI-IDLE")
            self.toggle_btn.setStyleSheet(self.get_button_style(True))
            self.show_message("ANTI-IDLE ACTIVE!", 2000)
        else:
            self.toggle_btn.setText("ACTIVATE ANTI-IDLE")
            self.toggle_btn.setStyleSheet(self.get_button_style(False))
            self.show_message("ANTI-IDLE INACTIVE.", 2000)

    def apply_cheat_aesthetic(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                border: 2px solid #00ff00;
                border-radius: 10px;
            }
            QLabel {
                color: #00ff00;
                font-family: 'Consolas', 'Monospace', monospace;
                font-size: 14px;
                padding: 5px;
            }
        """)

        font = QFont('Consolas', 12)
        self.info_label.setFont(font)
        self.info_label.setStyleSheet("color: #aaaaaa;")

        self.toggle_btn.setStyleSheet(self.get_button_style(False))

    def get_button_style(self, active):
        if active:
            return """
                QPushButton {
                    background-color: #006600;
                    color: #ffffff;
                    border: 2px solid #00ff00;
                    border-radius: 10px;
                    font-family: 'Consolas', 'Monospace', monospace;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 12px 25px;
                    box-shadow: 0 0 15px #00ff00;
                }
                QPushButton:hover {
                    background-color: #008800;
                    border: 2px solid #00ffff;
                    color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #003300;
                    border: 2px solid #00cc00;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #333333;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    border-radius: 8px;
                    font-family: 'Consolas', 'Monospace', monospace;
                    font-size: 16px;
                    padding: 10px 20px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #444444;
                    border: 1px solid #00ffff;
                    color: #00ffff;
                }
                QPushButton:pressed {
                    background-color: #004d00;
                    border: 1px solid #00ff00;
                }
            """

    def setup_hotkey(self):
        def hotkey_callback():
            self.toggle_anti_idle()
        keyboard.add_hotkey('f7', hotkey_callback)

    def show_message(self, message, duration_ms=1500):
        self.message_box.setText(message)
        self.message_box.adjustSize()
        self.message_box.move(
            int((self.width() - self.message_box.width()) / 2),
            int(self.height() - self.message_box.height() - 15)
        )
        self.message_box.show()
        QTimer.singleShot(duration_ms, self.message_box.hide)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AntiIdleApp()
    ex.show()
    sys.exit(app.exec_())
