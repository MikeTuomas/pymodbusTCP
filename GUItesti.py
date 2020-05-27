from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
def send_message():
    pass


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

# combo = Combobox(window)
# combo['values'] = (1,2,3,'text')
# combo.current(1)
# combo.grid(column=3,row=0)

# def clicked():
#     res = 'welcome to ' + txt.get()
#     lbl.configure(text= res)

btn = Button(window, text='send', command=send_message)
btn.grid(column=2,row=0)

window.mainloop()
