import Adafruit_ADS1x15
import time

# 初始化 ADS1115 模块
adc = Adafruit_ADS1x15.ADS1115()

# 读取 ADC 值
# value = adc.read_adc(0, gain=1)

"""
当同时读取四个值的时候，这貌似是个bug
0代表的是 A3
1代表的是 A0
2代表的是 A1
3代表的是 A2
"""
values = [0]*5
while True:
    for i in range(4):
        value = adc.read_adc(i, gain=1)
        # 将 ADC 值转换为电压值
        voltage = value / 32767.0 * 4.096
        values[i] = voltage
        print("get", i, "value", voltage)
        time.sleep(0.5)

    # 打印 ADC 值
    print(values)
    time.sleep(1)
