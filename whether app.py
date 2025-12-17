import sys, requests, os
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMainWindow)
from PyQt5.QtCore import Qt
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.response = None
        self.enterBox = QLabel("ENTER THE CITY OF YOUR CHOICE:", self)
        self.cityinput = QLineEdit(self)
        self.temperature = QLabel(self)
        self.emoji_label = QLabel(self)
        self.get_whether_button = QPushButton("Get Whether", self)
        self.description = QLabel(self)
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.UI()
    def UI(self):
        #MAIN WINDOW SETTINGS
        self.setWindowTitle('Whether App')
        self.setGeometry(650, 200, 700, 400)
        #ADDING SHIT TO LAYOUT
        self.layout.addWidget(self.enterBox)
        self.layout.addWidget(self.cityinput)
        self.layout.addWidget(self.get_whether_button)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.temperature)
        self.layout.addWidget(self.emoji_label)
        self.enterBox.setStyleSheet("font-size: 30px;"
                                 "color: green;"
                                 "background-color: black"
                                 )
        self.emoji_label.setStyleSheet("font-size: 30px;"
                                    )
        #SETTING SHIT UP IN LAYOUT
        self.enterBox.setAlignment(Qt.AlignCenter)
        self.cityinput.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        #ADDING LAYOUT TO THE CENTRAL WIDGET AND MAKE CENTRAL WIDGET THE CENTRAL WIDGET(I KNOW I KNOW NOTHINGS MAKES SENSE HERE BUT THAT'S THAT)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)
        #BUTTON SHIT
        self.get_whether_button.clicked.connect(self.getinfo)
    def getinfo(self):
        params = {
            "q": self.cityinput.text(),
            "appid": API_KEY,
            "units": "metric"
        }
        #ASKING THE SERVER FOR INFO
        self.response = requests.get(BASE_URL, params=params)
        if self.response.status_code != 200:
            print("Error:", self.response.text)
            return None
        #ADDING DATA TO LABELS
        self.data = self.response.json()
        temp = self.data["main"]["temp"]
        descriptionn = self.data["weather"][0]["description"]
        self.temperature.setText(f"{temp} °C")
        self.description.setText(descriptionn)
        if descriptionn == 'clear sky':
            self.emoji_label.setText("🌞")
            self.temperature_font_setter()
            self.description.setStyleSheet("font-size: 30px;"
                                           "color: red;"
                                           "background-color: black"
                                           )
            return None
        elif descriptionn == 'light rain':
            self.emoji_label.setText("☔")
            self.temperature_font_setter()
            self.description.setStyleSheet("font-size: 30px;"
                                           "color: blue;"
                                           "background-color: black"
                                           )

            return None
        elif descriptionn == 'haze':
            self.emoji_label.setText("🌥️")
            self.temperature_font_setter()
            self.description.setStyleSheet("font-size: 30px;"
                                           "color: brown;"
                                           "background-color: yellow"
                                           )
            return None
        else:
            self.emoji_label.setText("I dont know what to display")
            return None

    def temperature_font_setter(self):
        self.temperature.setStyleSheet("font-size: 30px;"
                                       "color: red;"
                                       "background-color: black"
                                       )





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())