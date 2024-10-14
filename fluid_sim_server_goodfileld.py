# Modbus server (TCP)
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from time import sleep
import asyncio

ip = "127.0.0.3"

class CallbackDataBlock(ModbusSequentialDataBlock):
    # modbus fill variables
    num_panels = 8
    system_state = 0            # System Wide
    current_recipe = 0          # Current Recipe
    previous_recipe = 0 
    current_job_num = 0         # Current Job Number
    fluid_panel_state_reg = [106,108,110,112,114,116,118,120]
    fluid_panel_states = {}     # Values for each fluid panel
    fluid_panel_status_reg = [122,124,126,128,130,132,134,136]
    fluid_panel_status = {}     # status bits for each panel
    fluid_panel_event = {}      # error bits for each panel
    current_job_vol_reg = [154,156,158,160,162,164,166,168]
    current_job_vol = {}        # values in cc for each panel. a val of 1250 = 12.50 cc
    last_job_vol_reg = [170,172,174,176,178,180,182,184]
    last_job_vol = {}           # values in cc for the last completed job for each panel
    current_flow_reg = [186,188,190,192,194,196,198,200]
    current_flow = {}           # flow in cc/min.
    dispense_target = {}        # i.e. 700 = 7.00 cc
    dispense_tolerance = {}     # acceptable fill range in percentage: 12 = 12%
    grand_total_volume = {}     
    grand_total_units = 0

    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0
    second = 0
    minute_second = 0
    
    reg_write_year = 1
    reg_write_month = 2
    reg_write_day = 3
    reg_write_hour = 4
    reg_write_minute = 5
    reg_write_second = 6
    reg_write_minute_second = 10
    reg_read_year = 1
    reg_read_month = 2
    reg_read_day = 3
    reg_read_hour = 4
    reg_read_minute = 5
    reg_read_second = 6
    reg_read_minute_second = 10

    def __init__(self, queue, addr, values):
        """Initialize."""
        self.queue = queue
        super().__init__(addr, values)

    def setValues(self, address, value):
        """Set the requested values of the datastore.
            Automation Outputs (to dispenser from modbu)
        """
        super().setValues(address-1, value)
        print(f"Callback from setValues with address {address-1}, value {value}")
        
        address=address-1
        if (address == self.reg_write_year):
            # set System State
            self.year = value
            print(self.year)
        elif (address == self.reg_write_month):
            self.month = value
            print(self.month)
        elif (address == self.reg_write_day):
            self.day = value
            print(self.day)
        elif (address == self.reg_write_hour):
            self.hour = value
            print(self.hour)
        elif (address == self.reg_write_minute):
            self.minute = value
            print(self.minute)
        elif (address == self.reg_write_second):
            self.second = value
            print(self.second)
        elif (address == self.reg_write_minute_second):
            self.minute_second = value
            print(self.minute_second)
        else:
            print("invalid write address")

    def getValues(self, address, count=1):
        """Return the requested values from the datastore.
           Automation inputs (from dispenser to modbus)
        """
        address=address-1
        result = super().getValues(address, count=count)
        print(f"Callback from getValues with address {address}")
        if (address == 1):
            #get year
            return self.year
        elif (address == 2):
            #get month
            return self.month
        elif (address == 3):
            # get day
            return self.day
        elif (address == 4):
            # get hour
            return self.hour
        elif (address == 5):
            # get min
            return self.minute
        elif (address == 6):
            # get second
            return self.second
        elif (address == self.reg_read_minute_second):
            return self.minute_second
        else:
            return [11,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            # return result

    def validate(self, address, count=1):
        """Check to see if the request is in range."""
        result = super().validate(address-1, count=count)
        return result

def run_async_server():
    nreg = 830      # number of registers
    queue = asyncio.Queue()
    block = CallbackDataBlock(queue,0x00, [0]*nreg)
    store = ModbusSlaveContext(hr=block)
    context = ModbusServerContext(slaves=store, single=True)
    # initialize the server information
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'FargoEngineering'
    identity.ProductCode = 'FEI-MB'
    identity.VendorUrl = 'https://feimodbus.com'
    identity.ProductName = 'Modbus Server'
    identity.ModelName = 'Modbus Server'
    identity.MajorMinorRevision = '3.0.2'

    # TCP Server
    server = StartTcpServer(context=context, host='localhost',identity=identity, address=(ip, 502))

if __name__ == "__main__":
    print(f"Modbus server started on {ip} port 502")
    run_async_server()
    