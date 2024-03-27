import time, math, framebuf, utime, gc

class ST7302(framebuf.FrameBuffer):

    @staticmethod
    def rgb(r, g, b):
        return int((r > 127) or (g > 127) or (b > 127))
        
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = bytearray(math.ceil(height/8)*(width if width%2==0 else width+1))
        self.old_buffer = bytearray(math.ceil(height/8)*(width if width%2==0 else width+1))
        self.bit_column_fill = [ 0x00 for _ in range(3-math.ceil(height%12/4))] # once param must 3 bit
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def clear(self):
        self.fill(0)
        self.old_buffer[:] = self.buffer
        self.write_cmd(0xb9)  #enable CLR RAM
        self.write_data(0xe3)
#        self.__sleep_wait_command(1000)
        self.__sleep_wait_command(200)
        self.write_cmd(0xb9)  #disable CLR RAM
        self.write_data(0x23)

    def init_display(self):
        self.hard_reset()
        self.write_cmd(0xeb) # Enable OTP
        self.write_data(0x02)
        self.write_cmd(0xd7) # OTP Load Control
        self.write_data(0x68)
        self.write_cmd(0xb4)  #GateEQSettingHPMEQLPMEQ
        self.write_data(0xa5)
        self.write_data(0x66)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x40)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x40)
        self.write_cmd(0x11) # sleep out
        self.__sleep_wait_command()
        self.write_cmd(0x36) # Memory Data Access Control
        self.write_data(0x00)
        self.write_cmd(0x39) # Low power
        self.write_cmd(0x3a) # DataFormatSelect4writefor24bit
        self.write_data(0x11)
        self.write_cmd(0xb0)  # Duty setting
        self.write_data(0x64)  # 250duty/4=63
        self.write_cmd(0xb8)  # Panel Setting Frame inversion
        self.write_data(0x09)  # 250duty/4=63
        self.write_cmd(0x29) # Display on

        self.clear()
        self.show()

    def __sleep_wait_command(self, sleep_time=100):
        time.sleep_ms(sleep_time)
    

    def inv_off(self):
        self.write_cmd(0x20)
        self.__sleep_wait_command()
    
    def inv_on(self):
        self.write_cmd(0x21)
        self.__sleep_wait_command()
    
    def hard_reset(self):
        self.res.value(0)
        self.__sleep_wait_command(5)
        self.res.value(1)
        self.__sleep_wait_command(10)
    
    def clear(self):
        self.fill(0)
        self.old_buffer[:] = self.buffer
        self.write_cmd(0xb9)  #enable CLR RAM
        self.write_data(0xe3)
        self.__sleep_wait_command(200)
        self.write_cmd(0xb9)  #disable CLR RAM
        self.write_data(0x23)

    def __judgment_change_column(self, buffer, old_buffer):
        change_list=set()
        for i, bits in enumerate(buffer):
            if not old_buffer[i] == bits:
                # update two line together
                change_list.add(i%self.width if i%self.width%2 == 0 else i%self.width - 1)
        return change_list


    def __shift_buffer(self, new_pos, cache):
        self.write_cmd(0x2a) # Row set
        self.write_data(0x19) # 0x19 is access memory start
        self.write_data(0x19+self.width)
        self.write_cmd(0x2b) # column set
        self.write_data(new_pos)
        self.write_data(self.height)
        self.write_cmd(0x2c) # write memory
        for item in cache:
            self.write_data(item)

    def show(self):
        column_list = [[] for _ in range(self.width)]
        change_column_index_list = self.__judgment_change_column(self.buffer, self.old_buffer)

        for i,bit in enumerate(self.buffer):
            column_list[i%self.width].append(bit)

        for column_i in change_column_index_list:
            two_column_param=[]
            for bit_i, bit in enumerate(column_list[column_i]):
                bit1 = self.__mix_bit(bit, column_list[column_i+1][bit_i])
                two_column_param.append(bit1)
                bit2 = self.__mix_bit(bit>>4, column_list[column_i+1][bit_i]>>4)
                two_column_param.append(bit2)
            self.__shift_buffer(column_i//2, two_column_param + self.bit_column_fill)
        if not len(change_column_index_list) == 0:
            self.old_buffer[:] = self.buffer
        gc.collect()

    def __mix_bit(self, bit1:int, bit2:int):
        mix_bit=0x00
        mix_bit=mix_bit|((bit1&0x01)<<7)
        mix_bit=mix_bit|((bit2&0x01)<<6)
        mix_bit=mix_bit|((bit1&0x02)<<4)
        mix_bit=mix_bit|((bit2&0x02)<<3)
        mix_bit=mix_bit|((bit1&0x04)<<1)
        mix_bit=mix_bit|((bit2&0x04)<<0)
        mix_bit=mix_bit|((bit1&0x08)>>2)
        mix_bit=mix_bit|((bit2&0x08)>>3)
        return mix_bit
        

class ST7302_SPI(ST7302):        
    def __init__(self, width, height, spi, dc, res, cs):
        self.rate = 33 * 1024 * 1024
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
        self.spi.write(bytearray([buf]))
        self.cs(1)





# ****************************************************************************







        
