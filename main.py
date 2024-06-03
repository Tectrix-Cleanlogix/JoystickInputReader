import time
import pygame
from pyModbusTCP.server import ModbusServer, DataBank
import threading

BUTTON_NAMES_PS5_DUALSENSE = {
    0: "Cross",
    1: "Cirlce",
    2: "Square",
    3: "Triangle",
    4: "Share",
    5: "Playstation",
    6: "Option",
    7: "L Stick",
    8: "R Stick",
    9: "L Bumper",
    10: "R Bumper",
    11: "Hat Up",
    12: "Hat Down",
    13: "Hat Left",
    14: "Hat Right",
    15: "Touchpad",
    16: "Power",
}

AXIS_NAMES_PS5_DUALSENSE = {
    0: "Left Stick X",
    1: "Left Stick Y",
    2: "Left Trigger",
    3: "Right Stick X",
    4: "Right Stick Y",
    5: "Right Trigger",
}

# Button names for Xbox 360 controller
BUTTON_NAMES_XBOX_360 = {
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

BUTTON_NAMES = BUTTON_NAMES_PS5_DUALSENSE
AXIS_NAMES = AXIS_NAMES_PS5_DUALSENSE

if __name__ == "__main__":

    # Initialize pygame and joystick
    pygame.init()
    pygame.joystick.init()

    #get count of joysticks
    if pygame.joystick.get_count() == 0:
        print("No joysticks found.")
        quit()
    else:
        print("Number of joysticks: ", pygame.joystick.get_count())
        print("Joystick names:")
        for i in range(pygame.joystick.get_count()):
            print(pygame.joystick.Joystick(i).get_name())

    joystick = pygame.joystick.Joystick(0)
    #get axis count, names, and initial values
    num_axes = joystick.get_numaxes()
    print("Number of axes: ", num_axes)
    print("Axis names and initial values:")
    for i in range(num_axes):
        print("Axis", i, ":", joystick.get_axis(i))

    #get button count and names
    num_buttons = joystick.get_numbuttons()
    print("Number of buttons: ", num_buttons)
    print("Button names:")
    for i in range(num_buttons):
        print("Button", i, ":", joystick.get_button(i))

    joystick.init()

    # Modbus server configuration
    SERVER_HOST = '10.1.10.33'  # Change this to your server's IP address
    SERVER_PORT = 502
    server = ModbusServer(host=SERVER_HOST, port=SERVER_PORT, no_block=True)

    # Start the Modbus server
    server.start()

    # Function to update Modbus registers with joystick data
    def update_registers():
        while True:
            # Read joystick data
            axis_values = [int(joystick.get_axis(i) * 100) for i in range(joystick.get_numaxes())]
            button_values = [int(joystick.get_button(i)) for i in range(joystick.get_numbuttons())]
            values = axis_values + button_values

            # Update Modbus holding registers using instance method
            server.data_bank.set_holding_registers(0, values)

            # Delay to avoid overwhelming the system
            print("Values:", values)
            time.sleep(0.500)

    # Start the thread to update Modbus registers
    update_thread = threading.Thread(target=update_registers)
    update_thread.start()

    # Initialize variables to store button and axis values
    button_values = {}
    axis_values = {}
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
                    #print(f"[button_index: {button_index}, button_name: {button_name}, button_value: {button_value}]")
                    
                elif event.type == pygame.JOYAXISMOTION:
                    axis_index = event.axis
                    axis_value = joystick.get_axis(axis_index)
                    
                    # Assuming Right Stick's X and Y axes are indexed at 3 and 4 respectively
                    if axis_index == 3:  # Right Stick X axis
                        rsb_x_value = axis_value
                    elif axis_index == 4:  # Right Stick Y axis
                        rsb_y_value = axis_value

                    #print(f"[axis_index: {axis_index}, axis_value: {axis_value}]")   
                    #print("Right Stick X Value:", rsb_x_value)
                    #print("Right Stick Y Value:", rsb_y_value)
                    
    except KeyboardInterrupt:
        pygame.quit()