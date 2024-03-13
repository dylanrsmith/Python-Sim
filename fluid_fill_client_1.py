# Modbus client
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from time import sleep

# Set Graco prodispense to static: 172.16.72.12
# Test ip was: 127.0.0.3

def connect():
    print('Start Modbus Client')
    client = ModbusClient(host='172.16.72.12', port=502) 

def write_register(reg, val):    
    data = [val]
    print('Write',data)
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG,\
    wordorder=Endian.LITTLE)
    for d in data:
        builder.add_16bit_int(int(d))
    payload = builder.build()
    result  = client.write_registers(int(reg), payload,\
    skip_encode=True, unit=int(0))


def read_register(reg):
    rd = client.read_holding_registers(reg).registers
    print(f'Reading value:{rd} from register:{reg}')

    return rd

if __name__ == '__main__':
    print("HELLO")
    
    # Emulating Fluid Fill Log
    read_register(100)   # System State
    write_register(402,1)       
    read_register(100)
    write_register(402,2)
    read_register(100)
    # Set recipe
    write_register(400,21)
    sleep(1)
    write_register(400,21)
    read_register(102)