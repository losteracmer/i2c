# 展示红外脉冲间隔时间
import RPi.GPIO as GPIO
import time
from queue import Queue


# 红外传感器的引脚
IR_PIN = 26

# 初始化GPIO口
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)

show_pulse = True
# global last_sign
last_sign = None
last_time = None
cnt = 0

def record_time(channel):
    global last_sign, last_time, cnt
    cnt +=1
    loh = GPIO.input(channel)
    if last_sign == None:
        print("first sign", "HIGH" if loh == GPIO.HIGH else "LOW")
        last_time = time.time()
        last_sign = loh
        return
    now = time.time()
    if last_sign == GPIO.HIGH and loh == GPIO.LOW and show_pulse:
        duration = now - last_time
        print("%d\t" % cnt,"HIGH:\t %.4f" % (duration * 1000))
    
    if last_sign == GPIO.LOW and loh == GPIO.HIGH:
        duration = now - last_time
        print("%d\t" % cnt,"LOW:\t %.4f" % (duration * 1000))
    
    last_sign = loh
    last_time = now
    

GPIO.add_event_detect(IR_PIN, GPIO.BOTH, callback=record_time)

# 循环等待中断处理程序执行
try:
    while True:
        time.sleep(1)
        # print("size", q.qsize())
        # print(q.queue)
except KeyboardInterrupt:
    GPIO.cleanup()
