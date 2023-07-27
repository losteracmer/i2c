"""
SCREEN PIN	RASPBERRY PI PIN
GND	Ground (pins 6, 9, 14, 20, 25, 30, 34 or 39)
VCC	5v Power (pins 2 or 4)
SCL	GPIO 11 (pin 23)
SDA	GPIO 10 (pin 19)
RES	GPIO 25 (pin 22)
DC	GPIO 24 (pin 18)
CS	GPIO 8 (pin 24)
BL	Not connected

link: https://jakew.me/st7735-pi/
"""
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735

disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=128, height=128, rotation=0, invert=False)

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Load default font.
font = ImageFont.load_default()

# Write some text
draw.text((5, 5), "123", font=font, fill=(255, 255, 255))

# Write buffer to display hardware, must be called to make things visible on the
# display!
disp.display(img)
