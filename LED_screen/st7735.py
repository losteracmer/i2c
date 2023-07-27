# -*- coding: UTF-8 -*-

from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from PIL import Image, ImageDraw, ImageFont
from luma.core.render import canvas
import RPi.GPIO as GPIO
import time

BL = 21

class Screen:
    def __init__(self):
        self.height = 128
        self.width = 128
        self.serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
        self.device = st7735(self.serial, width=self.width, height=self.height, rotate=1, h_offset=0, v_offset=0, bgr=False)
        self.buffer = Image.new(self.device.mode, self.device.size)
        self.fontType = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
        self.fontTypeEN = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
        self.fontSize = 24
        self.font = ImageFont.truetype(self.fontType, self.fontSize)
        self.draw = ImageDraw.Draw(self.buffer)

    def initGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BL,GPIO.OUT)

    def closeGPIO(self):
        GPIO.cleanup()

    def openScreen(self):
        GPIO.output(BL, GPIO.HIGH)

    def closeScreen(self):
        GPIO.output(BL, GPIO.LOW)

    def drawRect(self, x, y, w, h, color='black', outline=None):
        self.draw.rectangle((x, y, x+w, y+h), outline=outline, fill=color)
        self.device.display(self.buffer)

    def drawDemo(self):
        self.draw.rectangle((10,10,10+20,10+20), outline="white", fill="green")
        self.draw.text((30, 40), "Hello World", fill="red")
        self.draw.text((10, 70), "http://xfxuezhang.cn", "white")
        self.device.display(self.buffer)

    #with canvas(self.device) as draw:
    # draw.rectangle((10,10,10+20,10+20), outline="white", fill="green")
    # draw.text((30, 40), "Hello World", fill="red")
    # draw.text((10, 70), "http://xfxuezhang.cn", "white")

    def drawTextEN(self, x, y, msg, color='white', fontSize=None, fontType=None):
        newType = fontType if fontType else self.fontTypeEN
        newSize = fontSize if fontSize else self.fontSize
        font = ImageFont.truetype(newType, newSize)
        self.drawRect(x, y, len(msg)*newSize/2, newSize, 'black')
        self.draw.text((x, y), msg, font=font, fill=color)
        self.device.display(self.buffer)

    def drawTextCN(self, x, y, msg, color='white', fontSize=None, fontType=None):
        newType = fontType if fontType else self.fontType
        newSize = fontSize if fontSize else self.fontSize
        font = ImageFont.truetype(newType, newSize)
        self.drawRect(x, y, len(msg)*newSize, newSize, 'black')
        self.draw.text((x, y), msg, font=font, fill=color)
        self.device.display(self.buffer)

    def clearScreen(self, color='black'):
        self.draw.rectangle(self.device.bounding_box, outline=None, fill=color)
        self.device.display(self.buffer)

    def showInfo(self):
        self.clearScreen()
        self.drawTextCN(18, 20, '士涛学长')
        self.drawTextCN(5, 45, '无与伦比')
        self.drawTextEN(20, 80, "supersst.com", "red", fontSize=12)


if __name__ == '__main__':
    try:
        screen = Screen()
        screen.initGPIO()
        screen.openScreen()
        screen.drawDemo()
        time.sleep(2)
        screen.clearScreen()
        print(screen.width)
        print(screen.height)
        # screen.showInfo()
        screen.drawTextCN(5, 110, '捕获总数=', color='green', fontSize=18)
        screen.drawTextEN(85, 115, str(1), color='red', fontSize=18)
        time.sleep(2)
        screen.drawTextEN(85, 120, str(2), color='red', fontSize=18)
    except:
        pass
    finally:
        screen.closeGPIO()
