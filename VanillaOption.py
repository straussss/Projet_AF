import numpy as np
from scipy.stats import norm


class VanillaOption:
    """
    Annual Basis default 365
    Annual Volatility: 0.16 for 16% annually
    Annual Rate: 0.03 for 3% annually
    Annual Dividend: 0.05 for 5% annually
    Maturity in days

    Pricing methods:
    BS --> Black & Scholes
    """

    def __init__(self, spot: float, strike: int, rate: float, dividend: float, maturity: int,
                 typ: str = 'C', volatility: float = 0, pricing_method: str = 'BS'):
        self.__typ = typ
        self.__spot = spot
        self.__strike = strike
        self.__rate = rate
        self.__dividend = dividend
        self.__maturity = maturity
        self.__volatility = volatility
        self.__pricing_method = pricing_method
        self.__annual_basis = 365

    @property
    def Volatility(self):
        return self.__volatility

    @Volatility.setter
    def Volatility(self, volatility):
        self.__volatility = volatility

    @property
    def Price(self):
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return VanillaOption.pricing_call_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                     self.__volatility, self.__maturity, self.__annual_basis)
            if self.__typ == 'P':
                return VanillaOption.pricing_put_bs(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                    self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Delta(self):
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return VanillaOption.delta_call(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                self.__volatility, self.__maturity, self.__annual_basis)
            if self.__typ == 'P':
                return VanillaOption.delta_put(self.__spot, self.__strike, self.__rate, self.__dividend,
                                               self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Theta(self):
        if self.__pricing_method == "BS":
            if self.__typ == 'C':
                return VanillaOption.theta_call(self.__spot, self.__strike, self.__rate, self.__dividend,
                                                self.__volatility, self.__maturity, self.__annual_basis)
            if self.__typ == 'P':
                return VanillaOption.theta_put(self.__spot, self.__strike, self.__rate, self.__dividend,
                                               self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Gamma(self):
        if self.__pricing_method == "BS":
            return VanillaOption.gamma(self.__spot, self.__strike, self.__rate, self.__dividend,
                                       self.__volatility, self.__maturity, self.__annual_basis)

    @property
    def Vega(self):
        if self.__pricing_method == "BS":
            return VanillaOption.vega(self.__spot, self.__strike, self.__rate, self.__dividend,
                                      self.__volatility, self.__maturity, self.__annual_basis)

    ############################################### BLACK & SCHOLES ####################################################
    @property
    def d1(self):
        return VanillaOption.c_d1(self.__spot, self.__strike, self.__rate, self.__dividend, self.__volatility,
                                  self.__maturity)

    @property
    def d2(self):
        return VanillaOption.c_d2(self.__spot, self.__strike, self.__rate, self.__dividend, self.__volatility,
                                  self.__maturity)

    @staticmethod
    def pricing_call_bs(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        n_d2 = VanillaOption.n(d2)
        return s * n_d1 * np.exp(-q * t / b) - k * np.exp(-r * t / b) * n_d2

    @staticmethod
    def c_d1(s, k, r, q, sig, t, b=365):
        return (np.log(s / k) + (r - q + 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @staticmethod
    def c_d2(s, k, r, q, sig, t, b=365):
        return (np.log(s / k) + (r - q - 0.5 * (sig ** 2)) * t / b) / (sig * np.sqrt(t / b))

    @staticmethod
    def n(d):
        return norm.cdf(d, 0, 1)

    @staticmethod
    def d_n(d):
        return norm.pdf(d, 0, 1)

    @staticmethod
    def pricing_put_bs(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_md1 = VanillaOption.n(-d1)
        n_md2 = VanillaOption.n(-d2)
        return k * np.exp(-r * t / b) * n_md2 - s * n_md1 * np.exp(-q * t / b)

    @staticmethod
    def delta_call(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        return np.exp(-q * t / b) * n_d1

    @staticmethod
    def delta_put(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        return np.exp(-q * t / b) * (n_d1 - 1)

    @staticmethod
    def theta_call(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_d1 = VanillaOption.n(d1)
        n_d2 = VanillaOption.n(d2)
        d_n_d1 = VanillaOption.d_n(d1)
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) + q * np.exp(-q * t / b) * s * n_d1
                - r * np.exp(-r * t / b) * k * n_d2) / b

    @staticmethod
    def theta_put(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d2 = VanillaOption.c_d2(s, k, r, q, sig, t, b)
        n_md1 = VanillaOption.n(-d1)
        n_md2 = VanillaOption.n(-d2)
        d_n_d1 = VanillaOption.d_n(d1)
        return (-np.exp(-q * t / b) * s * d_n_d1 * sig / (2 * np.sqrt(t / b)) - q * np.exp(-q * t / b) * s * n_md1
                + r * np.exp(-r * t * b) * k * n_md2) / b

    @staticmethod
    def gamma(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d_n_d1 = VanillaOption.d_n(d1)
        return (np.exp(-q * t / b) / (s * sig * np.sqrt(t / b))) * d_n_d1

    @staticmethod
    def vega(s, k, r, q, sig, t, b=365):
        d1 = VanillaOption.c_d1(s, k, r, q, sig, t, b)
        d_n_d1 = VanillaOption.d_n(d1)
        return (np.exp(-q * t / b) * s * np.sqrt(t / b) * d_n_d1) / 100

