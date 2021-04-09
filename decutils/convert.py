import binascii
import struct


def float2hex(fltnum: float) -> str:
    return hex(struct.unpack(">I", struct.pack(">f", fltnum))[0])[2:]


def hex2float(hexnum: str) -> float:
    if hexnum.startswith("0x"):
        hexnum = hexnum[2:]
    return struct.unpack(">f", binascii.unhexlify(hexnum))[0]


def float2binary(fltnum: float, sep: str = "None") -> str:
    binary: str = (bin(int(float2hex(fltnum), 16))[2:]).zfill(32)
    if sep == "mean":
        return f"{binary[0]}_{binary[1:9]}_{binary[9:]}"
    elif sep == "length":
        return f"{binary[0:8]}_{binary[8:16]}_{binary[16:24]}_{binary[24:32]}"
    else:
        return binary


def binary2float(binary: str) -> float:
    return hex2float(hex(int(binary, 2)))
