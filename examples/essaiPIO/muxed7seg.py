# A driver using PIO to display a number on a 3 digits multiplexed 7 segments display
# segments are connected this way
# GPIO     2  3  4  5  6  7  8  9
# segments A  B  C  D  E  F  G  DP
# A HIGH switches on a segment of the selected digit
#
# Digits are connected this way
# GPIO     10 11 12
# DIGITS   0  1  2
# Digits are driven by a transistor so a HIGH selects a digit
#
# A digit is lit 30% of the time
#
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep


@asm_pio(out_shiftdir = rp2.PIO.SHIFT_RIGHT, out_init=(PIO.OUT_LOW,) * 8, set_init=(PIO.OUT_LOW,) * 3)
def muxed7seg():
    pull(noblock)
    mov(x, osr)         # Keep most recent pull data saved in X, for recycling by noblock
    set(pins, 0)        # All digits deselected to avoid ghosting
    out(pins, 8)        # Shift 8 segments
    set(pins, 4) [31]   # digit 1 selected
    set(pins, 0)        # All digits deselected to avoid ghosting
    out(pins, 8)        # Shift 8 segments
    set(pins, 2) [31]   # digit 2 selected
    set(pins, 0)        # All digits deselected to avoid ghosting
    out(pins, 8)        # Shift 8 segments
    set(pins, 1) [31]   # digit 3 selected
    wrap

class MUXED_7SEG:
    #            0     1     2     3     4     5     6     7     8     9
    numbers = (0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F) 
    # Despite the digits are deselected when activating the segments there is some ghosting if count-freq is too high (>100_000)
    # There is also a better contrast if count_freq is slower (say 10_000)
    def __init__(self, sm_id, pin_out, pin_set, count_freq, default = 0):
        self._sm = StateMachine(sm_id, muxed7seg, freq=2 * count_freq, out_base=Pin(pin_out), set_base=Pin(pin_set))
        # Use exec() to load default
        self._sm.put(default)
        self._sm.active(1)

    def set(self, value):
        self.segments = self.numbers[value % 10]
        self.segments = self.segments | self.numbers[(value // 10) % 10] << 8
        self.segments = self.segments | self.numbers[(value // 100) % 10] << 16
        self._sm.put(self.segments)


display = MUXED_7SEG(0, 2, 10, count_freq=10_000)


#Count from 0 to 999
while True:
    for i in range(1000):
        display.set(i)
        sleep(0.1)

