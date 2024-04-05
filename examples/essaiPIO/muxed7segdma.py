# A driver using PIO to display a number on a 3 digits multiplexed 7 segments display
# Variant with DMA
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
from rp2 import PIO, StateMachine, asm_pio, DMA
from time import sleep
from array import array
from uctypes import addressof, bytes_at

# This PIO pulls the 3 digits state to display them
@asm_pio(out_shiftdir = rp2.PIO.SHIFT_RIGHT, out_init=(PIO.OUT_LOW,) * 11)
def muxed7seg():
    pull()
    out(pins, 11) [31]  # Shift 8 segments + 3 digit selector
    wrap

class MUXED_7SEG:
    # this class drives a 3 digits 7 segment display. The dispay is refreshed using 2 DMA channel and a PIO
    # describes which segment is on for each number
    #            0     1     2     3     4     5     6     7     8     9
    numbers = (0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F)
    # buffer used to keep the state of the 3 digits
    seg_buffer = array('I',[0x43F, 0x23F, 0x13F]) 
    
    DMA_BASE = 0x50_000_000
    DMA_READ = 0
    DMA_WRITE = 4
    
    def __init__(self, sm_id, pin_out, pin_set, count_freq):
        self._sm = StateMachine(sm_id, muxed7seg, freq=2 * count_freq, out_base=Pin(pin_out), pull_thresh=11)
        # init DMA channels
        self.dma0 = rp2.DMA()
        self.dma1 = rp2.DMA()
        
        # dma0 copy data from seg_buffer to the PIO TX fifo then arms dma1
        self.ctrl0 = self.dma0.pack_ctrl(inc_read=True, inc_write=False, size=2, chain_to=self.dma1.channel, treq_sel=sm_id)
        self.dma0.config(read=addressof(self.seg_buffer), write=self._sm, count=3, ctrl=self.ctrl0)
        
        # dma1 copies seg_buffer address into dma0.read register and then arms dma0
        self.p = array('I',[0]) #1-element array
        self.p[0] = addressof(self.seg_buffer)
        self.ctrl1 = self.dma1.pack_ctrl(inc_read=False, inc_write=False, size=2, chain_to=self.dma0.channel)
# following line is the expected used one but there is currently a bug in DMA class
#        self.dma1.config(read=self.p, write=self.dma0.read, count=1, ctrl=self.ctrl1)
        write_ad = self.DMA_BASE + (self.dma0.channel << 6) + self.DMA_READ
        self.dma1.config(read=self.p, write=write_ad, count=1, ctrl=self.ctrl1)
        
        # active the dma and the statemachine
        self.dma0.active(True)
        self.dma1.active(True)
        self._sm.active(1)

    def set(self, value):
    # takes 3 least significant digits of value and store de segments state in the buffer in order to display the value
        self.seg_buffer[0] = self.numbers[value % 10] | 0x0400
        self.seg_buffer[1] = self.numbers[(value // 10) % 10] | 0x0200
        self.seg_buffer[2] = self.numbers[(value // 100) % 10] | 0x0100

# 3 functions used during debug to dump DMA registers and part of memory
def buf():
    for i in display.seg_buffer:
        print(hex(i))

def dumpDMAregs(dma):
    for i in dma.registers:
        print(hex(i))

def dumpMem(ad,qty):
    for i in bytes_at(ad,qty):
        print(hex(i))

display = MUXED_7SEG(0, 2, 10, count_freq=10_000)


#Count from 0 to 999
while True:
    for i in range(1000):
        display.set(i)
        sleep(0.1)

