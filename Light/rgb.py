import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 设置RGB灯引脚
red_pin = 18
green_pin = 23
blue_pin = 24

# 初始化RGB灯引脚
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

# 定义RGB灯控制函数
def set_color(r, g, b):
    GPIO.output(red_pin, r)
    GPIO.output(green_pin, g)
    GPIO.output(blue_pin, b)

# 测试代码
while True:
    set_color(1, 0, 0)  # 红色
    time.sleep(1)
    set_color(0, 1, 0)  # 绿色
    time.sleep(1)
    set_color(0, 0, 1)  # 蓝色
    time.sleep(1)
    set_color(1, 1, 0)  # 黄色
    time.sleep(1)
    set_color(1, 0, 1)  # 紫色
    time.sleep(1)
    set_color(0, 1, 1)  # 青色
    time.sleep(1)

# 清理GPIO资源
GPIO.cleanup()


