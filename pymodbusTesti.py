from pymodbus.client.sync import ModbusTcpClient



SERVER_HOST = '192.168.81.36'
addr = 8005

client = ModbusTcpClient(SERVER_HOST)

result = client.read_input_registers(addr,2)
print(result.registers[0:])
client.close()