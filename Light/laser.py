import time
import RPi.GPIO as GPIO

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 设置GPIO引脚
pin = 10
GPIO.setup(pin, GPIO.OUT)

# 点亮激光头
def turn_on_laser():
    GPIO.output(pin, GPIO.HIGH)

# 关闭激光头
def turn_off_laser():
    GPIO.output(pin, GPIO.LOW)

# 测试代码
while True:
    turn_on_laser()
    time.sleep(1)
    turn_off_laser()
    time.sleep(1)

# 清理GPIO资源
GPIO.cleanup()


