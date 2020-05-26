from pyModbusTCP.client import ModbusClient

# TCP auto connect on first modbus request
c = ModbusClient(host="192.168.81.36", port=502, auto_open=True)
c.debug(True)
regs = c.write_single_coil(7206, 1)
if regs:
    print(regs)
else:
    print("read error")

