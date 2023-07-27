import RPi.GPIO as GPIO
import time

# 红外传感器的引脚
IR_PIN = 26

# 初始化GPIO口
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)

# NEC红外解码器参数
HEADER_MARK = 9000
HEADER_SPACE = 4500
BIT_MARK = 560
ONE_SPACE = 1600
ZERO_SPACE = 560
END_SPACE = 11000

# 解码NEC红外信号
def nec_decode(data):
    print("data:", bin(data))
    # 将数据转换为二进制格式
    binary_data = bin(data)[2:].zfill(32)



    # 解析数据格式
    address = int(binary_data[0:8], 2)
    address_inv = int(binary_data[8:16], 2)
    command = int(binary_data[16:24], 2)
    command_inv = int(binary_data[24:32], 2)

    # 判断数据是否合法
    if (address ^ address_inv) != 0xFF or (command ^ command_inv) != 0xFF:
        return None

    # 返回解码结果
    return (address, command)

# 循环读取红外遥控发出的信号
while True:
    # 等待红外遥控发出信号
    while GPIO.input(IR_PIN) == GPIO.HIGH:
        pass

    

    # 等待信号头部出现
    while GPIO.input(IR_PIN) == GPIO.LOW:
        pass
    # 记录信号开始时间
    start_time = time.time()
    while GPIO.input(IR_PIN) == GPIO.HIGH:
        pass

   

    # 等待信号头部结束
    duration = int((time.time() - start_time) * 1000000)
    print("header time", duration)
    if HEADER_MARK - 500 < duration < HEADER_MARK + 500:
        # 解码数据位
        data = 0
        for i in range(32):
            # 等待数据位出现
            while GPIO.input(IR_PIN) == GPIO.LOW:
                pass

            # 记录数据位开始时间
            bit_start_time = time.time()

            while GPIO.input(IR_PIN) == GPIO.HIGH:
                pass

            
            # 等待数据位结束
            # duration = int((time.time() - bit_start_time) * 1000000)
            duration = int((time.time() - bit_start_time) * 1000000)
            print("i", duration)
            if duration > ONE_SPACE:
                data |= 1 << (31 - i)
           

        # 等待信号结束
        while GPIO.input(IR_PIN) == GPIO.LOW:
            pass

        # 输出解码结果
        result = nec_decode(data)
        if result is not None:
            print('Address: {}, Command: {}'.format(result[0], result[1]))

    # 等待信号结束
    while GPIO.input(IR_PIN) == GPIO.HIGH:
        pass
