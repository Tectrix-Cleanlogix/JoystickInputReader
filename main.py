import time
import pygame
from pyModbusTCP.server import ModbusServer, DataBank
import threading

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Modbus server configuration
SERVER_HOST = '192.168.29.210'  # Change this to your server's IP address
SERVER_PORT = 502
server = ModbusServer(host=SERVER_HOST, port=SERVER_PORT, no_block=True)

# Start the Modbus server
server.start()

# Button names for Xbox 360 controller
BUTTON_NAMES = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "LB",
    5: "RB",
    6: "Back",
    7: "Start",
    8: "Left Stick",
    9: "Right Stick",
    10: "Xbox",
    11: "DPad Up",
    12: "DPad Down",
    13: "DPad Left",
    14: "DPad Right",
    15: "Guide",
    16: "Left Trigger",
    17: "Right Trigger",
    18: "Button 18",
    19: "Button 19",
    20: "Button 20",
    # Add more buttons as needed
}

# Function to update Modbus registers with joystick data
def update_registers():
    while True:
        # Read joystick data
        axis_values = [int(joystick.get_axis(i) * 100) for i in range(joystick.get_numaxes())]
        button_values = [int(joystick.get_button(i)) for i in range(joystick.get_numbuttons())]
        hat_values = [hat_val for hat_val in joystick.get_hat(0)]  # Assuming there's only one hat on the joystick
        values = axis_values + button_values + hat_values

        # Update Modbus holding registers using instance method
        server.data_bank.set_holding_registers(0, values)

        # Delay to avoid overwhelming the system
        time.sleep(0.500)

# Start the thread to update Modbus registers
update_thread = threading.Thread(target=update_registers)
update_thread.start()




# Define button names
BUTTON_NAMES = {
    0: "ButtonA",
    1: "ButtonB",
    2: "ButtonX",
    3: "ButtonY",
    4: "LeftShoulder",
    5: "RightShoulder",
    6: "LeftTrigger",
    7: "RightTrigger",
    8: "Back",
    9: "Start",
    10: "LeftStick",
    11: "RightStick",
    12: "DPadUp",
    13: "DPadDown",
    14: "DPadLeft",
    15: "DPadRight"
}

# Initialize variables to store button, axis, and hat values
button_values = {}
axis_values = {}
hat_values = {}
rsb_x_value = 0.0  # Initialize Right Stick X axis value
rsb_y_value = 0.0  # Initialize Right Stick Y axis value

# Main loop to handle events
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button_index = event.button
                button_name = BUTTON_NAMES.get(button_index, "Unknown")
                button_value = joystick.get_button(button_index)
                button_values[button_name] = button_value
                print("Button Values:", button_values)
                
            elif event.type == pygame.JOYAXISMOTION:
                axis_index = event.axis
                axis_value = joystick.get_axis(axis_index)
                
                # Assuming Right Stick's X and Y axes are indexed at 3 and 4 respectively
                if axis_index == 3:  # Right Stick X axis
                    rsb_x_value = axis_value
                elif axis_index == 4:  # Right Stick Y axis
                    rsb_y_value = axis_value
                    
                print("Right Stick X Value:", rsb_x_value)
                print("Right Stick Y Value:", rsb_y_value)
                
            elif event.type == pygame.JOYHATMOTION:
                hat_index = event.hat
                hat_name = "Hat " + str(hat_index)
                hat_value = joystick.get_hat(hat_index)
                hat_values[hat_name] = hat_value
                print("Hat Values:", hat_values)
                
except KeyboardInterrupt:
    pygame.quit()