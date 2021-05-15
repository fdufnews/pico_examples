from machine import Timer, Pin

class led_timer:

    def __init__(self, PinNum = 25, periodH = 500, periodL = 500):
        self.pin = PinNum
        self.periodH = periodH
        self.periodL = periodL
        self.led=Pin(self.pin,Pin.OUT)
        self.led.value(0)
        self.timer = Timer()
        self.timer.init(period=self.periodL, mode=Timer.ONE_SHOT, callback=self.toggle)


    def toggle(self, timer):
        self.led.value(not self.led.value())
        if (self.led.value()):
            self.timer.init(period=self.periodH, mode=Timer.ONE_SHOT, callback=self.toggle)
        else:
            self.timer.init(period=self.periodL, mode=Timer.ONE_SHOT, callback=self.toggle)

    def setPeriodH(self, period):
        self.periodH = period

    def setPeriodL(self, period):
        self.periodL = period

    def setPeriod(self, period):
        self.periodL = self.periodH = period

    def setPeriodHL(self, periodH, periodL):
        self.periodL = periodL
        self.periodH = periodH

    def stop(self):
        self.timer.deinit()
        self.led.value(0)

    def restart(self):
        self.toggle(self.timer)


