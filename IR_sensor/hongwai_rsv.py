#!/usr/bin/python
#coding=utf8
import RPi.GPIO as gpio
import time
import datetime

#定义gpio引脚号
#BCM，物理引脚27号
pin=26
Lowtime=[0]*32
Hightime=[0]*32
msg=("用户码:","用户码反码:","按键码:","按键码反码:")
data=[0]*4
keeptime=0

gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.IN)

print("开始等待按键信号……")

while True:
	# 高电平，表示没有按键信号
	while gpio.input(pin)==1:
		continue

	# 低电平，表示按键信号出现，空循环等待直到出现高电平
	while gpio.input(pin)==0:
		continue

    # 开始读取数据，总共32个比特位，包括：用户码，用户码反码，按键码，按键码反码
	for i in range(0,32):
		# 记录低电平时刻
		while gpio.input(pin)==0:
			continue
		Lowtime[i]=datetime.datetime.now()

		# 记录高电平时刻
		while gpio.input(pin)==1:
			continue
		Hightime[i]=datetime.datetime.now()

    # 循环读取4个字节，每个字节8个比特位，分别是：用户码，用户码反码，按键码，按键码反码
    # 反码就是用255去减，比如原数据是50，那么它的反码就是255 - 50 = 205
    # 本代码使用的是NEC协议
    # 同一个遥控器，用户码是固定的
    # 如果要做红外遥控操作，则可以对用户码、用户码反码、按键码、按键码反码进行校验，校验通过就可以做自己的事情了，如果不校验的话，有可能会出现同一个按键每次的代码不相同的情况
	# 如果做的操作不区分按键的话，纯粹是判断有没有按键信号的话，那就可以不做校验也没问题
	for i in range(0,4):
		data[i]=0
		for j in range(0,8):
			# print(data)
			keeptime=Hightime[i*8+j]-Lowtime[i*8+j]
			print("keeptime:", i*8+j, keeptime)
			if keeptime.microseconds>1100:
				data[i]|=1<<j
			# print(keeptime.microseconds)
            
		print(msg[i]+str(data[i]))

	print(bin(data[0]), bin(data[1]), bin(data[2]), bin(data[3]))
	if data[0]&data[1]==0:
		print("用户码校验通过")
	else:
		print("注意：用户码校验不通过")

	if data[2]&data[3]==0:
		print("按键码校验通过")
	else:
		print("注意：按键码校验不通过")

	print("**********************")
	time.sleep(1)
