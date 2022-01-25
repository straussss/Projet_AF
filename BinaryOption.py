import numpy as np
from scipy.stats import norm
from VanillaOption import VanillaOption


class BinaryOption(VanillaOption):
    def __init__(self, delta_max: float, spot: float, strike: int, rate: float, dividend: float, maturity: int,
                 typ: str = 'C', volatility: float = 0, pricing_method: str = 'BS'):
        VanillaOption.__init__(self, spot, strike, rate, dividend, maturity, typ, volatility=volatility,
                               pricing_method=pricing_method)
        self.__delta_max = delta_max
