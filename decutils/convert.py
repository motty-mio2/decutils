import binascii
import math
import struct


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


def float2fix(x: float, IL: int, FL: int, header: bool = False, complement: bool = False, round: str = "ceil") -> str:
    """convert Single float to fixed point expression
    Args:
        x (float): flaot number
        IL (int): expression length of integer part
        FL (int): expression length of fraction part
        header (bool, optional): Add header "0b" / "-0b" for verilog. Defaults to False.
        complement (bool, optional):
            True : Use complement.
            False : Use absolute.
            Defaults to False (absolute).
        round (str, optional): Way of round up.
            ceil, zero, floor.
            Defaults to "ceil".

    Raises:
        ValueError: Unknown argument

    Returns:
        str: fixed point expression of input number
    """

    shifted_x: int = 0
    expression_length: int = IL + FL
    # 端数の処理
    if round == "ceil":
        shifted_x = math.ceil(x * 2 ** FL)
    elif round == "zero":
        shifted_x = int(x * 2 ** FL)
    elif round == "floor":
        shifted_x = math.floor(x * 2 ** FL)
    else:
        raise ValueError()

    # Check Over / Under flow
    if x >= (max_size := 2 ** (IL + FL) - 1):
        x = max_size
    elif x <= (min_size := -1 * max_size + 1):
        x = min_size

    y: str = ""
    if complement:  # Complement
        y = bin(shifted_x & ((1 << (expression_length)) - 1))[2:]
        # y = "0" + format(x, f"0>{IL + FL - 1}b") if x >= 0 else format(x & (2 ** (IL + FL) - 1), f"1>{IL+FL}b")
        y = f"{expression_length}'b" + y if header else y  # header
    else:  # Absolute
        y = format(abs(x), f"0{IL + FL}b")
        if header:
            if x <= 0:
                y = f"-{expression_length}'b" + y
            else:
                y = f"{expression_length}'b" + y
    return y


def fix2float(x: str, FL: int, complement: bool = False) -> float:
    """Conver fixed point number to Single float

    Args:
        x (str): fixed point number
        FL (int): expression length of fraction part
        complement (bool, optional):
            True : Use complement.
            False : Use absolute.
            Defaults to False (absolute).

    Returns:
        float: single float expression for input number
    """

    if x.startswith("0b"):
        x = x[2:]

    y: float = 0.0
    if complement:  # Use complement
        y = -int(x[0]) << len(x) | int(x, 2)
        y /= 2 ** FL
    else:
        y = int(x, 2) / 2 ** FL
    return y
