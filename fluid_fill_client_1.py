# Modbus client
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from time import sleep

# Set Graco prodispense to static: 172.16.72.12
# Test ip was: 127.0.0.3

# NOW TESTING EDGEBOX FF
# for edgebox, slave index needs to be 1 when calling write_register or read_holding_registers

client = ModbusClient(host='192.168.1.155', port=502)

def write_register(reg, val):    
    data = [val]
    print('Write',data)
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG,\
    wordorder=Endian.LITTLE)
    for d in data:
        builder.add_16bit_int(int(d))
    payload = builder.build()
    # result  = client.write_registers(int(reg), payload, skip_encode=True, unit=int(0))
    result = client.write_register(reg,val,slave=1)    
    
    if(result):
        print("write success")
    else:
        print("write fail")


def read_register(reg):
    # rd = client.read_holding_registers(reg,0).registers    
    try:
        rd = client.read_holding_registers(reg,1,1)    
        print(f'Reading value:{rd} from register:{reg}')
    except Exception as e:
        print("Error: ")
        print(e)
    return rd

if __name__ == '__main__':
    # Device index needs to be 1 for edgebox.
    
    print("HELLO")    
    
    client.connect()
    print(client.connected)
    sleep(1)
    
    # read registers
    read_register(100) # read system state
    sleep(0.5)
    read_register(102) # read current recipe
    sleep(0.5)
    read_register(122) # read system status
    sleep(0.5)    
    read_register(154) # read current job volume
    sleep(0.5)
    read_register(170) # read last job volume
    sleep(0.5)
    read_register(186) # read current flow rate
    sleep(0.5)
    
    # write registers
    write_register(400,1) # write recipe
    sleep(0.5)
    write_register(402,2) # system state
    sleep(0.5)
    write_register(422,3) # system status
    sleep(0.5)
    write_register(454,4) # current job volume
    sleep(0.5)
    write_register(470,5) # last job volume (?)
    sleep(0.5)
    write_register(486,6) # current flow rate
    sleep(0.5)
        
    sleep(1)
    client.close()