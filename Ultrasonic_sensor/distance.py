#导入 GPIO库
import RPi.GPIO as GPIO
import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 设置OLED屏幕的大小和引脚
RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()

# 清空屏幕并创建一个新的图像
disp.clear()
disp.display()
width = disp.width
height = disp.height

# 获取图像的绘图对象并设置字体
#font = ImageFont.load_default()
font = ImageFont.truetype('arial.ttf', 14)

def clear():
    disp.clear()
    disp.display()

def showdistance(dis):
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), dis, font=font, fill=255)
    disp.image(image)
    disp.display()
  
#设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)
  
#定义 GPIO 引脚
GPIO_TRIGGER = 15
GPIO_ECHO = 14
  
#设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
  
def distance():
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)
  
    # 持续 10 us 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
  
    start_time = time.time()
    stop_time = time.time()
  
    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
  
    # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
  
    # 计算超声波的往返时间 = 时刻2 - 时刻1
    time_elapsed = stop_time - start_time
    # 声波的速度为 343m/s， 转化为 34300cm/s。
    distance = (time_elapsed * 34300) / 2
  
    return distance
  
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            distance_str = "{:.2f}".format(dist)
            print("Measured Distance = {:.2f} cm".format(dist))
            # clear()
            showdistance(distance_str)
            # time.sleep(0.05)
            #break
  
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
