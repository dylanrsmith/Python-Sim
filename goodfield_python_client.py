# Modbus client
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from time import sleep

# Set Graco prodispense to static: 172.16.72.12
# Test ip was: 127.0.0.3

print('Start Modbus Client')
# client = ModbusClient(host='127.0.0.3', port=502) 
client = ModbusClient(host='192.168.1.155',port=502)

def write_register(reg, val):    
    data = [val]
    print('Write',data)
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG,\
    wordorder=Endian.LITTLE)
    for d in data:
        builder.add_16bit_int(int(d))
    payload = builder.build()
    result = client.write_register(int(reg), val, 1)
    print(result)


def read_register(reg):
    rd = client.read_holding_registers(reg,1,1)
    print(f'Reading value:{rd.registers} from register:{reg}')

    return rd

if __name__ == '__main__':
    print("HELLO")
    # Emulating Fluid Fill Log - Graco:
    
    print("reading system state")
    read_register(100)
    
    print("writing system state")
    write_register(402,2)
    
    print("reading back system state")
    read_register(100)
    
    print("reading recipe: ")
    read_register(102)
    
    print("writing recipe as 3:")
    write_register(400,2)
    
    print("reading back recipe: ")
    read_register(102)
    
    print("set sytem state to fill")
    write_register(402,3)
    
    print("Read back system state")
    read_register(100)