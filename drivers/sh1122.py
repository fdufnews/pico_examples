# MicroPython SH1122 OLED driver, SPI interface
# fdufnews 2021/02/09
# based on Peter Hinch SSD1306 driver

from micropython import const
import framebuf


# register definitions

SET_COL_ADR_LSB = const(0X0)
SET_COL_ADR_MSB = const(0X10)
SET_DISP_START_LINE = const(0X40)
SET_CONTRAST = const(0X81)
SET_SEG_REMAP = const(0XA0)
SET_ENTIRE_ON = const(0XA4)
SET_NORM_INV = const(0XA6)
SET_MUX_RATIO = const(0XA8)
SET_CTRL_DCDC = const(0XAD)
SET_DISP = const(0XAE)
SET_ROW_ADR = const(0XB0)
SET_COM_OUT_DIR = const(0XC0)
SET_DISP_OFFSET = const(0XD3)
SET_DISP_CLK_DIV = const(0XD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_VSEG_LEVEL = const(0XDC)
SET_DISCHARGE_LEVEL = const(0X30)
           


# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SH1122(framebuf.FrameBuffer):
    @staticmethod
    def rgb(r, g, b):
        return int(max(r,g,b))  # perhaps not the better but .....

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pages = self.height // 2
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.GS4_HMSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            SET_COL_ADR_LSB,
            SET_COL_ADR_MSB,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP,
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR,  # scan from COM0 to COM[N]
            SET_DISP_OFFSET,
            0x00,
            # display
            SET_CONTRAST,
            0x80,  # median
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        self.write_cmd(SET_COL_ADR_LSB)
        self.write_cmd(SET_COL_ADR_MSB)
        self.write_cmd(SET_ROW_ADR)
        self.write_data(self.buffer)


class SH1122_SPI(SH1122):
    def __init__(self, width, height, spi, dc, res, cs):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time

        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)
