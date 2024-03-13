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
    
    port_one_vol = 0
    port_two_vol = 0
    port_three_vol = 0
    port_four_vol = 0
    
    recipe_one = [600,0,2000,0,100,0,0,0,0,0,0,0,0,0,0,0]
    recipe_two = [1200,0,300,0,300,0,300,0,0,0,0,0,0,0,0,0]
    recipe_three = [600,0,0,0,0,0,1500,0,0,0,0,0,0,0,0,0]
    
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
        if (address == 402):
            # set System State
            self.system_state = value
            print(self.system_state[0])
        if (address == 400):
            self.current_recipe = value
            
    def createRecipe(self):
        print(f"Create Recipe: {self.current_recipe}")
        print(self.current_job_vol)
        
    def getValues(self, address, count=1):
        """Return the requested values from the datastore.
           Automation inputs (from dispenser to modbus)
        """
        address=address-1
        result = super().getValues(address, count=count)
        print(f"Callback from getValues with address {address}")
        if (address == 100):
            #get System State
            return self.system_state
        elif (address == 102):
            #get current recipe
            return self.current_recipe
        elif (106 <= address <= 120):
            # get fluid panel state
            pass
        elif (122 <= address <= 136):
            # get fluid panel status
            pass
        elif (138 <= address <= 152):
            # Fluid panel events
            pass
        elif (154 <= address <= 168):
            # current job volume (cc)
            if self.current_recipe[0] != self.previous_recipe:
                self.previous_recipe = self.current_recipe[0]  
                self.port_one_vol = 0
                self.port_two_vol = 0
                self.port_three_vol = 0
                self.port_four_vol = 0
                
            if self.system_state[0] == 3:
                if self.current_recipe[0] == 1:
                    if self.port_one_vol < self.recipe_one[0]:
                        self.port_one_vol = self.port_one_vol + 6
                    if self.port_two_vol < self.recipe_one[2]:
                        self.port_two_vol = self.port_two_vol + 14
                    else:
                        print("Fill Complete")
                        super().setValues(402,2)
                        self.system_state[0] = 2
                    if self.port_three_vol < self.recipe_one[4]:
                        self.port_three_vol = self.port_three_vol + 9
                elif self.current_recipe[0] == 2:
                    if self.port_one_vol < self.recipe_two[0]:
                        self.port_one_vol = self.port_one_vol + 9
                    else:
                        print("Fill Complete")
                        super().setValues(402,2)
                        self.system_state[0] = 2
                    if self.port_two_vol < self.recipe_two[2]:
                        self.port_two_vol = self.port_two_vol + 13
                    if self.port_three_vol < self.recipe_two[4]:    
                        self.port_three_vol = self.port_three_vol + 11
                    if self.port_four_vol < self.recipe_two[6]:
                        self.port_four_vol = self.port_four_vol + 9
                elif self.current_recipe[0] == 3:
                    if self.port_one_vol < self.recipe_three[0]:
                        self.port_one_vol = self.port_one_vol + 11
                    if self.port_four_vol < self.recipe_three[6]:
                        self.port_four_vol = self.port_four_vol + 13
                    else:
                        print("Fill Complete")
                        super().setValues(402,2)
                        self.system_state[0] = 2
                    
            return [self.port_one_vol,0,self.port_two_vol,0,self.port_three_vol,0,self.port_four_vol,0,0,0,0,0,0,0,0,0]
        elif (170 <= address <= 184):
            # last job volume (cc)
            pass
        elif (186 <= address <= 200):
            # current flow (cc/min)            
            pass
        elif (202 <= address <= 216):
            # dispense target
            if self.current_recipe[0] == 1:
                return self.recipe_one
            elif self.current_recipe[0] == 2:
                return self.recipe_two
            elif self.current_recipe[0] == 3:
                return self.recipe_three
        elif (218 <= address <= 232):
            # dispense tolerance %
            pass
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
    