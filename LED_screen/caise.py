import time
import spidev
import RPi.GPIO as GPIO

# 定义ST7735显示器的引脚
DC = 24
RST = 25
CS = 8

# 定义ST7735显示器的命令
SWRESET = 0x01
SLPOUT = 0x11
COLMOD = 0x3A
MADCTL = 0x36
SET_PIXEL_FORMAT = 0x3A
SET_DISPLAY_ON = 0x29

# 定义SPI总线的参数
SPI_SPEED_HZ = 4000000

# 初始化SPI总线和GPIO口
spi = spidev.SpiDev()
GPIO.setmode(GPIO.BCM)
GPIO.setup(DC, GPIO.OUT)
GPIO.setup(RST, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

# ST7735显示器初始化函数
def st7735_init():
    # 初始化SPI总线和GPIO口
    spi.open(0, 0)
    spi.max_speed_hz = SPI_SPEED_HZ
    GPIO.output(CS, GPIO.LOW)

    # 复位ST7735显示器
    GPIO.output(RST, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RST, GPIO.HIGH)
    time.sleep(0.1)

    # 初始化ST7735显示器
    spi.writebytes([SWRESET])
    time.sleep(0.1)
    spi.writebytes([SLPOUT])
    time.sleep(0.1)
    spi.writebytes([COLMOD, 0x05])
    spi.writebytes([MADCTL, 0x08])
    spi.writebytes([SET_PIXEL_FORMAT, 0x05])
    spi.writebytes([SET_DISPLAY_ON])

    # 关闭SPI总线和GPIO口
    GPIO.output(CS, GPIO.HIGH)
    spi.close()

# 显示图像函数
def st7735_display_image(image):
    # 初始化SPI总线和GPIO口
    spi.open(0, 0)
    spi.max_speed_hz = SPI_SPEED_HZ
    GPIO.output(CS, GPIO.LOW)

    # 发送显示图像的命令和数据
    GPIO.output(DC, GPIO.LOW)
    spi.writebytes([0x2A])
    GPIO.output(DC, GPIO.HIGH)
    spi.writebytes([0x00, 0x00, 0x00, 127])
    GPIO.output(DC, GPIO.LOW)
    spi.writebytes([0x2B])
    GPIO.output(DC, GPIO.HIGH)
    spi.writebytes([0x00, 0x00, 0x00, 127])
    GPIO.output(DC, GPIO.LOW)
    spi.writebytes([0x2C])
    GPIO.output(DC, GPIO.HIGH)
    spi.writebytes(image)

    # 关闭SPI总线和GPIO口
    GPIO.output(CS, GPIO.HIGH)
    spi.close()

# 初始化ST7735显示器
st7735_init()

# 显示图像测试代码
image = [0xFF] * (128 * 128 * 2)
st7735_display_image(image)

