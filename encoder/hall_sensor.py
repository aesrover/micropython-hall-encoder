import utime
from machine import Pin


class EVENT:
    """ Hall effect sensor events. """
    RISING = 0b01
    FALLING = 0b10
    BOTH = 0b11


class HallEffectLatching:
    def __init__(self, read_pin: Pin, setup=True):
        self._p = read_pin

        # Previous and current values (updated at read):
        self.value_prev = None  # bool
        self.value_curr = None  # bool

        # Event storage:
        self.last_event = None  # event (by ID): int [see class `EVENT`]
        self.last_event_ms = None  # ms tick when `self.last_event` was detected: int
        self._event_new = None  # if event has been read by `self.get_event()`: bool

        if setup: self.setup()

    def setup(self):
        """
        General setup of hall effect sensor -- Engages and sets up hardware.
        """
        self._p.init(mode=Pin.IN)  # Set given Pin to input mode

    def __value_check(self, e, last, curr, event):
        """
        Check state with given values, to return updated event state.

        :return int: Updated event ID.
        """
        if self.value_prev == last and self.value_curr == curr:
            return e | event
        else:
            return e

    def _detect_event(self):
        """ Detect a new value event. """
        e = 0b0  # Default event (none)
        e = self.__value_check(e, 0, 1, EVENT.RISING)  # ORs 'RISING' to event if rising
        e = self.__value_check(e, 1, 0, EVENT.FALLING)  # ORs 'FALLING' to event if falling

        # If event is either rising or falling:
        if e & EVENT.BOTH:
            self.last_event = e  # Set event
            self.last_event_ms = utime.ticks_ms()  # Set event time
            self._event_new = True  # Set new event

    def value(self):
        """
        Return current value of sensor.

        :return bool: Current/new sensor value
        """
        self.value_prev = self.value_curr  # Set previous value to (previous) current value
        self.value_curr = bool(self._p.value())  # Read new Pin (sensor) state; cast to boo.
        self._detect_event()  # Run event detect
        return self.value_curr

    def get_new_event(self):
        """
        Get a new event, if exists.

        :return (int, int): Tuple including ew sensor event, by ID (see `EVENT`) and event ms tick time
        """
        # Return, only if hasn't been previously:
        if self._event_new:
            self._event_new = False  # Prevent future returns
            return self.last_event, utime.ticks_diff(utime.ticks_ms(), self.last_event_ms)  # Return last_event data
        return 0b0

    def reg_callback(self, f: callable, *args, **kwargs):
        """ Register pin callback (passes through to `Pin.irq` of set Pin). """
        self._p.irq(f, *args, **kwargs)
