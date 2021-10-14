from dataclasses import dataclass
from typing import Any, List, Union
import numpy as np


@dataclass
class ff_convert:
    """'ff' is 'fixed' and 'float'
    conver fixed <--> float number
    Args:
        int_length (int): expression length of integer part
        float_length (int): expression length of fraction part
        header (bool, optional): Add header "0b" / "-0b" for verilog. Defaults to False.
        complement (bool, optional):
            True : Use complement.
            False : Use absolute.
            Defaults to False (absolute).
        round (str, optional): Way of round up.
            ceil, zero, floor.
            Defaults to "ceil".
    """

    int_length: int
    float_length: int
    header: bool = False
    complement: bool = False
    round: str = "ceil"

    def float2fix(self, x: float) -> str:
        """convert Single float to fixed point expression
        Args:
            x (float): flaot number

        Raises:
            ValueError: Unknown argument

        Returns:
            str: fixed point expression of input number
        """

        shifted_x: int = 0
        expression_length: int = self.int_length + self.float_length

        if round == "ceil":
            shifted_x = np.ceil(x * 2 ** self.float_length)
        elif round == "zero":
            shifted_x = int(x * 2 ** self.float_length)
        elif round == "floor":
            shifted_x = np.floor(x * 2 ** self.float_length)
        else:
            raise ValueError()

        # Check Over / Under flow
        if x >= (max_size := 2 ** (self.int_length + self.float_length) - 1):
            x = max_size
        elif x <= (min_size := -1 * max_size + 1):
            x = min_size

        y: str = ""
        if self.complement:  # Complement
            y = bin(shifted_x & ((1 << (expression_length)) - 1))[2:]
            # y = "0" + format(x, f"0>{self.int_length + self.float_length - 1}b") if x >= 0 else format(x & (2 ** (self.int_length + self.float_length) - 1), f"1>{self.int_length+self.float_length}b")
            y = f"{expression_length}'b" + y if self.header else y  # header
        else:  # Absolute
            y = format(abs(shifted_x), f"0{expression_length}b")
            if self.header:
                if x <= 0:
                    y = f"-{expression_length}'b" + y
                else:
                    y = f"{expression_length}'b" + y
        return y

    def fix2float(self, x: str) -> float:
        """Conver fixed point number to Single float

        Args:
            x (str): fixed point number

        Returns:
            float: single float expression for input number
        """

        if x.startswith("0b"):
            x = x[2:]

        y: float = 0.0
        if self.complement:  # Use complement
            y = -int(x[0]) << len(x) | int(x, 2)
            y /= 2 ** self.float_length
        else:
            y = int(x, 2) / 2 ** self.float_length
        return y
