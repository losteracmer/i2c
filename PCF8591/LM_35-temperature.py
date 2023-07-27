import time
import smbus

# 初始化I2C总线
bus = smbus.SMBus(1)

# 设置PCF8591模块地址
address = 0x48

# 设置PCF8591模块通道
channel = 0x44
# channel = 0

# 读取温度数据
def read_temp():
    # 设置PCF8591模块通道
    bus.write_byte(address, channel)

    # 读取LM35模块输出电压
    raw_value = bus.read_byte(address)
    voltage = raw_value / 255 * 3.3

    # 将电压转换为温度，精确到小数点后两位
    temp_c = round(voltage * 100, 2)

    return temp_c

# 测试代码
while True:
    print(read_temp())
    time.sleep(1)

# 关闭I2C总线
bus.close()

