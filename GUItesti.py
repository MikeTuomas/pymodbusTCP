from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from pyModbusTCP.client import ModbusClient
import struct
import time
import numpy as np 
import threading as th
from guiLoop import guiLoop, stopLoop  

class stopper:
    def __init__(self):
        self.state = 0
    def stop(self):
        self.state = 1
class checkker:
    def __init__(self):
        self.state = 0
    

def stop_sending():
    
    s.stop()

def send_button_pressed():
    stoppaaja = stopper()
    saie = th.Thread(target=send_message(stoppaaja), args=(), name='send_message', daemon=True).start()
    
def send_message(stop):
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
    running = 1
    while running: #tähän jatkuva rekisterin päivitys
    # open or reconnect TCP to server
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+str(txt_modbus_ip)+":"+str(port))

        # if open() is ok, write
        if c.is_open():
            
            yield(1)

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
                    bitreg = (bits1[0] << 16) + bits1[1]
                    s = struct.pack('>HH', bits1[0], bits1[1])
                    final = struct.unpack('>f', s)[0]

                    print("Force is: " +str(final/1000)[0:5]+str("Nm"))
                    
                else:
                    print("Unable to read")

            else: print("Wrong fuction code")
        
        if not chk_cont:
            running = 0
        if stop.state:
            running = 0
        # sleep before next polling
        yield(0.5)
    c.close()
    print("Connection is closed")



window = Tk()
window.title('Modbus TCP test client')
# window.geometry('320x200')
s = stopper()
lbl_modbus = Label(window, text='Modbus server IP address')
lbl_modbus.grid(column=0,row=0)
txt_modbus_ip = Entry(window, width=20)
txt_modbus_ip.grid(column=1, row=0)
txt_modbus_ip.focus()
txt_modbus_ip.insert('0','192.168.81.36')

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
txt_address.insert('0','7901')

lbl_lenght = Label(window, text='register lenght')
lbl_lenght.grid(column=0,row=3)
txt_lenght = Entry(window, width=20)
txt_lenght.grid(column=1,row=3)
txt_lenght.insert('0','1')

# txt_ = scrolledtext.ScrolledText(window, width=40, height=10, state='disabled')
# txt.grid(column=1, row=0)
chk_cont = BooleanVar()
chk_cont.set(False)
chk_continous_send = Checkbutton(window, text='Send continously', var=chk_cont)
chk_continous_send.grid(column=3,row=0)

btn_start = Button(window, text='Send', command=send_button_pressed)
btn_start.grid(column=2,row=0)

btn_stop = Button(window, text='Stop', command=stop_sending)
btn_stop.grid(column=2,row=1)



window.mainloop()
