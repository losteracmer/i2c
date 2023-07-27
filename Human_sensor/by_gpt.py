import RPi.GPIO as GPIO
import time
import datetime

# 定义 GPIO 引脚
SENSOR_PIN = 26

# 初始化 GPIO 引脚
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# 传感器检测函数
def sensor_callback(channel):
    if GPIO.input(SENSOR_PIN):
        print("Motion detected at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        print("Motion stopped at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

# 监听传感器状态变化
GPIO.add_event_detect(SENSOR_PIN, GPIO.BOTH, callback=sensor_callback)

# 主循环
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

# 清理 GPIO 引脚
GPIO.cleanup()
