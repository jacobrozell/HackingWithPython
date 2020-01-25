from winreg import *
import datetime
import string


def get_subkeys(key):
    for i in range(QueryInfoKey(key)[0]):
        name = EnumKey(key, i)
        yield (name, OpenKey(key, name))


def get_values(key):
    for i in range(QueryInfoKey(key)[1]):
        name, value, val_type = EnumValue(key, i)
        yield (name, value)


def time_convert(ns):
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=ns / 1e7)

def is_printable(s):
    return not any(repr(ch).startswith("'\\x") or repr(ch).startswith("'\\u") for ch in s)


def parse_bin(bin_data):
    nhex = ["{:02X}".format(i) for i in bin_data]

    rows = []
    count = len(nhex)
    for row in range(int(count / 8.0)):
        rows += [" ".join(nhex[int(row * 8):int((row + 1) * 8.0)])]
        return "\n\t\t".join(rows)


def parse_bin_complete(bin_data):
    out = ""
    zero_row = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    blocks = bin_data.split(zero_row)

    for block in blocks:
        out += '\n\t\t'
        out += block.decode('utf-8', errors='ignore')
    return ''.join(ch for ch in out if is_printable(ch))
    #return list(filter(lambda x: x in string.printable, out))


loc = r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU"

with OpenKey(HKEY_CURRENT_USER, loc, 0, KEY_READ | KEY_WOW64_64KEY) as mru:
    for subkey in get_subkeys(mru):
        modtime = time_convert(QueryInfoKey(subkey[1])[2])
        print(u"\n\n{}: modified {}".format(subkey[0], modtime))
        for value in get_values(subkey[1]):
            print(u"\t{}:\n\t\t{}".format(value[0], parse_bin_complete(value[1])))

