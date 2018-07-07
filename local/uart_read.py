import json
import serial


PREFIX = b"DATA:"
s = serial.Serial("/dev/cu.SLAB_USBtoUART", baudrate=115200)


def decode(raw_line):
    if raw_line.startswith(PREFIX):  # Catch only if starts with PREFIX
        s = raw_line[len(PREFIX):].strip(b"\n")  # clip start and end (of byte string)
        d = json.loads(s.decode())  # Decode `bytes` into `str` and load as dictionary
        return d
    return None


while True:
    d = decode(s.readline())
    if d:
        print("\rTicks: {}".format(d['ticks']), end="")
