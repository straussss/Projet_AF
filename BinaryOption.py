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
    def price_digital(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.pricing_call_digital_bs()
            if self.__typ == 'P':
                return self.pricing_put_digital_bs()

    @property
    def delta_th(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return self.delta_digital_call_bs()

    @property
    def price_bull_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__rep == 'C':
                return (self.rep_option_km().price - self.rep_option_k().price) * self.delta_max
            if self.__rep == 'P':
                pass

    @property
    def price_bear_spread(self) -> float:
        if self.pricing_method == "BS":
            if self.__rep == 'C':
                return (self.rep_option_k().price - self.rep_option_km().price) * self.delta_max
            if self.__rep == 'P':
                pass

    @property
    def delta_rp(self) -> float:
        if self.pricing_method == "BS":
            if self.__typ == 'C':
                return 0.01

    ############################################### BLACK & SCHOLES ####################################################

    ############################################### THEORICAL

    def pricing_call_digital_bs(self) -> float:
        """
        :return: the price of a digital call with the BS model (Bull digital)
        """
        p = self.__payoff
        r = self.rate
        t = self.maturity
        b = self.annual_basis
        n_d2 = self.n_d2
        return p * np.exp(-r * t / b) * n_d2

    def pricing_put_digital_bs(self) -> float:
        """
        :return: the price of a digital put with the BS model (Bear digital)
        """
        p = self.__payoff
        r = self.__rate
        t = self.__maturity
        b = self.__annual_basis
        n_md2 = 1 - self.n_d2
        return p * np.exp(-r * t / b) * n_md2

    def delta_digital_call_bs(self) -> float:
        """
        :return: the delta of a digital call with the BS model
        """
        s = self.__spot
        r = self.__rate
        t = self.__maturity
        sig = self._volatility
        b = self.__annual_basis
        d_n_d2 = self.d_n_d2
        return (np.exp(-r * t / b) * d_n_d2)/(sig * s * np.sqrt(t / b))

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
                             self.stirke - (self.payoff / self.delta_max),
                             self.rate,
                             self.dividend,
                             self.maturity,
                             self.__typ,
                             self.volatility)



