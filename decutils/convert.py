import binascii
import math
import struct
from decimal import Decimal
from typing import List


def float2hex(fltnum: float) -> str:
    return hex(struct.unpack(">I", struct.pack(">f", fltnum))[0])[2:]


def hex2float(hexnum: str) -> float:
    if hexnum.startswith("0x"):
        hexnum = hexnum[2:]
    return struct.unpack(">f", binascii.unhexlify(hexnum))[0]


def float2binary(fltnum: float, sep: str = "None") -> str:
    binary: str = bin(struct.unpack(">I", struct.pack(">f", fltnum))[0])[2:].zfill(32)
    if sep == "mean":
        return f"{binary[0]}_{binary[1:9]}_{binary[9:]}"
    elif sep == "length":
        return f"{binary[0:8]}_{binary[8:16]}_{binary[16:24]}_{binary[24:32]}"
    else:
        return binary


def binary2float(binary: str) -> float:
    if binary.startswith("0b"):
        binary = binary[2:]
    binary = binary.replace("_", "").replace(" ", "")
    return hex2float(hex(int(binary, 2)))


def float2fix(x: int, IL: int, FL: int, header: bool = False, select: str = "absolute", fraction: str = "ceil") -> str:
    """
    x：入力
    IL：integer length
    FL：deciminal length
    select：complement(2の補数表現) or absolute(絶対値表現, header=True を推奨)
    fraction：端数の処理 ceil(xより大きい最小の数値)，zero(0の方へ寄せる，正はfloor，負)
    """
    # 端数の処理
    if fraction == "ceil":
        x = math.ceil(x * 2 ** FL)
    elif fraction == "zero":
        x = int(x * 2 ** FL)
    elif fraction == "floor":
        x = math.floor(x * 2 ** FL)

    # オーバー(アンダー)フロー
    if x >= (max_size := 2 ** (IL + FL - 1)):
        x = max_size
    elif x <= (min_size := -1 * max_size + 1):
        x = min_size

    if select == "complement":  # 2の補数
        # 絶対値
        y: str = "0" + format(x, f"0{IL + FL - 1}b") if x >= 0 else format(x & (2 ** (IL + FL) - 1), f"0{IL+FL}b")
        # header
        y = f"{IL+FL}'b" + y if header else y
    elif select == "absolute":  # 正負記号 + 絶対値 Verilogに直書きすると2の補数になります。
        y: str = format(abs(x), f"0{IL + FL - 1}b")
        if header == True:
            if x <= 0:
                y = f"-{IL+FL}'b" + y
            else:
                y = f"{IL+FL}'b" + y
    else:
        raise Exception("Unknown Option")

    return y


def fix2float(x: str, FL: int, select: str = "absolute") -> float:
    """
    x：入力
    FL：小数部分
    select：2の補数 or 絶対値
    Args :
        select
    """
    if select == "complement":  # 2の補数
        y = -int(x[0]) << len(x) | int(x, 2)
        y /= 2 ** FL
    elif select == "absolute":  # 全て正の数と判断
        y = int(x, 2) / 2 ** FL
    else:
        raise Exception("Unknown Option")
    return y
