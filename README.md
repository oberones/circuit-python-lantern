# circuit-python-lantern
A circuit python playground express project for a programmable LED lantern using NeoPixels

# Requirements
- Circuit Playground Express
- Circuit Playground Python 8.x libraries

# Installation
1. Plug in CPE via usb
2. Click reset button to reveal CPLAYBOOT folder
3. Download latest release of circuit python from here: https://circuitpython.org/board/circuitplayground_express/
4. Drag the adafruit-circuitpython-circuitplayground_express-en_US-8.2.1.uf2 file to the CPLAYBOOT folder and wait for it to install and restart
5. Download the corresponding library zip from: https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/

6. Add the following folders/files to the lib folder in the new mounted CIRCUITPY folder
	adafruit_bus_device
	adafruit_circuitplayground
	adafruit_debouncer.mpy
	adafruit_lis3dh.mpy (?)
	adafruit_ticks.mpy
	neopixel.mpy

# Connect to Serial Console
## OSX
1. Find the tty device
```
ls /dev/tty.*
```

2. Connect to it with screen
```
screen /dev/tty.usbmodem114401 115200
```
