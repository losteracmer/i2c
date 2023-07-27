import RPi.GPIO as GPIO
import time
from queue import Queue
# 红外传感器的引脚
IR_PIN = 26

# 初始化GPIO口
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)

# NEC红外解码器参数
HEADER_MARK = 9000
HEADER_SPACE = 4500
BIT_MARK = 560
ONE_SPACE = 1690
ZERO_SPACE = 560
END_SPACE = 11000

q = Queue()

# 解码NEC红外信号
def nec_decode(data):
    # 将数据转换为二进制格式
    binary_data = bin(data)[2:].zfill(32)

    # 解析数据格式
    address = int(binary_data[0:8], 2)
    address_inv = int(binary_data[8:16], 2)
    command = int(binary_data[16:24], 2)
    command_inv = int(binary_data[24:32], 2)
    msg=("用户码:","用户码反码:","按键码:","按键码反码:")
    print(msg[0], address)
    print(msg[1], address_inv)
    print(msg[2], command)
    print(msg[3], command_inv)
    # 判断数据是否合法
    if (address ^ address_inv) != 0xFF or (command ^ command_inv) != 0xFF:
        return None

    # 返回解码结果
    return (address, command)

def push_to_queen(channel):
    # 第一个不能为高电平
    print("receive: ",  "HIGH" if GPIO.input(channel) == GPIO.HIGH else "LOW", time.time())
    if q.qsize() == 0 and GPIO.input(channel) == GPIO.HIGH:
        print("skip this sign")
        return
    q.put((GPIO.input(channel), time.time()))
    # 判断队列长度是否=33
    if q.qsize() == 68:
        (header_begin, begin) = q.get()
        (header_end, end) = q.get()
        print("header mark", (end-begin)*1000000)
        (healder_sign, sign) = q.get()
        print("header space", (sign - end)*1000000)
        # 将队列中的数据取出做计算
        data=0
        for i in range(32):
            (w, begin) = q.get()
            (ww, end) = q.get()
            # print("高电平", w == GPIO.HIGH)
            # print("低电平", ww != GPIO.HIGH)
            print( "HIGH" if w == GPIO.HIGH else "LOW", " -> ",  "HIGH" if ww == GPIO.HIGH else "LOW")
            duration = int((end - begin) * 1000000)
            print("%d \t" %i, duration)
            if ONE_SPACE - 500 < duration:
                data |= (1 << (31 - i))
        print("bin data:", bin(data))
        result = nec_decode(data)
        if result is not None:
                print("Received NEC IR signal: address={}, command={}".format(result[0], result[1]))
        else:
                print("Recived NEC IR is malformed")
        # 清空队列
        while not q.empty():
            q.get()

# 中断处理函数，用于读取红外遥控发出的信号
def handle_ir_signal(channel):
    global start_time, data 

    # 记录信号开始时间
    if GPIO.input(channel) == GPIO.HIGH:
        start_time = time.time()
        print("high", time.time())
    else:
        # 计算信号持续时间
        print("low", time.time())
        duration = int((time.time() - start_time) * 1000000)

        if HEADER_MARK - 500 < duration < HEADER_MARK + 500:
            # 解码数据位
            data = 0
            for i in range(32):
                # 等待下一个数据位的开始
                while GPIO.input(IR_PIN) == GPIO.HIGH:
                    pass

                # 计算数据位持续时间
                duration = int((time.time() - start_time) * 1000000)

                if ONE_SPACE - 500 < duration < ONE_SPACE + 500:
                    data |= (1 << (31 - i))
                elif ZERO_SPACE - 500 < duration < ZERO_SPACE + 500:
                    pass
                else:
                    return

            # 解码NEC红外信号
            result = nec_decode(data)
            if result is not None:
                print("Received NEC IR signal: address=0x{:02X}, command=0x{:02X}".format(result[0], result[1]))
            else:
                print("Recived NEC IR is malformed")

# 设置GPIO引脚状态变化时的中断处理函数
# GPIO.add_event_detect(IR_PIN, GPIO.BOTH, callback=handle_ir_signal)
GPIO.add_event_detect(IR_PIN, GPIO.BOTH, callback=push_to_queen)

# 循环等待中断处理程序执行
try:
    while True:
        time.sleep(1)
        # print("size", q.qsize())
        # print(q.queue)
except KeyboardInterrupt:
    GPIO.cleanup()
