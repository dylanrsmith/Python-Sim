# Modbus client
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from time import sleep

client = ModbusClient(host='192.168.0.117',port=80)     # Benson Fluid Fill box

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
    return 

def read_coil(reg):
    try: 
        rd = client.read_coils(reg,1,1)
        print(f'Reading value:{rd} from register: {reg}')
    except Exception as e:
        print("Error: ")
        print(e)
    
        

if __name__ == '__main__':
    # Device index needs to be 1 for edgebox.    
    print("HELLO")    
    
    client.connect()
    sleep(1)    
    print(client.connected)
    
    read_coil(100)    
    sleep(1)        

    client.close()