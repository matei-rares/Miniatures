import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

path="sprites"
sprites=["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png"]
for i in range(len(sprites)):
    sprites[i]=path+"/"+sprites[i]

class RunningTeddy(QWidget):
    def __init__(self):
        super().__init__()

        # Load Teddy Bear Animation Frames
        self.frames = [
            QPixmap(sprites[0]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),  # Replace with actual frame images
            QPixmap(sprites[1]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(sprites[2]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(sprites[3]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(sprites[4]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            QPixmap(sprites[5]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        ]
        self.current_frame = 0

        # Teddy Label
        self.label = QLabel(self)
        self.label.setPixmap(self.frames[self.current_frame])

        # Window settings
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 1000, 200, 200)  # Adjust Y-position to match the taskbar height

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(100)  # Adjust speed as needed

        # Timer for movement
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_teddy)
        self.move_timer.start(20)  # Adjust movement speed

        self.x_pos = 0

    """Switch Teddy Bear Frames"""
    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.setPixmap(self.frames[self.current_frame])

    """Move Teddy Bear from Left to Right"""
    def move_teddy(self):
        screen_width = QApplication.primaryScreen().geometry().width()
        self.x_pos += 5  # Adjust speed
        if self.x_pos > screen_width:
            self.x_pos = -100  # Reset position when out of screen
        self.move(self.x_pos, 990)  # Adjust height to be near the taskbar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    teddy = RunningTeddy()
    teddy.show()
    sys.exit(app.exec_())
