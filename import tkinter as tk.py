import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from pyModbusTCP.client import ModbusClient
from binascii import hexlify
import time

def blink():
    SERVER_HOST = "192.168.81.45"
    SERVER_PORT = 502

    c = ModbusClient()

    # uncomment this line to see debug message
    #c.debug(True)

    # define modbus server host, port
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)

    addr = 7701
    str = 'palikan_nostelu'.encode()
    # print(str)
    res= hexlify(str)
    send = res + b'5c30'
    # print(send)
    send = [0x6161,0x5c30]
    print(send)
    # send.append(0x5c30)
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write
    if c.is_open():
        
        print("")
        print("write bits")
        print("")
        
        is_ok = c.write_multiple_registers(addr, send)

        time.sleep(0.5)

    
        print("")
        print("read bits")
        print("")
        # bits = c.read_coils(addr, 1)

    # sleep before next polling
    time.sleep(0.5)

blink()