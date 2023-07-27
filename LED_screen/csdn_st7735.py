# -*- coding: UTF-8 -*-

import time
from luma.core.interface.serial import spi
from luma.core.render import canvas
from PIL import Image, ImageDraw, ImageFont

serial = spi(port=0, device=0, bus_speed_hz=16000000)

def delay_ms(ms):
  time.sleep(ms * 0.001)

def lcd_writeCmd(cmd):
  serial.command(cmd)

def lcd_writeData(data):
  serial.data([data])

def lcd_reset():
  serial._gpio.output(serial._RST, serial._gpio.LOW)
  delay_ms(100)
  serial._gpio.output(serial._RST, serial._gpio.HIGH)

def lcd_init():
  lcd_reset()
  lcd_writeCmd(0x11)
  delay_ms(120)
  lcd_writeCmd(0x21)
  lcd_writeCmd(0xB1)
  lcd_writeData(0x05)
  lcd_writeData(0x3A)
  lcd_writeData(0x3A)
  lcd_writeCmd(0xB2)
  lcd_writeData(0x05)
  lcd_writeData(0x3A)
  lcd_writeData(0x3A)
  lcd_writeCmd(0xB3)
  lcd_writeData(0x05)
  lcd_writeData(0x3A)
  lcd_writeData(0x3A)
  lcd_writeData(0x05)
  lcd_writeData(0x3A)
  lcd_writeData(0x3A)
  lcd_writeCmd(0xB4)
  lcd_writeData(0x03)
  lcd_writeCmd(0xC0)
  lcd_writeData(0x62)
  lcd_writeData(0x02)
  lcd_writeData(0x04)
  lcd_writeCmd(0xC1)
  lcd_writeData(0xC0)
  lcd_writeCmd(0xC2)
  lcd_writeData(0x0D)
  lcd_writeData(0x00)
  lcd_writeCmd(0xC3)
  lcd_writeData(0x8D)
  lcd_writeData(0x6A)
  lcd_writeCmd(0xC4)
  lcd_writeData(0x8D)
  lcd_writeData(0xEE)
  lcd_writeCmd(0xC5)
  lcd_writeData(0x0E)
  lcd_writeCmd(0xE0)
  lcd_writeData(0x10)
  lcd_writeData(0x0E)
  lcd_writeData(0x02)
  lcd_writeData(0x03)
  lcd_writeData(0x0E)
  lcd_writeData(0x07)
  lcd_writeData(0x02)
  lcd_writeData(0x07)
  lcd_writeData(0x0A)
  lcd_writeData(0x12)
  lcd_writeData(0x27)
  lcd_writeData(0x37)
  lcd_writeData(0x00)
  lcd_writeData(0x0D)
  lcd_writeData(0x0E)
  lcd_writeData(0x10)
  lcd_writeCmd(0xE1)
  lcd_writeData(0x10)
  lcd_writeData(0x0E)
  lcd_writeData(0x03)
  lcd_writeData(0x03)
  lcd_writeData(0x0F)
  lcd_writeData(0x06)
  lcd_writeData(0x02)
  lcd_writeData(0x08)
  lcd_writeData(0x0A)
  lcd_writeData(0x13)
  lcd_writeData(0x26)
  lcd_writeData(0x36)
  lcd_writeData(0x00)
  lcd_writeData(0x0D)
  lcd_writeData(0x0E)
  lcd_writeData(0x10)
  lcd_writeCmd(0x3A)
  lcd_writeData(0x05)
  lcd_writeCmd(0x36)
  lcd_writeData(0xC8)
  lcd_writeCmd(0x29)

def lcd_setRegion(x1, y1, x2, y2):
  lcd_writeCmd(0x2a)
  lcd_writeData(0x00)
  lcd_writeData(x1 + 0x1A)
  lcd_writeData(0x00)
  lcd_writeData(x2 + 0x1A)
  lcd_writeCmd(0x2b)
  lcd_writeData(0x00)
  lcd_writeData(y1 + 1)
  lcd_writeData(0x00)
  lcd_writeData(y2 + 1)
  lcd_writeCmd(0x2c)

def lcd_fill(color1, color2):
  lcd_setRegion(0, 0, 79, 159)
  for i in range(1,161):
    for j in range(1,81):
      lcd_writeData(color1)
      lcd_writeData(color2)


lcd_init()
lcd_fill(0xf8, 0x00)
lcd_fill(0xff, 0xe0)
serial.cleanup()
