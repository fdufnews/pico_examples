# test program for the led_timer module
# 3 LEDs on GPIO 16, 17 and 18

from led_timer import led_timer as lt
import time

red = lt(16)
green = lt(17)
blue = lt(18)

red.setPeriodHL(200,800)
green.setPeriodHL(500,500)
blue.setPeriodHL(800,200)

while True:
    time.sleep(10)

    red.stop()
    green.stop()
    blue.stop()

    red.setPeriodHL(800,200)
    green.setPeriodHL(500,500)
    blue.setPeriodHL(200,800)

    red.restart()
    green.restart()
    blue.restart()

    time.sleep(10)

    red.stop()
    green.stop()
    blue.stop()

    red.setPeriodHL(200,800)
    green.setPeriodHL(500,500)
    blue.setPeriodHL(800,200)

    red.restart()
    green.restart()
    blue.restart()

