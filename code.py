import board
import time
import random
from adafruit_debouncer import Debouncer
from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground import cp

cp.pixels.auto_write = False
cp.pixels.brightness = 0.3

# Set up the button pins directly
button_a_pin = DigitalInOut(board.BUTTON_A)
button_a_pin.direction = Direction.INPUT
button_a_pin.pull = Pull.DOWN
button_a_debounced = Debouncer(button_a_pin)

button_b_pin = DigitalInOut(board.BUTTON_B)
button_b_pin.direction = Direction.INPUT
button_b_pin.pull = Pull.DOWN
button_b_debounced = Debouncer(button_b_pin)

# Define the color spectrum
colors = [
    (255, 0, 0),  # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (75, 0, 130),  # Indigo
    (148, 0, 211),  # Violet
]

# Function to interpolate colors (used by config_spectrum)
def interpolate_color(color1, color2, steps):
    step_size = 1.0 / steps
    interp_colors = []
    for i in range(steps):
        r = int((1.0 - step_size * i) * color1[0] + step_size * i * color2[0])
        g = int((1.0 - step_size * i) * color1[1] + step_size * i * color2[1])
        b = int((1.0 - step_size * i) * color1[2] + step_size * i * color2[2])
        interp_colors.append((r, g, b))
    return interp_colors


# Function to cycle through the color spectrum
def config_spectrum():
    print("Starting spectrum animation")
    i = 0
    while True:
        current_color = colors[i]
        next_color = colors[(i + 1) % len(colors)]
        transition_steps = 50
        i_colors = interpolate_color(current_color, next_color, transition_steps)

        for step_color in i_colors:
            cp.pixels.fill(step_color)
            cp.pixels.show()
            time.sleep(0.05)

            # Update button states
            button_a_debounced.update()
            button_b_debounced.update()

            # Check for button presses
            if button_a_debounced.fell or button_b_debounced.fell:
                return  # Return from the function if a button was pressed

        time.sleep(0.5)
        i = (i + 1) % len(colors)


def config_fire():
    print("Starting fire animation")
    while True:
        # Generate random variations for red, green, and blue channels
        flicker_r = random.randint(150, 255)
        flicker_g = random.randint(50, 150)
        flicker_b = random.randint(0, 50)

        flicker_color = (flicker_r, flicker_g, flicker_b)

        cp.pixels.fill(flicker_color)
        cp.pixels.show()
        time.sleep(random.uniform(0.05, 0.1))

        # Update button states
        button_a_debounced.update()
        button_b_debounced.update()

        # Check for button presses
        if button_a_debounced.fell:
            print ("Breaking - button a pressed")
            break  # Break out of the loop if a button was pressed

        if button_b_debounced.fell:
            print ("Breaking - button b pressed")
            break  # Break out of the loop if a button was pressed


# Configuration variable
current_config = 0  # Start with the first configuration (0 = cycle through spectrum)

# Main loop
while True:
    print("Starting main loop")
    config_map = {
        0: config_fire,
        1: config_spectrum
    }
    max_config = len(config_map) - 1

    # Left button press (A)
    if button_a_debounced.fell:
        print("Left button pressed")
        current_config = (current_config - 1) % (max_config + 1)

    # Right button press (B)
    if button_b_debounced.fell:
        print("Right button pressed")
        current_config = (current_config + 1) % (max_config + 1)

    # Read button states
    button_a_debounced.update()
    button_b_debounced.update()

    # Call the current configuration function
    print(current_config)
    config_map[current_config]()
