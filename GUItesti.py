from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from pyModbusTCP.client import ModbusClient
import struct
import time
import numpy as np 

def send_message():
    port = 502

    c = ModbusClient()

    # uncomment this line to see debug message
    #c.debug(True)

    # define modbus server host, port
    c.host(txt_modbus_ip.get())
    c.port(port)

    address = np.int16(txt_address.get())
    lenght = np.int16(txt_lenght.get())
    fc = txt_fc.get()
    
    # while keep_going: #tähän jatkuva rekisterin päivitys
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+txt_modbus_ip+":"+str(port))

    # if open() is ok, write
    if c.is_open():
        
        time.sleep(1)

        if fc in ["02"]:

            print("")
            print("Message")
            print("")
            bits = c.read_discrete_inputs(address, lenght)
            print('Input status',bits)
            

        elif fc in ["04"]:

            print("")
            print("Message")
            print("")
            bits1 = c.read_input_registers(address, lenght)
            if bits1:
                float_bits = [float(i) for i in bits1]
                #print("bits #0 to 3: "+str(bits))
                #print(float_bits)

                bitreg = (bits1[0] << 16) + bits1[1]
                s = struct.pack('>HH', bits1[0], bits1[1])
                final = struct.unpack('>f', s)[0]

                print("Force is: " +str(final/1000)[0:5]+str("Nm"))
                
            else:
                print("Unable to read")

        else: print("Wrong fuction code")
    
    # sleep before next polling
    time.sleep(0.5)
    c.close()
    print("Connection is closed")


window = Tk()
window.title('Modbus TCP test client')
# window.geometry('320x200')

lbl_modbus = Label(window, text='Modbus server IP address')
lbl_modbus.grid(column=0,row=0)
txt_modbus_ip = Entry(window, width=20)
txt_modbus_ip.grid(column=1, row=0)
txt_modbus_ip.focus()

lbl_fc = Label(window, text='Function code')
lbl_fc.grid(column=0, row=1)
txt_fc = Combobox(window)
txt_fc['values'] = ('02', '04')
txt_fc.current(1)
txt_fc.grid(column=1, row=1)

lbl_address = Label(window, text='Starting register address')
lbl_address.grid(column=0, row=2)
txt_address = Entry(window, width=20)
txt_address.grid(column=1,row=2)

lbl_lenght = Label(window, text='register lenght')
lbl_lenght.grid(column=0,row=3)
txt_lenght = Entry(window, width=20)
txt_lenght.grid(column=1,row=3)


# txt_ = scrolledtext.ScrolledText(window, width=40, height=10, state='disabled')
# txt.grid(column=1, row=0)


btn = Button(window, text='send', command=send_message)
btn.grid(column=2,row=0)

window.mainloop()
