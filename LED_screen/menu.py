from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

# 设置OLED屏幕的大小和引脚
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# 定义菜单选项
menu_items = ["Add item 1", "Add item 2", "Add item 3", "Add item 4"]
selected_item = 0

# 显示菜单
def show_menu():
    fontsize = 12
    font = ImageFont.truetype("arial.ttf", fontsize)
    with canvas(device) as draw:
        for i, item in enumerate(menu_items):
            if i == selected_item:
                draw.text((0, i * 30), "> " + item, font=font, fill="white")
            else:
                draw.text((0, i * 30), "  " + item, font=font, fill="white")

# 处理按键事件
def handle_key(key):
    global selected_item
    if key == "up":
        selected_item = (selected_item - 1) % len(menu_items)
    elif key == "down":
        selected_item = (selected_item + 1) % len(menu_items)
    elif key == "enter":
        # 执行所选菜单项的操作
        print("Selected item:", menu_items[selected_item])

# 运行程序
if __name__ == "__main__":
    show_menu()

    while True:
        key = input("Enter key (up/down/enter): ")
        handle_key(key)
        show_menu()

