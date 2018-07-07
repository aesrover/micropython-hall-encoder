from machine import UART, Pin
from encoder import DualHallEncoder

from encoder.hall_sensor import HallEffectLatching


def main():
    # Setup hall sensors:
    h1 = HallEffectLatching(Pin(14))
    h2 = HallEffectLatching(Pin(12))

    # Setup UART:
    u = UART(0, baudrate=115200)

    # Initial write:
    u.write(b'START\n')

    # Setup encoder class:
    e = DualHallEncoder(h1, h2)

    # Main loop:
    while True:
        if e.detect_tick():  # Run tick detect
            # Report on UART if tick update:
            u.write(bytearray('DATA:{{"ticks":{}}}\n'.format(e.ticks)))


if __name__ == "__main__":
    main()
