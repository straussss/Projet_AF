import numpy as np
from VanillaOption import VanillaOption
from BlackScholes import BlackScholes


class BinaryOption(BlackScholes):
    def __init__(self,
                 spot: float,
                 strike: int,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 volatility: float = 0,
                 typ: str = 'C',
                 rep: str = 'C',
                 payoff: float = 1,
                 delta_max: float = 1,
                 pricing_method: str = 'BS',
                 annual_basis: int = 365):
        BlackScholes.__init__(self, spot, strike, rate, dividend, maturity, volatility, annual_basis)
        self.__payoff = payoff
        self.__delta_max = delta_max
        self.__pricing_method = pricing_method
        self.__typ = typ
        self.__rep = rep

    @property
    def volatility(self) -> float:
        return self._volatility

    @volatility.setter
    def volatility(self, volatility):
        self._volatility = volatility

    @property
    def payoff(self) -> float:
        return self.__payoff

    @payoff.setter
    def payoff(self, payoff):
        self.__payoff = payoff

    @property
    def delta_max(self) -> float:
        return self.__delta_max

    @delta_max.setter
    def delta_max(self, delta_max):
        self.__delta_max = delta_max

    @property
    def pricing_method(self) -> str:
        return self.__pricing_method

    @pricing_method.setter
    def pricing_method(self, pricing_method):
        self.__pricing_method = pricing_method

    @property
    def strike_overh(self):
        return self.stirke - (self.payoff / self.delta_max)

    @property
    def price_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.price_call_digital_bs(self.payoff)
            if self.__typ == 'P':
                return self.price_put_digital_bs(self.payoff)

    @property
    def delta_th(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.delta_digital_call_bs

    @property
    def price_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C': #Bull Spread
                if self.__rep == 'C':
                    return (self.rep_option_km().price - self.rep_option_k().price) * self.delta_max
                if self.__rep == 'P':
                    pass
            if self.__typ == 'P':
                if self.__rep == 'C':
                    return (self.rep_option_k().price - self.rep_option_km().price) * self.delta_max
                if self.__rep == 'P':
                    pass

    @property
    def delta_rp(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return 0.01

    ############################################### REPLICATION
    def rep_option_k(self):
        return VanillaOption(self.spot,
                             self.stirke,
                             self.rate,
                             self.dividend,
                             self.maturity,
                             self.__typ,
                             self.volatility)

    def rep_option_km(self):
        return VanillaOption(self.spot,
                             self.strike_overh,
                             self.rate,
                             self.dividend,
                             self.maturity,
                             self.__typ,
                             self.volatility)



