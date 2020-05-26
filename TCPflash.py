from pyModbusTCP.client import ModbusClient
import time
import threading as th

keep_going = True

def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def blink():
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    print('aaaa')
    SERVER_HOST = "192.168.81.36"
    SERVER_PORT = 502

    c = ModbusClient()

    # uncomment this line to see debug message
    #c.debug(True)

    # define modbus server host, port
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)

    addr = 7206
    toggle = True
    print('cc')
    while keep_going:
        print('bbb')
        # open or reconnect TCP to server
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

        # if open() is ok, write coils (modbus function 0x01)
        if c.is_open():
            # write 4 bits in modbus address 0 to 3
            print("")
            print("write bits")
            print("----------")
            print("")
            
            is_ok = c.write_single_coil(addr, toggle)
            if is_ok:
                print("bit #" + str(addr) + ": write to " + str(toggle))
            else:
                print("bit #" + str(addr) + ": unable to write " + str(toggle))
            time.sleep(0.5)

            time.sleep(1)

            print("")
            print("read bits")
            print("---------")
            print("")
            bits = c.read_coils(addr, 1)
            if bits:
                print("bits #0 to 3: "+str(bits))
            else:
                print("unable to read")
        toggle = not toggle
        # sleep 2s before next polling
        time.sleep(0.5)

blink()

