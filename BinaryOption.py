import numpy as np
from VanillaOption import VanillaOption


class BinaryOption(VanillaOption):
    def __init__(self,
                 spot: float,
                 strike: int,
                 rate: float,
                 dividend: float,
                 maturity: int,
                 typ: str = 'C',
                 volatility: float = 0,
                 payoff: float = 1,
                 delta_max: float = 1,
                 pricing_method: str = 'BS'):
        super().__init__(spot, strike, rate, dividend, maturity, typ, volatility, pricing_method)
        self.__payoff = payoff
        self.__delta_max = delta_max


    @property
    def a(self) -> float:
        return self.__SecondClass__pricing_method

    @property
    def Payoff(self) -> float:
        return self.__payoff

    @Payoff.setter
    def Payoff(self, payoff):
        self.__payoff = payoff

    @property
    def Delta_max(self) -> float:
        return self.__delta_max

    @Delta_max.setter
    def Delta_max(self, delta_max):
        self.__delta_max = delta_max

    @property
    def Price_call_digital(self) -> float:
        if self.Pricing_method == "BS":
            return BinaryOption.pricing_call_digital_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                        self.__volatility, self.__maturity, self.__annual_basis,
                                                        self.__payoff)

    @property
    def Price_put_digital(self) -> float:
        if self.Pricing_method == "BS":
            return BinaryOption.pricing_put_digital_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                       self.__volatility, self.__maturity, self.__annual_basis,
                                                       self.__payoff)

    @property
    def Price_call_spread(self) -> float:
        if self.Pricing_method == "BS":
            return BinaryOption.pricing_call_digital_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                        self.__volatility, self.__maturity, self.__annual_basis,
                                                        self.__payoff)

    @property
    def Price_put_spread(self) -> float:
        if self.Pricing_method == "BS":
            return BinaryOption.pricing_put_digital_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                       self.__volatility, self.__maturity, self.__annual_basis,
                                                       self.__payoff)

    @property
    def Delta_th(self) -> float:
        if self.Pricing_method == "BS":
            if self.__typ == 'C':
                return BinaryOption.delta_digital_call_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                          self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Delta_rp(self) -> float:
        if self.Pricing_method == "BS":
            if self.__typ == 'C':
                return self.delta_bull_call_spread_bs()

    ############################################### BLACK & SCHOLES ####################################################

    ############################################### THEORICAL
    @staticmethod
    def pricing_call_digital_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b: int = 365,
                                p: float = 1) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :param p: payoff
        :return: the price of a digital call with the BS model (Bull digital)
        """
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_d2 = VanillaOption.n(d2)
        return p * np.exp(-r * t / b) * n_d2

    @staticmethod
    def pricing_put_digital_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b: int = 365,
                               p: float = 1) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :param p: payoff
        :return: the price of a digital put with the BS model (Bear digital)
        """
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_md2 = VanillaOption.n(-d2)
        return p * np.exp(-r * t / b) * n_md2

    @staticmethod
    def delta_digital_call_bs(s: float, k: float, r: float, q: float, sig: float, t: int, b=365) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param b: annual basis 365 days per year
        :return: the delta of a digital call with the BS model
        """
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        d_n_d2 = VanillaOption.d_n(d2)
        return (np.exp(-r * t / b) * d_n_d2)/(sig * s * np.sqrt(t / b))

    ############################################### REPLICATION

    @staticmethod
    def pricing_bull_call_spread_bs(s: float, k: float, r: float, q: float, sig: float, t: int,
                                    p: float = 1, delta_max: int = 1) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param p: payoff
        :param delta_max: maximum delta possible for the position
        :return: the price of a n delta_max call spread with a spread of (payoff/delta_max)
        """
        l_call = VanillaOption.pricing_call_bs(s, k - (p / delta_max), r, q, sig, t)
        s_call = VanillaOption.pricing_call_bs(s, k, r, q, sig, t)
        return (l_call - s_call) * delta_max

    def delta_bull_call_spread_bs(self) -> float:
        return VanillaOption.delta_call_bs(self.__spot, self.__strike - (self.__payoff/self.__delta_max),
                                           self.__rate, self.__dividend, self.__volatility, self.__maturity) -\
                VanillaOption.delta_call_bs(self.__spot, self.__strike, self.__rate, self.__dividend, self.__volatility,
                                            self.__maturity)

    @staticmethod
    def pricing_bear_call_spread_bs(s: float, k: float, r: float, q: float, sig: float, t: int,
                                    p: float = 1, delta_max: int = 1) -> float:
        """
        :param s: spot price
        :param k: stirke price
        :param r: risk free rate 0.05 corresponds to 5%
        :param q: dividend yield 0.01 corresponds to 1%
        :param sig: volatility 0.16 corresponds to 16%
        :param t: maturity in days
        :param p: payoff
        :param delta_max: maximum delta possible for the position
        :return: the price of a n delta_max put spread with a spread of (payoff/delta_max)
        """
        l_call = VanillaOption.pricing_call_bs(s, k, r, q, sig, t)
        s_call = VanillaOption.pricing_call_bs(s, k - (p / delta_max), r, q, sig, t)
        return (l_call - s_call) * delta_max


