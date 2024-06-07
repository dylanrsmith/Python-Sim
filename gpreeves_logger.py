from pymodbus.client import ModbusTcpClient
import time

# Modify these parameters according to your setup
SERVER_IP = '192.168.1.100'
SERVER_PORT = 502
STARTING_REGISTER = 40000
NUM_REGISTERS = 10
LOG_FILE = 'modbus_values.csv'

def log_modbus_values():
    with open(LOG_FILE, 'a') as f:
        f.write("Timestamp," + ','.join([f"Register_{i}" for i in range(NUM_REGISTERS)]) + "\n")
       
        client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)
        client.connect()

        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                # Read holding registers
                response = client.read_holding_registers(STARTING_REGISTER, NUM_REGISTERS, unit=1)

                if response.isError():
                    print("Error:", response)
                else:
                    # Write values to log file
                    timestamp = time.time()
                    values = response.registers
                    f.write(f"{timestamp}," + ','.join(map(str, values)) + "\n")
                    print("Logged values:", values)

            except Exception as e:
                print("Exception:", e)
           
            time.sleep(1)  # Adjust the interval as needed

        client.close()

if __name__ == "__main__":
    log_modbus_values()