import utime
from machine import Pin

from encoder.hall_sensor import HallEffectLatching


h1 = HallEffectLatching(Pin(14))
h2 = HallEffectLatching(Pin(12))


# == Run functions == :
def continuous_run():
    while True:
        print("\rHall Values: {} | {}".format(h1.value(), h2.value()), end="  ")
        utime.sleep_ms(50)


def event_only():
    def print_event(t, e):
        if not e == 0:
            print("{} EVENT UPDATE: {} [{}ms ago]".format(t, *e))

    while True:
        # Read:
        h1.value(); h2.value()
        e1, e2 = h1.get_new_event(), h2.get_new_event()

        print_event(1, e1)
        print_event(2, e2)


def dir_print_run():
    last_handled = None

    while True:
        h1.value(); h2.value()
        if (not h1.last_event == last_handled) and h1.last_event == h2.last_event:
            last_handled = h1.last_event
            diff = utime.ticks_diff(h2.last_event_ms, h1.last_event_ms)
            if diff > 0:
                print("1 -> 2")
            elif diff < 0:
                print("2 -> 1")
            else:
                print("neither??")


def enc_tick_count_run():
    last_handled_1_ms = None
    last_handled_2_ms = None

    tick_count = 0

    while True:
        h1.value(); h2.value()
        if ((not h1.last_event_ms == last_handled_1_ms or not h2.last_event_ms == last_handled_2_ms)
                and h1.last_event == h2.last_event):
            last_handled_1_ms = h1.last_event_ms
            last_handled_2_ms = h2.last_event_ms
            diff = utime.ticks_diff(h2.last_event_ms, h1.last_event_ms)
            if diff > 0:
                tick_count += 1
            elif diff < 0:
                tick_count -= 1
        print("\rTicks: {}".format(tick_count), end="")


def usb_serial_comm():
    import utime
    from machine import UART

    #u = UART(0, baudrate=115200)
    u = UART(0)
    u.write(b'START\n')
    for i in range(0, 10):
        s = 'DATA:{{"i":{}}}\n'.format(i)
        u.write(bytearray(s))
        utime.sleep_ms(1000)


def usb_serial_ticks():
    import utime
    from machine import UART
    from encoder import DualHallEncoder

    u = UART(0, baudrate=115200)
    u.write(b'START\n')
    e = DualHallEncoder(h1, h2)
    while True:
        if e.detect_tick():
            u.write(bytearray('DATA:{{"ticks":{}}}\n'.format(e.ticks)))



# Executes on uproc start:
def main():
    #continuous_run()
    #event_only()
    #dir_print_run()
    #enc_tick_count_run()
    #usb_serial_comm()
    usb_serial_ticks()
