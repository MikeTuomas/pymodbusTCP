from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from pyModbusTCP.client import ModbusClient
import struct
import time
import numpy as np 
import threading as th
import guiLoop   

def send_button_pressed():
    state = []
    continous_run = chk_cont.get()
    generator = send_message(btn_start, state, continous_run)
    btn_start['text'] = 'Stop'  
    def turn_off():
        state.append('stop')
        btn_start['command'] = send_button_pressed
        btn_start['text'] = 'Send'
    btn_start['command'] = turn_off

@guiLoop.guiLoop    
def send_message(state, cont):
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
    while state != ['stop']: #tähän jatkuva rekisterin päivitys
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

            else: print("Wrong function code")
        
        if cont == False:
            state.append('stop')
            btn_start['command'] = send_button_pressed
            btn_start['text'] = 'Send'
        # sleep before next polling
        yield(0.5)

    c.close()
    print("Connection is closed")

window = Tk()
window.title('Modbus TCP test client')
# window.geometry('320x200')
lbl_modbus = Label(window, text='Modbus server IP address')
lbl_modbus.grid(column=0,row=0, pady = 2, sticky = W)
txt_modbus_ip = Entry(window, width=23)
txt_modbus_ip.grid(column=1, row=0, pady = 2, sticky = W)
txt_modbus_ip.focus()
txt_modbus_ip.insert('0','192.168.81.45')

lbl_fc = Label(window, text='Function code')
lbl_fc.grid(column=0, row=1, stick = W, pady = 2)
txt_fc = Combobox(window)
txt_fc['values'] = ('02', '04')
txt_fc.current(0)
txt_fc.grid(column=1, row=1, pady = 2, sticky = W)

lbl_address = Label(window, text='Starting register address')
lbl_address.grid(column=0, row=2, stick = W, pady = 2)
txt_address = Entry(window, width=23)
txt_address.grid(column=1,row=2, pady = 2)
txt_address.insert('0','7202')

lbl_lenght = Label(window, text='register lenght')
lbl_lenght.grid(column=0,row=3, stick = W, pady = 2)
txt_lenght = Entry(window, width=23)
txt_lenght.grid(column=1,row=3, pady = 2)
txt_lenght.insert('0','1')

# txt_ = scrolledtext.ScrolledText(window, width=40, height=10, state='disabled')
# txt.grid(column=1, row=0)
chk_cont = BooleanVar()
chk_cont.set(False)
chk_continous_send = Checkbutton(window, text='Send continously', var=chk_cont)
chk_continous_send.grid(column=3,row=0)

btn_start = Button(window, text='Send', command=send_button_pressed)
btn_start.grid(column=2,row=0, pady = 2)

window.mainloop()
