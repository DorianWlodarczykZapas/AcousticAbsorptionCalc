from decimal import Decimal
from typing import Dict


class Calculations:
    def __init__(self, width: Decimal, length: Decimal, height: Decimal) -> None:
        self.width: Decimal = width
        self.length: Decimal = length
        self.height: Decimal = height
        self.equipment: Dict[str, Decimal] = {}

