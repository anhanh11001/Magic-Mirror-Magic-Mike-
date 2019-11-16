from gui.gui import MagicApp
from weather.weather import Weather
import sys
import News_API
import Calendar_API
from camera.gesture_detector import GestureDetector
import rpi_neopixel_simpletest

if __name__ == '__main__':
    app = MagicApp(Weather(),
            Calendar_API.Calendar(),
            News_API.News(),
            GestureDetector(),
            rpi_neopixel_simpletest.LedSTRIP())
    app.run(sys.argv)

