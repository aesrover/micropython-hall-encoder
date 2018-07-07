import utime

from .hall_sensor import HallEffectLatching


class DualHallEncoder:
    """ Handles two latching hall effect sensors to catch and record directional encoder ticks. """

    def __init__(self, h1: HallEffectLatching, h2: HallEffectLatching):
        self.h1 = h1
        self.h2 = h2

        # Times of last handled events:
        self.last_handled_1_ms = None
        self.last_handled_2_ms = None

        self._enc_tick = 0  # Private: current encoder tick (see `self.ticks()`)

    def detect_tick(self):
        """
        Run tick detect, to check if new hall effect sensor event has occurred.

        :return bool: If new tick was recorded
        """
        # Read hall effect sensors:
        self.h1.value()
        self.h2.value()

        # Test if either sensor has new event, and events match:
        if ((not self.h1.last_event_ms == self.last_handled_1_ms or not self.h2.last_event_ms == self.last_handled_2_ms)
                and self.h1.last_event == self.h2.last_event):
            # Set last event time, to current:
            self.last_handled_1_ms = self.h1.last_event_ms
            self.last_handled_2_ms = self.h2.last_event_ms
            # Calculate difference between event trigger time:
            diff = utime.ticks_diff(self.h2.last_event_ms, self.h1.last_event_ms)
            # Add if positive movement, subtract if negative
            if diff > 0:
                self._enc_tick += 1
            elif diff < 0:
                self._enc_tick -= 1
            return True
        return False

    @property
    def ticks(self):
        """ Current encoder tick. """
        return self._enc_tick
