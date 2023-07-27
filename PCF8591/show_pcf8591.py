import smbus
import time
bus = smbus.SMBus(1)
address = 0x48
ains = [0x40, 0x41, 0x42, 0x43, 0x44]
"""

接在5v的电源上,显示比较正常
这五个地址,其中0x40 == 0x41
其余的分别对应后面的输出口
input0是电位器
input1是光敏电阻
input2是热敏电阻?

J6短接，0x44是电位器
J5短接，0x40,0x41是光敏电阻
J4短接，0x42是热敏电阻？
"""

values = [0]*5
infos = [0]*5
while True:
    for i, ain in enumerate(ains):
        bus.write_byte(address, ain)
        values[i] = bus.read_byte(address)
        infos[i] = (values[i]*5/255)
        # print("AOUT:%1.3f  " %(values[i]*3.3/255))
        time.sleep(0.12)
    print(values)
    print(infos)

