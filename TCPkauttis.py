from pyModbusTCP.client import ModbusClient
import struct
import time
import threading as th

keep_going = True

def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def blink():
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    txt_modbus_ip = "192.168.81.45"
    port = 502

    c = ModbusClient()

    # uncomment this line to see debug message
    #c.debug(True)

    # define modbus server host, port
    c.host(txt_modbus_ip.get())
    c.port(port)

    address = txt_address.get()
    lenght = txt_lenght.get()
    fc = txt_fc.get()
    
    while keep_going:
        # open or reconnect TCP to server
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+txt_modbus_ip+":"+str(port))

        # if open() is ok, write
        if c.is_open():
            
            time.sleep(1)

            if fc == "02"

                print("")
                print("Message")
                print("")
                bits = c.read_discrete_inputs(address, lenght)
                print(bits)
                

            else if fc == "04"

                print("")
                print("Message")
                print("")
                bits = c.read_input_register(address, lenght)
                if bits:
                    float_bits = [float(i) for i in bits]
                    #print("bits #0 to 3: "+str(bits))
                    #print(float_bits)

                    bitreg = (bits[0] << 16) + bits[1]
                    s = struct.pack('>HH', bits[0], bits[1])
                    final = struct.unpack('>f', s)[0]

                    print("Force is: " +str(final/1000)[0:5]+str("Nm"))
                    
                else:
                    print("Unable to read")

            else: print("Wrong fuction code")
        
        # sleep before next polling
        time.sleep(0.5)
    c.close()
    print("Connection is. " +str(c.is_open()))
blink()


