import board
import math
import time
import random
from adafruit_debouncer import Debouncer
from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground import cp

cp.pixels.auto_write = False
cp.pixels.brightness = 0.3
button_a_pin = DigitalInOut(board.BUTTON_A)
button_a_pin.direction = Direction.INPUT
button_a_pin.pull = Pull.DOWN
button_a_debounced = Debouncer(button_a_pin)
button_b_pin = DigitalInOut(board.BUTTON_B)
button_b_pin.direction = Direction.INPUT
button_b_pin.pull = Pull.DOWN
button_b_debounced = Debouncer(button_b_pin)


def config_fire():
    while True:
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
        if button_a_debounced.fell or button_b_debounced.fell:
            return


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

# Function to interpolate colors
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
            button_a_debounced.update()
            button_b_debounced.update()
            if button_a_debounced.fell or button_b_debounced.fell:
                return
        time.sleep(0.5)
        i = (i + 1) % len(colors)


def complementary_color(color):
    """Return the complementary color."""
    return (255 - color[0], 255 - color[1], 255 - color[2])


def blend_colors(color1, color2, weight=0.5):
    """Blend two colors together. Weight determines the balance of the blend."""
    r = int(color1[0] * weight + color2[0] * (1 - weight))
    g = int(color1[1] * weight + color2[1] * (1 - weight))
    b = int(color1[2] * weight + color2[2] * (1 - weight))
    return (r, g, b)


def config_psychedelic():
    while True:
        for i in range(len(colors)):  # Base layer: spectrum animation
            base_color = colors[i]
            comp_color = complementary_color(base_color)  # Get the complementary color

            # Interpolate colors for smooth transition
            transition_steps = 30
            next_color = colors[(i + 1) % len(colors)]
            interp_colors = interpolate_color(base_color, next_color, transition_steps)

            for step_color in interp_colors:
                cp.pixels.fill(step_color)  # Fill all LEDs with the base color

                # Top layer: two dynamic LEDs with complementary color
                for j in range(10):  # Move the dynamic LEDs around the circle
                    blend_color = blend_colors(
                        step_color, complementary_color(step_color)
                    )

                    # Set main dynamic LEDs
                    cp.pixels[j] = complementary_color(step_color)
                    cp.pixels[(j + 5) % 10] = complementary_color(step_color)

                    # Set blending effect for neighboring LEDs
                    cp.pixels[(j + 1) % 10] = blend_color
                    cp.pixels[(j - 1) % 10] = blend_color
                    cp.pixels[(j + 6) % 10] = blend_color
                    cp.pixels[(j + 4) % 10] = blend_color

                    cp.pixels.show()
                    button_a_debounced.update()
                    button_b_debounced.update()
                    if button_a_debounced.fell or button_b_debounced.fell:
                        return
                    time.sleep(0.05)

                    # Reset LEDs for next iteration
                    for k in range(10):
                        cp.pixels[k] = step_color


current_config = 0
while True:
    config_map = {0: config_fire, 1: config_spectrum, 2: config_psychedelic}
    max_config = len(config_map) - 1
    if button_a_debounced.fell:
        current_config = (current_config - 1) % (max_config + 1)
    if button_b_debounced.fell:
        current_config = (current_config + 1) % (max_config + 1)
    button_a_debounced.update()
    button_b_debounced.update()
    print(current_config)
    config_map[current_config]()
