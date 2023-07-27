import time
 
# 在/boot/config.txt文件中，添加dtoverlay=w1-gpio,gpiopin=4，重启
# DS18B20温度传感器的文件路径
SENSOR_PATH = '/sys/bus/w1/devices/28-3ce1e38093a6/w1_slave'

# 读取DS18B20温度传感器的温度值
def read_temperature():
    # 打开DS18B20温度传感器文件
    with open(SENSOR_PATH, 'r') as f:
        lines = f.readlines()

    # 解析温度值
    if lines[0].strip()[-3:] == 'YES':
        temperature = int(lines[1].strip()[lines[1].find('t=')+2:]) / 1000.0
        return temperature

    # 如果读取失败，返回None
    return None

# 循环读取并输出温度值
while True:
    temperature = read_temperature()
    if temperature is not None:
        print('Temperature: {} °C'.format(temperature))
    else:
        print('Failed to read temperature')
    time.sleep(1)
