from machine import ADC, mem32

_CS=const(0x4004c000)
_TsEn=const(1<<1)
_GPIO26=const(0x4001c06c)
_GPIO27=const(0x4001c070)
_GPIO28=const(0x4001c074)
_GPIO29=const(0x4001c078)

def volt(adc):
  if isinstance(adc, ADC):
    pass
  else:
    adc=ADC(int(adc))
  # Vref = 3.3v on rpi pico
  # 3.3 / 65535 = 5.035477e-05
  return adc.read_u16() * 5.035477e-05

def raw(adc):
  if isinstance(adc, ADC):
    pass
  else:
    adc=ADC(int(adc))
  return adc.read_u16()

_adcTemp=ADC(ADC.CORE_TEMP)
_adcVSYS=ADC(3)
def coreTemp():
    mem32[_CS]|=_TsEn #enable temperature sensor bias
    vt = volt(_adcTemp)
    mem32[_CS]&=~_TsEn #disable temperature sensor bias to conserve 40 uA
    return 27 - (vt - 0.706)/0.001721

def VSYS():
    return 3 * volt(_adcVSYS)
#workaround for pin setup
# disable output, disable pull up/down
# gpio 29 adc 3 VSYS
mem32[_GPIO29]=0x80
# may comment out unused ADC
# gpio 26 adc 0
mem32[_GPIO26]=0x80
# gpio 27 adc 1
mem32[_GPIO27]=0x80
# gpio 28 adc 2
mem32[_GPIO28]=0x80

