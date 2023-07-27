import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 设置OLED屏幕的大小和引脚
RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

# 清空屏幕并创建一个新的图像
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# 获取图像的绘图对象并设置字体
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
fontsize = 26
font = ImageFont.truetype("wqy-zenhei.ttc", fontsize)

# 在屏幕上显示“Hello, world!”
#draw.text((0, 0), "shao shi tao\n and \n very coll\n ------ end", font=font, fill=255)
draw.text((0, 0), "丁佳梦就会\n浪费钱qaq*", font=font, fill=255)
disp.image(image)
disp.display()

