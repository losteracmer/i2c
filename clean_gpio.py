import RPi.GPIO as GPIO

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 获取所有GPIO引脚编号
pins = [pin for pin in range(2, 28)]

#初始化GPIO引脚
GPIO.setup(pins, GPIO.OUT)
# 清理GPIO资源
GPIO.cleanup(pins)


